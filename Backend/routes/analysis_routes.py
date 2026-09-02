"""
PIWOT Legal Advisor — Analysis & System API Blueprint
Defines REST endpoints for contract analysis, system health, and model capabilities.
"""

import os
import werkzeug.utils
from flask import Blueprint, request, jsonify, current_app

from services.analyzer_service import ContractAnalysisService
from ml.preprocessing.document_pipeline import DocumentPreprocessingError

analysis_bp = Blueprint("analysis", __name__)

# Global analysis service instance
_analysis_service = None


def get_analysis_service() -> ContractAnalysisService:
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = ContractAnalysisService()
    return _analysis_service


@analysis_bp.route("/api/health", methods=["GET"])
def health_check():
    """Returns service health status and active model status."""
    service = get_analysis_service()
    return jsonify({
        "status": "healthy",
        "service": "PIWOT Legal Advisor ML Backend",
        "models": {
            "clause_classifier": service.classifier.active_backend,
            "retriever": "SentenceTransformer (all-MiniLM-L6-v2)",
            "risk_engine": "Rule & Anomaly Scorer v1.0",
            "summarizer": "TextRank Graph Extractor"
        }
    }), 200


@analysis_bp.route("/api/models", methods=["GET"])
def model_info():
    """Returns technical details on the active ML models."""
    service = get_analysis_service()
    return jsonify({
        "classifier_backend": service.classifier.active_backend,
        "supported_categories": [
            "termination", "governing_law", "confidentiality", "indemnification",
            "liability", "payment", "intellectual_property", "dispute_resolution",
            "warranty", "force_majeure", "non_compete", "miscellaneous"
        ],
        "local_execution": True,
        "llm_dependency": False
    }), 200


@analysis_bp.route("/api/analyze", methods=["POST"])
def analyze_contract_api():
    """
    Main canonical ML contract analysis endpoint.
    Accepts multipart/form-data with 'file' or 'resume'.
    """
    file = request.files.get("file") or request.files.get("resume")
    if not file or not file.filename:
        return jsonify({"error": "No file uploaded. Please upload a PDF contract under field 'file'."}), 400

    filename = werkzeug.utils.secure_filename(file.filename)
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Unsupported file format. Only PDF files are supported."}), 400

    try:
        pdf_bytes = file.read()
        service = get_analysis_service()
        analysis_result = service.analyze_pdf_document(pdf_bytes, filename=filename)
        return jsonify(analysis_result), 200
    except DocumentPreprocessingError as de:
        return jsonify({"error": str(de)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal analysis error: {str(e)}"}), 500


@analysis_bp.route("/analyze", methods=["POST"])
def analyze_legacy_adapter():
    """
    Backward-compatible adapter for legacy frontend / scripts.
    Returns both the legacy 'response' text summary and the complete structured JSON.
    """
    file = request.files.get("resume") or request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Invalid file or no file uploaded"}), 400

    filename = werkzeug.utils.secure_filename(file.filename)
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Invalid file or no file uploaded"}), 400

    try:
        pdf_bytes = file.read()
        service = get_analysis_service()
        analysis_result = service.analyze_pdf_document(pdf_bytes, filename=filename)

        # Build legacy summary response string
        summary_sentences = analysis_result["summary"].get("summary_sentences", [])
        risk_level = analysis_result["risk"]["level"]
        risk_score = analysis_result["risk"]["score"]

        response_str = f"CONTRACT SUMMARY (Risk: {risk_level}, Score: {risk_score}/100):\n" + "\n".join(f"• {s}" for s in summary_sentences)

        # Merge legacy key with full structured response
        response_payload = dict(analysis_result)
        response_payload["response"] = response_str

        return jsonify(response_payload), 200
    except DocumentPreprocessingError as de:
        return jsonify({"error": str(de)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
