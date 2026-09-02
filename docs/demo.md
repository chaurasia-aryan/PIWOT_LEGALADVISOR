# PIWOT Legal Advisor: Live Demo & Walkthrough Guide

This guide walks through testing and demonstrating the PIWOT Legal Advisor platform using sample benchmark contracts.

---

## 1. Quick Launch

Open two terminal windows:

### Terminal 1: Start ML Backend
```bash
cd Backend
python app.py
```
*Expected output: `Running on http://127.0.0.1:5000`*

### Terminal 2: Start Next.js Frontend
```bash
cd frontend
npm run dev
```
*Expected output: `Ready in http://localhost:3000`*

---

## 2. Interactive Demo Walkthrough

1. Open your browser and navigate to:
   ```
   http://localhost:3000/Dashboard
   ```
2. You will see the **PIWOT Legal Advisor** dashboard, the prototype disclaimer banner, the drag-and-drop PDF upload zone, and the contract history table.

3. **Test Case 1: Standard Commercial MSA (Low Risk)**
   - Upload `ml/data/sample_contracts/sample_msa_contract.pdf`.
   - The UI will show a processing spinner while running local CPU inference (~10-15 seconds).
   - The **Contract Analysis Modal** will appear automatically:
     - **Risk Badge**: `Low Risk (20/100)`
     - **Extractive Summary**: 4 key sentences distilled via TextRank with page numbers cited.
     - **Clause Breakdown**: 6 classified clauses with >80% confidence and reference benchmark comparisons.
     - **Key Metadata**: Contracting parties (*Apex Global Solutions LLC* and *Quantum Byte Technologies Inc*), normalized dates, Net 30 payment terms, and Delaware jurisdiction.

4. **Test Case 2: High-Risk Contract with Severe Clauses & Contradictions (High Risk)**
   - Upload `ml/data/sample_contracts/sample_high_risk_contract.pdf`.
   - The **Contract Analysis Modal** will display:
     - **Risk Badge**: `High Risk (100/100)`
     - **Risk Factors & Anomalies**:
       - ⚠️ **Uncapped Liability Provision**: Detects unlimited liability without exclusion for indirect damages.
       - ⚠️ **Severe Non-Compete Overreach**: Detects 5-year duration and worldwide restriction.
       - ⚠️ **Unilateral Termination**: Detects termination at sole discretion without cause on 24 hours notice.
       - ⚠️ **Chronological Date Contradiction**: Flags effective date (June 1, 2024) is later than expiration date (January 1, 2024).

5. **Test Case 3: Filtering and Searching**
   - Use the category dropdown in the **Clause Breakdown** tab to isolate `High Risk Clauses Only` or specific categories like `Termination` or `Liability`.
   - Close the modal and test the search bar in the table to find contracts by party name or document title.

---

## 3. Automated Headless Verification

To run the automated browser test suite that executes this entire flow automatically:
```bash
python tests/test_browser_flow.py
```
*Expected output: `ALL BROWSER END-TO-END TESTS PASSED!`*
