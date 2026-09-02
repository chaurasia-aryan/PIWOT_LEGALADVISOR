"""
Legal Dataset Acquisition and Synthetic Preprocessing Pipeline.
Manages downloading and generating canonical datasets for PIWOT Legal Advisor.
"""

import os
import json
import csv
from typing import Dict, List, Tuple
import fitz  # PyMuPDF

CURATED_CLAUSES = [
    # Termination
    {"category": "termination", "text": "This Agreement may be terminated by either party upon thirty (30) days prior written notice in the event of a material breach by the other party that remains uncured.", "source": "LEDGAR/CUAD", "risk_level": "Medium"},
    {"category": "termination", "text": "Company reserves the sole right to terminate this Agreement immediately without cause and without any payment of penalty or compensation to Contractor.", "source": "CUAD", "risk_level": "High"},
    {"category": "termination", "text": "Upon termination of this Agreement for any reason, all licenses granted hereunder shall immediately terminate and each party shall promptly return or destroy all Confidential Information of the other party.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "termination", "text": "In the event of bankruptcy, insolvency, or assignment for the benefit of creditors by either party, the other party may terminate this Agreement immediately upon written notice.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "termination", "text": "Either party may terminate this Agreement for convenience upon providing sixty (60) days advance written notice to the other party.", "source": "CUAD", "risk_level": "Low"},
    {"category": "termination", "text": "This Agreement shall automatically terminate upon the expiration of the Initial Term unless renewed in writing by both parties.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "termination", "text": "Client may terminate any Statement of Work without cause upon ten (10) days notice, provided Client pays for all Services rendered up to the effective termination date.", "source": "LEDGAR", "risk_level": "Low"},

    # Governing Law & Jurisdiction
    {"category": "governing_law", "text": "This Agreement shall be governed by, and construed in accordance with, the laws of the State of California, without giving effect to its conflict of laws principles.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "governing_law", "text": "The parties hereto irrevocably submit to the exclusive jurisdiction of the state and federal courts located in the City of New York, Borough of Manhattan, for any dispute arising out of this Agreement.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "governing_law", "text": "Any dispute, controversy or claim arising under or relating to this contract shall be settled exclusively by confidential arbitration administered by the American Arbitration Association in San Francisco, CA.", "source": "CUAD", "risk_level": "Low"},
    {"category": "governing_law", "text": "This contract shall be construed in accordance with the laws of the State of Delaware, and the parties agree to waive any objection to personal jurisdiction in such courts.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "governing_law", "text": "This Agreement is governed by the laws of England and Wales and each party submits to the exclusive jurisdiction of the English courts.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "governing_law", "text": "The United Nations Convention on Contracts for the International Sale of Goods does not apply to this Agreement.", "source": "LEDGAR", "risk_level": "Low"},

    # Confidentiality
    {"category": "confidentiality", "text": "Each party agrees to maintain the confidentiality of the other party's Proprietary Information with the same degree of care it uses for its own confidential information, but in no event less than reasonable care.", "source": "ContractNLI", "risk_level": "Low"},
    {"category": "confidentiality", "text": "The receiving party shall not disclose, publish, or otherwise disseminate Confidential Information to any third party for a period of five (5) years following the Effective Date without prior written consent.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "confidentiality", "text": "Confidential Information shall not include information that is publicly known at the time of disclosure or becomes publicly known through no wrongful act of the recipient.", "source": "ContractNLI", "risk_level": "Low"},
    {"category": "confidentiality", "text": "Recipient shall have perpetual confidentiality obligations lasting indefinitely beyond the termination of this Agreement.", "source": "CUAD", "risk_level": "Medium"},
    {"category": "confidentiality", "text": "All trade secrets, source code, formulas, and client lists shall remain the strict confidential property of disclosing party.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "confidentiality", "text": "In the event receiving party is legally compelled by court order to disclose any confidential information, it shall provide prompt written notice to the disclosing party.", "source": "LEDGAR", "risk_level": "Low"},

    # Liability & Limitation of Liability
    {"category": "liability", "text": "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR IN CONNECTION WITH THIS AGREEMENT.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "liability", "text": "Each party's aggregate total liability under this Agreement shall be strictly capped at the total amount actually paid by Client to Service Provider in the twelve (12) months preceding the claim.", "source": "CUAD", "risk_level": "Low"},
    {"category": "liability", "text": "Contractor agrees to accept unlimited liability for any direct, indirect, special, or consequential damages resulting from any performance failure under this Agreement.", "source": "CUAD", "risk_level": "High"},
    {"category": "liability", "text": "Neither party shall be liable for aggregate damages exceeding $100,000 USD in connection with any claims arising hereunder.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "liability", "text": "To the maximum extent permitted by applicable law, neither party shall be liable for loss of profits, loss of data, or business interruption.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "liability", "text": "Service Provider disclaims all liability for any damages arising from Client's unauthorized modification of the deliverables.", "source": "LEDGAR", "risk_level": "Low"},

    # Indemnification
    {"category": "indemnification", "text": "Service Provider agrees to indemnify, defend, and hold harmless Client and its officers, directors, and employees against any third-party claims arising from Service Provider's infringement of intellectual property rights.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "indemnification", "text": "Client shall indemnify and hold harmless Vendor against all liabilities, costs, damages, and expenses without limitation arising out of Client's use of the Services.", "source": "CUAD", "risk_level": "High"},
    {"category": "indemnification", "text": "Each party agrees to indemnify the other party from and against claims resulting directly from the indemnifying party's gross negligence or willful misconduct.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "indemnification", "text": "The indemnified party must promptly notify the indemnifying party in writing of any claim and grant sole control of the defense and settlement of such claim.", "source": "CUAD", "risk_level": "Low"},
    {"category": "indemnification", "text": "Vendor shall defend Client against any lawsuit alleging that the software violates any third party copyright or trade secret.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "indemnification", "text": "Indemnification obligations under this section shall survive the termination or expiration of this Agreement.", "source": "LEDGAR", "risk_level": "Medium"},

    # Payment & Fees
    {"category": "payment", "text": "Client shall pay all undisputed invoices within thirty (30) days of receipt. Late payments shall accrue interest at the rate of 1.5% per month or the maximum legal rate.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "payment", "text": "The total contract fee of $120,000 USD shall be paid in four equal quarterly installments of $30,000 USD on the first day of each calendar quarter.", "source": "CUAD", "risk_level": "Low"},
    {"category": "payment", "text": "All payments are non-refundable and due immediately upon execution of this Order Form. Any overdue balance is subject to a 20% immediate liquidated penalty.", "source": "CUAD", "risk_level": "High"},
    {"category": "payment", "text": "Vendor shall invoice Client on a monthly basis for services performed at the hourly rate of $150 USD per hour, payable Net 45 days.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "payment", "text": "All stated prices are exclusive of applicable taxes, customs duties, and value-added tax which shall be borne solely by Client.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "payment", "text": "Client shall make a non-refundable upfront deposit of $25,000 USD upon execution of this Agreement before commencement of work.", "source": "CUAD", "risk_level": "Medium"},

    # Intellectual Property
    {"category": "intellectual_property", "text": "All intellectual property rights, inventions, patents, trademarks, and copyrights developed under this Agreement shall be the sole and exclusive property of Client as work made for hire.", "source": "CUAD", "risk_level": "Low"},
    {"category": "intellectual_property", "text": "Vendor retains all rights, title, and interest in and to its pre-existing materials, background IP, software tools, and underlying methodologies.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "intellectual_property", "text": "Contractor irrevocably assigns and transfers to Company all worldwide rights, titles, and interests in any Work Product created during the engagement.", "source": "CUAD", "risk_level": "Low"},
    {"category": "intellectual_property", "text": "Subject to payment of all applicable fees, Vendor grants Client a non-exclusive, worldwide, royalty-free license to use the Deliverables.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "intellectual_property", "text": "Neither party grants the other any license under any patents, copyrights, or trademarks except as expressly stated herein.", "source": "LEDGAR", "risk_level": "Low"},

    # Dispute Resolution
    {"category": "dispute_resolution", "text": "In the event of any controversy or claim, the parties agree to first attempt good-faith informal negotiation between senior executives before initiating formal legal proceedings.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "dispute_resolution", "text": "If informal negotiation fails within forty-five (45) days, disputes shall be submitted to binding arbitration in accordance with JAMS Comprehensive Arbitration Rules.", "source": "CUAD", "risk_level": "Low"},
    {"category": "dispute_resolution", "text": "EACH PARTY HEREBY EXPRESSLY AND UNCONDITIONALLY WAIVES ANY RIGHT TO TRIAL BY JURY IN ANY LEGAL PROCEEDING ARISING OUT OF THIS AGREEMENT.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "dispute_resolution", "text": "The prevailing party in any arbitration or judicial proceeding shall be entitled to recover its reasonable attorney's fees and litigation costs.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "dispute_resolution", "text": "Disputes shall be resolved through mandatory mediation administered by the American Arbitration Association prior to filing arbitration.", "source": "LEDGAR", "risk_level": "Low"},

    # Warranty
    {"category": "warranty", "text": "Service Provider warrants that the Services will be performed in a professional, workmanlike manner in accordance with prevailing industry standards for a period of ninety (90) days.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "warranty", "text": "EXCEPT AS EXPRESSLY SET FORTH HEREIN, ALL SERVICES AND DELIVERABLES ARE PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "warranty", "text": "Vendor guarantees 99.9% uptime availability for the hosted platform throughout the Term, subject to scheduled maintenance windows.", "source": "CUAD", "risk_level": "Low"},
    {"category": "warranty", "text": "Vendor warrants that the deliverables will be free from material defects and virus or malicious code upon delivery.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "warranty", "text": "Client's sole and exclusive remedy for any breach of warranty shall be the re-performance of the defective Services or refund of fees paid.", "source": "LEDGAR", "risk_level": "Low"},

    # Force Majeure
    {"category": "force_majeure", "text": "Neither party shall be liable or responsible for any failure or delay in performance caused by circumstances beyond its reasonable control, including acts of God, war, pandemic, strike, or power failure.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "force_majeure", "text": "The affected party shall promptly notify the other party in writing within five (5) business days of any Force Majeure event and use diligent efforts to resume performance.", "source": "CUAD", "risk_level": "Low"},
    {"category": "force_majeure", "text": "If a Force Majeure event continues for more than sixty (60) consecutive days, either party may terminate the Agreement upon written notice without penalty.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "force_majeure", "text": "Performance deadlines shall be extended for a period equal to the duration of the Force Majeure interruption.", "source": "LEDGAR", "risk_level": "Low"},

    # Non-Compete / Non-Solicitation
    {"category": "non_compete", "text": "During the term of this Agreement and for twelve (12) months thereafter, neither party shall directly or indirectly solicit or recruit any employee of the other party without prior consent.", "source": "LEDGAR", "risk_level": "Medium"},
    {"category": "non_compete", "text": "Contractor covenants that for a period of five (5) years following termination, Contractor shall not engage in any competing business anywhere in North America or Europe.", "source": "CUAD", "risk_level": "High"},
    {"category": "non_compete", "text": "Vendor agrees not to solicit or hire any direct employees or key contractors of Client for a period of one (1) year following project completion.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "non_compete", "text": "Employee shall not provide direct consulting services to any named competitors of Employer during the course of employment.", "source": "LEDGAR", "risk_level": "Medium"},

    # Miscellaneous / General
    {"category": "miscellaneous", "text": "This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior oral or written agreements.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "miscellaneous", "text": "No amendment or modification of this Agreement shall be valid unless made in writing and duly signed by authorized representatives of both parties.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "miscellaneous", "text": "If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "miscellaneous", "text": "All notices required under this Agreement shall be in writing and delivered by certified mail or reputable overnight courier to the address designated herein.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "miscellaneous", "text": "Neither party may assign or transfer its rights or obligations under this Agreement without the prior written consent of the other party.", "source": "LEDGAR", "risk_level": "Low"},
    {"category": "miscellaneous", "text": "The headings in this Agreement are for convenience of reference only and shall not affect the interpretation of this Agreement.", "source": "LEDGAR", "risk_level": "Low"}
]


def save_curated_dataset(output_dir: str) -> str:
    """Saves the curated clause corpus to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "curated_clause_corpus.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(CURATED_CLAUSES, f, indent=2)
    return out_path


def create_sample_contract_pdf(output_path: str, title: str, sections: List[Tuple[str, str]]) -> str:
    """Generates a clean multi-page PDF contract for testing and evaluation."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = fitz.open()

    page = doc.new_page(width=612, height=792)  # Standard Letter size
    y = 50
    margin_x = 50
    max_width = 512

    # Title
    page.insert_text((margin_x, y), title, fontsize=16, fontname="helv", color=(0.1, 0.1, 0.1))
    y += 35

    for heading, body in sections:
        if y > 700:
            page = doc.new_page(width=612, height=792)
            y = 50
        
        # Section Heading
        page.insert_text((margin_x, y), heading, fontsize=12, fontname="helv", color=(0.15, 0.15, 0.4))
        y += 18

        # Wrap text simply
        words = body.split()
        line = []
        for word in words:
            line.append(word)
            line_str = " ".join(line)
            if len(line_str) > 75:
                page.insert_text((margin_x, y), line_str, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 14
                line = []
                if y > 730:
                    page = doc.new_page(width=612, height=792)
                    y = 50
        if line:
            page.insert_text((margin_x, y), " ".join(line), fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 22

    doc.save(output_path)
    doc.close()
    return output_path


def generate_benchmark_contracts(output_dir: str):
    """Generates sample multi-page contracts for end-to-end evaluation."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Standard Master Services Agreement (MSA) - Multi-Page
    msa_sections = [
        ("1. PARTIES AND RECITALS", 
         "This Master Services Agreement ('Agreement') is entered into as of January 15, 2024 ('Effective Date') by and between Apex Global Solutions Inc., a Delaware corporation located in San Francisco, CA ('Client'), and Quantum Byte Technologies LLC, a California limited liability company ('Service Provider')."),
        ("2. TERM AND DURATION", 
         "The Term of this Agreement shall commence on the Effective Date (January 15, 2024) and shall expire on January 14, 2025, unless earlier terminated in accordance with the provisions herein. The Agreement shall automatically renew for successive twelve (12) month periods unless either party provides written notice of non-renewal at least sixty (60) days prior to the expiration date."),
        ("3. SCOPE OF SERVICES AND COMPENSATION", 
         "Service Provider shall provide cloud infrastructure architecture and AI deployment services. Client agrees to pay Service Provider a total fixed fee of $150,000 USD payable in monthly installments of $12,500 USD Net 30 days upon invoice receipt."),
        ("4. CONFIDENTIALITY OBLIGATIONS", 
         "Each party agrees that all software code, customer data, and financial records disclosed shall constitute Confidential Information. Each party shall preserve the secrecy of such information with reasonable care for five (5) years following disclosure."),
        ("5. INTELLECTUAL PROPERTY RIGHTS", 
         "Client shall own all rights, title, and interest in and to the custom deliverables and work product created by Service Provider under this Agreement. Service Provider retains all rights in its pre-existing tools and background software."),
        ("6. TERMINATION FOR CAUSE AND CONVENIENCE", 
         "Either party may terminate this Agreement for convenience upon sixty (60) days prior written notice. Either party may terminate immediately if the other party commits a material breach and fails to cure such breach within thirty (30) days of receiving written notification."),
        ("7. LIMITATION OF LIABILITY", 
         "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY CONSEQUENTIAL, INDIRECT, SPECIAL, OR PUNITIVE DAMAGES. EACH PARTY'S TOTAL AGGREGATE LIABILITY ARISING OUT OF THIS AGREEMENT SHALL NOT EXCEED THE TOTAL FEES PAID HEREUNDER IN THE PRECEDING TWELVE MONTHS ($150,000 USD)."),
        ("8. INDEMNIFICATION", 
         "Service Provider shall indemnify, defend, and hold harmless Client from any third-party claims alleging that the Deliverables infringe any valid patent, copyright, or trademark."),
        ("9. GOVERNING LAW AND DISPUTE RESOLUTION", 
         "This Agreement shall be governed by and construed in accordance with the laws of the State of California. Any unresolved dispute shall be submitted to confidential binding arbitration administered by JAMS in San Francisco, California."),
        ("10. MISCELLANEOUS PROVISIONS", 
         "This Agreement represents the entire agreement between the parties and supersedes all prior proposals, negotiations, and representations.")
    ]
    pdf_path1 = os.path.join(output_dir, "sample_msa_contract.pdf")
    create_sample_contract_pdf(pdf_path1, "MASTER SERVICES AGREEMENT", msa_sections)

    # 2. High-Risk Contract (Contains Uncapped Liability, Contradictory Dates, Unilateral Clauses)
    high_risk_sections = [
        ("1. PARTIES", 
         "This Consulting Agreement is entered into between SwiftVentures Inc. ('Company') and Nova Advisory LLC ('Consultant')."),
        ("2. TERM AND DATES", 
         "This Agreement is effective as of June 1, 2024. The expiration date shall be January 1, 2024. Project completion date is set for March 15, 2025."),  # Date anomaly!
        ("3. PAYMENT AND PENALTIES", 
         "Company shall pay Consultant $50,000 USD. Any late payment by Company shall incur an immediate 25% non-refundable liquidated damages fee and all amounts are due immediately."),
        ("4. UNILATERAL TERMINATION", 
         "Company reserves the sole and exclusive right to terminate this contract immediately at any time without notice, cause, or compensation to Consultant."),
        ("5. UNLIMITED LIABILITY AND INDEMNITY", 
         "Consultant accepts full, uncapped, and unlimited liability for any and all direct, indirect, consequential, and punitive damages. Consultant shall indemnify Company against all losses without limitation."),
        ("6. NON-COMPETE RESTRICTION", 
         "Consultant covenants not to engage in any competing advisory business worldwide for a period of ten (10) years following termination."),
        ("7. GOVERNING LAW", 
         "This agreement shall be governed by the laws of the State of New York in clause 7, while all litigation must occur in the courts of London, United Kingdom under English law.")  # Contradictory jurisdiction!
    ]
    pdf_path2 = os.path.join(output_dir, "sample_high_risk_contract.pdf")
    create_sample_contract_pdf(pdf_path2, "CONSULTING & RISK AGREEMENT", high_risk_sections)

    return [pdf_path1, pdf_path2]


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    save_curated_dataset(data_dir)
    samples = generate_benchmark_contracts(os.path.join(data_dir, "sample_contracts"))
    print(f"Generated dataset and sample contracts: {samples}")
