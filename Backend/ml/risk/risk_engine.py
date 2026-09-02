"""
PIWOT Legal Advisor — Explainable Risk Engine & Inconsistency Detection Service
Quantifies overall contract risk (0-100), detects date/jurisdiction contradictions,
flags severe clause terms with exact page citations, and checks for missing essential clauses.
"""

import datetime
from typing import Dict, List, Any, Optional

# Essential standard clauses that every commercial contract should contain
ESSENTIAL_CLAUSES = {
    "limitation_of_liability": {"category": "liability", "penalty": 15, "desc": "Missing Limitation of Liability Clause (Exposes parties to uncapped statutory damages)"},
    "dispute_resolution": {"category": "dispute_resolution", "penalty": 10, "desc": "Missing Dispute Resolution / Arbitration Mechanism"},
    "confidentiality": {"category": "confidentiality", "penalty": 10, "desc": "Missing Confidentiality / Proprietary Information Protection Clause"},
    "termination": {"category": "termination", "penalty": 10, "desc": "Missing Clear Termination / Exit Clause"}
}


class LegalRiskEngine:
    """Calculates explainable risk scores and detects contractual anomalies."""

    def __init__(self):
        pass

    def check_date_inconsistencies(self, entities: Dict[str, Any], chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detects chronological date contradictions (e.g. Effective Date > Expiration Date)."""
        issues = []
        eff_str = entities.get("effective_date")
        exp_str = entities.get("expiry_date")

        if eff_str and exp_str:
            try:
                eff_dt = datetime.date.fromisoformat(eff_str)
                exp_dt = datetime.date.fromisoformat(exp_str)

                if eff_dt > exp_dt:
                    # Find page reference
                    page_ref = 1
                    for c in chunks:
                        if eff_str in c["text"] or exp_str in c["text"]:
                            page_ref = c["page_start"]
                            break

                    issues.append({
                        "type": "CHRONOLOGICAL_CONTRADICTION",
                        "severity": "High",
                        "weight": 35,
                        "title": "Effective Date Occurs After Expiration Date",
                        "description": f"The contract effective date ({eff_str}) is chronologically later than the specified expiration date ({exp_str}).",
                        "evidence": f"Effective: {eff_str} | Expiration: {exp_str}",
                        "page": page_ref
                    })
            except Exception:
                pass

        return issues

    def check_jurisdiction_conflicts(self, entities: Dict[str, Any], chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detects conflicting governing laws or mismatched arbitration venues."""
        issues = []
        all_j = entities.get("all_jurisdictions", [])
        venues = entities.get("dispute_venues", [])

        if len(all_j) > 1:
            page_ref = 1
            for c in chunks:
                if any(j in c["text"] for j in all_j):
                    page_ref = c["page_start"]
                    break

            issues.append({
                "type": "JURISDICTION_CONFLICT",
                "severity": "Medium",
                "weight": 20,
                "title": "Multiple Competing Governing Laws Mentioned",
                "description": f"Contract references multiple distinct legal jurisdictions: {', '.join(all_j)}.",
                "evidence": f"Jurisdictions detected: {', '.join(all_j)}",
                "page": page_ref
            })

        return issues

    def check_high_risk_clauses(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Inspects classified chunks for severe terms and penalty clauses."""
        risk_reasons = []

        for c in chunks:
            cat = c.get("category", "")
            text = c.get("text", "")
            lower_text = text.lower()
            page = c.get("page_start", 1)

            # 1. Uncapped Liability
            if cat == "liability" and any(k in lower_text for k in ["unlimited liability", "uncapped", "without limitation"]):
                risk_reasons.append({
                    "type": "UNCAPPED_LIABILITY",
                    "severity": "High",
                    "weight": 25,
                    "title": "Uncapped / Unlimited Liability Clause",
                    "description": "The contract imposes uncapped or unlimited damages on one or more parties.",
                    "evidence": text[:200] + ("..." if len(text) > 200 else ""),
                    "page": page
                })

            # 2. Unilateral / Immediate Termination Without Cause
            if cat == "termination" and any(k in lower_text for k in ["sole right to terminate immediately", "without cause and without any payment", "unilateral"]):
                risk_reasons.append({
                    "type": "UNILATERAL_TERMINATION",
                    "severity": "High",
                    "weight": 20,
                    "title": "Immediate Unilateral Termination Without Cause",
                    "description": "One party reserves the exclusive right to cancel without notice or penalty.",
                    "evidence": text[:200] + ("..." if len(text) > 200 else ""),
                    "page": page
                })

            # 3. Excessive Non-Compete
            if cat == "non_compete" and any(k in lower_text for k in ["five (5) years", "ten (10) years", "worldwide", "any competing business"]):
                risk_reasons.append({
                    "type": "EXCESSIVE_RESTRICTION",
                    "severity": "High",
                    "weight": 20,
                    "title": "Excessive Non-Compete Scope or Duration",
                    "description": "The covenant non-compete duration or geographic scope may be legally unreasonable or punitive.",
                    "evidence": text[:200] + ("..." if len(text) > 200 else ""),
                    "page": page
                })

            # 4. Aggressive Liquidated Penalties
            if cat == "payment" and any(k in lower_text for k in ["20%", "25%", "liquidated penalty", "non-refundable and due immediately"]):
                risk_reasons.append({
                    "type": "AGGRESSIVE_PAYMENT_PENALTY",
                    "severity": "Medium",
                    "weight": 15,
                    "title": "Disproportionate Payment Penalty / Non-Refundability",
                    "description": "Contract mandates immediate forfeiture or high liquidated default penalties.",
                    "evidence": text[:200] + ("..." if len(text) > 200 else ""),
                    "page": page
                })

        return risk_reasons

    def check_missing_essential_clauses(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flags omission of standard protective clauses."""
        detected_categories = set(c.get("category", "") for c in chunks)
        missing_reasons = []

        for key, info in ESSENTIAL_CLAUSES.items():
            if info["category"] not in detected_categories:
                missing_reasons.append({
                    "type": "MISSING_ESSENTIAL_CLAUSE",
                    "severity": "Medium" if info["penalty"] >= 15 else "Low",
                    "weight": info["penalty"],
                    "title": info["desc"],
                    "description": f"Standard commercial agreements typically include a {info['category'].replace('_', ' ')} provision.",
                    "evidence": "Clause absent from parsed document sections.",
                    "page": 1
                })

        return missing_reasons

    def evaluate_contract_risk(
        self,
        document_schema: Dict[str, Any],
        classified_chunks: List[Dict[str, Any]],
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Computes composite 0-100 risk score and generates explainable audit report.
        """
        date_issues = self.check_date_inconsistencies(entities, classified_chunks)
        jurisdiction_issues = self.check_jurisdiction_conflicts(entities, classified_chunks)
        clause_risks = self.check_high_risk_clauses(classified_chunks)
        missing_clauses = self.check_missing_essential_clauses(classified_chunks)

        all_inconsistencies = date_issues + jurisdiction_issues
        all_reasons = all_inconsistencies + clause_risks + missing_clauses

        # Base clean score = 10 (all contracts have minor inherent operational risk)
        raw_score = 10 + sum(r["weight"] for r in all_reasons)
        score = min(max(raw_score, 0), 100)

        if score >= 70:
            level = "High"
        elif score >= 35:
            level = "Medium"
        else:
            level = "Low"

        return {
            "score": score,
            "level": level,
            "total_risk_factors": len(all_reasons),
            "reasons": all_reasons,
            "inconsistencies": all_inconsistencies
        }
