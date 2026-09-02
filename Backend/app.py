"""
PIWOT Legal Advisor — Flask Application Entrypoint
Serves local ML/DL legal contract analysis endpoints with full multi-page PDF processing.
"""

import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Configure CORS for all origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Maximum upload size: 16 MB
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))

    # Register blueprints
    from routes.analysis_routes import analysis_bp
    app.register_blueprint(analysis_bp)

    @app.route("/")
    def index():
        return jsonify({
            "service": "PIWOT Legal Advisor ML/DL Backend",
            "version": "2.0.0",
            "status": "online",
            "endpoints": {
                "health": "/api/health",
                "models": "/api/models",
                "analyze": "POST /api/analyze"
            }
        })

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({"error": "Uploaded file exceeds the 16MB maximum file size limit."}), 413

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "An internal server error occurred."}), 500

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug_mode, use_reloader=False)
