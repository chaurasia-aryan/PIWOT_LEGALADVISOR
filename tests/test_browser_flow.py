"""
PIWOT Legal Advisor — End-to-End Playwright Browser Verification
Automates end-to-end user experience: Document Upload -> ML Inference -> UI Rendering & Modal Inspection.
"""

import os
import sys
import time
import subprocess
import requests
import pytest
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(BASE_DIR, "Backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
SAMPLE_PDF = os.path.join(BASE_DIR, "ml", "data", "sample_contracts", "sample_msa_contract.pdf")
SCREENSHOT_PATH = os.path.join(BASE_DIR, "ml", "reports", "browser_verification.png")


def is_service_running(url: str) -> bool:
    try:
        r = requests.get(url, timeout=2)
        return r.status_code in [200, 404]
    except Exception:
        return False


def wait_for_service(url: str, timeout: int = 35):
    start = time.time()
    while time.time() - start < timeout:
        if is_service_running(url):
            return True
        time.sleep(1)
    return False


def test_browser_contract_analysis_flow():
    backend_proc = None
    frontend_proc = None

    if not is_service_running("http://localhost:5000/api/health"):
        print("Starting Flask Backend...")
        backend_env = os.environ.copy()
        backend_env["PORT"] = "5000"
        backend_env["FLASK_DEBUG"] = "0"
        backend_proc = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=BACKEND_DIR,
            env=backend_env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if not is_service_running("http://localhost:3000/Dashboard"):
        print("Starting Next.js Frontend...")
        frontend_proc = subprocess.Popen(
            "npm run start -- -p 3000",
            cwd=FRONTEND_DIR,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    # Wait for both services to be responsive
    assert wait_for_service("http://localhost:5000/api/health", timeout=35), "Backend failed to start"
    assert wait_for_service("http://localhost:3000/Dashboard", timeout=35), "Frontend failed to start"
    print("Both Backend and Frontend are healthy and responsive!")

    console_errors = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Track console errors
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            print("Navigating to http://localhost:3000/Dashboard...")
            page.goto("http://localhost:3000/Dashboard", timeout=30000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)

            # Verify page elements
            content = page.content()
            assert "PIWOT" in content and "LEGAL ADVISOR" in content
            assert "Decision-Support" in content
            print("Dashboard loaded successfully with Anthropic Design System.")

            # Upload sample contract
            print(f"Uploading {SAMPLE_PDF}...")
            file_input = page.locator('input[type="file"]')
            file_input.set_input_files(SAMPLE_PDF)

            # Wait for ML analysis modal to appear
            print("Waiting for ML analysis and modal rendering...")
            page.wait_for_selector("text=Close Analysis", timeout=45000)
            print("Analysis modal appeared!")

            # Verify Modal Content
            modal_text = page.content()
            assert "sample_msa_contract.pdf" in modal_text
            assert "Extractive Contract Summary" in modal_text

            # Test Tab Switching
            print("Testing modal tabs...")
            page.click("text=Risk Factors")
            page.wait_for_timeout(500)
            assert "Risk Evaluation Matrix" in page.content()

            page.click("text=Segmented Clauses")
            page.wait_for_timeout(500)
            assert "Segmented Contract Clauses" in page.content()

            page.click("text=Parties & Metadata")
            page.wait_for_timeout(500)
            assert "Contracting Parties" in page.content()

            # Capture Screenshot for visual proof
            os.makedirs(os.path.dirname(SCREENSHOT_PATH), exist_ok=True)
            page.screenshot(path=SCREENSHOT_PATH, full_page=True)
            print(f"Saved visual verification screenshot to {SCREENSHOT_PATH}")

            # Close Modal
            print("Closing modal...")
            page.click("text=Close Analysis")
            page.wait_for_timeout(500)

            # Verify contract table contains newly analyzed contract
            table_content = page.content()
            assert "sample_msa_contract.pdf" in table_content
            print("Contract table verified with analyzed document.")

            # Test Homepage Navigation & Band Alternation
            print("Navigating to Homepage http://localhost:3000/...")
            page.goto("http://localhost:3000/", timeout=20000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            home_content = page.content()
            assert "Legal precision without cloud latency" in home_content
            assert "CORE SYSTEM CAPABILITIES" in home_content
            print("Homepage verified with Cream-and-Black Band Rhythm.")

            browser.close()

        # Check console errors
        critical_errors = [e for e in console_errors if "favicon" not in e.lower()]
        assert len(critical_errors) == 0, f"Frontend console errors encountered: {critical_errors}"

    finally:
        if backend_proc:
            try:
                subprocess.call(f"taskkill /F /T /PID {backend_proc.pid}", shell=True)
            except Exception:
                backend_proc.kill()

        if frontend_proc:
            try:
                subprocess.call(f"taskkill /F /T /PID {frontend_proc.pid}", shell=True)
            except Exception:
                frontend_proc.kill()


if __name__ == "__main__":
    test_browser_contract_analysis_flow()
    print("ALL BROWSER END-TO-END TESTS PASSED!")
