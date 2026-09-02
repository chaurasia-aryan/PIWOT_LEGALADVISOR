"""
PIWOT Legal Advisor — Legal Named Entity & Key Information Extraction (NER/KEI) Service
Comprehensive extraction supporting multi-currency (USD, INR, Rs., EUR, GBP), Indian & Western
numeric patterns, interest/penalty percentages, loan facilities, and ISO date normalization.
"""

import re
import datetime
from typing import Dict, List, Any, Optional

MONTH_MAP = {
    'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
    'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
    'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
    'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
}


def normalize_to_iso_date(date_str: str) -> Optional[str]:
    """Converts diverse date strings (e.g. 'January 15, 2024', '15th Jan 2024', '2024-01-15') to ISO 'YYYY-MM-DD'."""
    if not date_str:
        return None
    
    clean = re.sub(r'(st|nd|rd|th)', '', date_str, flags=re.IGNORECASE).strip()

    # Pattern: Month DD, YYYY or Month DD YYYY
    m1 = re.search(r'([A-Za-z]+)\s+([0-9]{1,2})[,\s]+([0-9]{4})', clean)
    if m1:
        month_name = m1.group(1).lower()
        if month_name in MONTH_MAP:
            m = MONTH_MAP[month_name]
            d = int(m1.group(2))
            y = int(m1.group(3))
            try:
                return datetime.date(y, m, d).isoformat()
            except ValueError:
                pass

    # Pattern: DD Month YYYY
    m2 = re.search(r'([0-9]{1,2})\s+([A-Za-z]+)[,\s]+([0-9]{4})', clean)
    if m2:
        month_name = m2.group(2).lower()
        if month_name in MONTH_MAP:
            m = MONTH_MAP[month_name]
            d = int(m2.group(1))
            y = int(m2.group(3))
            try:
                return datetime.date(y, m, d).isoformat()
            except ValueError:
                pass

    # Pattern: YYYY-MM-DD
    m3 = re.search(r'([0-9]{4})[-/]([0-9]{1,2})[-/]([0-9]{1,2})', clean)
    if m3:
        try:
            return datetime.date(int(m3.group(1)), int(m3.group(2)), int(m3.group(3))).isoformat()
        except ValueError:
            pass

    # Pattern: DD/MM/YYYY
    m4 = re.search(r'([0-9]{1,2})[-/]([0-9]{1,2})[-/]([0-9]{4})', clean)
    if m4:
        try:
            d_val = int(m4.group(1))
            m_val = int(m4.group(2))
            y_val = int(m4.group(3))
            if m_val > 12 >= d_val:
                d_val, m_val = m_val, d_val
            return datetime.date(y_val, m_val, d_val).isoformat()
        except ValueError:
            pass

    return date_str


class LegalEntityExtractor:
    """Extracts structured legal metadata from full contract text with global and Indian legal support."""

    def __init__(self):
        # Comprehensive currency patterns: USD, INR, Rs., Rupees, Lakhs, Crores, EUR, GBP
        self.money_pattern = re.compile(
            r'(?:(?:Rs\.?|INR|₹|USD|\$|EUR|€|GBP|£)\s*[\d,]+(?:\.\d+)?(?:\s*(?:Lakhs?|Crores?|Million|Billion|k|thousand|mn|cr|lakh))?|'
            r'[\d,]+(?:\.\d+)?\s*(?:USD|INR|EUR|GBP|Rupees?|Lakhs?|Crores?|dollars?)|'
            r'Rupees\s+[A-Za-z\s\-]+(?:\([0-9,]+\))?|'
            r'sum\s+of\s+(?:Rs\.?|INR|\$)?\s*[\d,]+(?:\.\d+)?)',
            re.IGNORECASE
        )

        self.party_pattern = re.compile(
            r'(?:between|by and between|entered into by|among)\s+([A-Z][A-Za-z0-9\s\,\.\&\-\(\)\/]{3,70}?)\s*(?:\([^\)]*?\))?\s*(?:,|and|\&)\s+([A-Z][A-Za-z0-9\s\,\.\&\-\(\)\/]{3,70}?)(?:\s*\(|\s*\.|\s*\,|\s+each|\s+collectively|\s+hereinafter)',
            re.IGNORECASE
        )

        self.jurisdiction_pattern = re.compile(
            r'(?:laws of|governed by the laws of|governed by and construed in accordance with the laws of|subject to the exclusive jurisdiction of the courts (?:in|at|of))\s+(?:the\s+)?(State of\s+[A-Za-z\s]+|Commonwealth of\s+[A-Za-z\s]+|[A-Za-z\s]+?)(?:[,\.\;]|\s+without|\s+and)',
            re.IGNORECASE
        )

        self.venue_pattern = re.compile(
            r'(?:courts (?:located )?(?:in|at)|jurisdiction of the\s+[a-z\s]*courts (?:in|at)|arbitration (?:administered by|at|in))\s+([A-Za-z0-9\s\,\.]{3,60}?)(?:[,\.\;]|\s+for any|\s+and)',
            re.IGNORECASE
        )

        self.notice_period_pattern = re.compile(
            r'([0-9]+|\b(?:ten|fifteen|twenty|thirty|sixty|ninety)\b)\s*(?:\([0-9]+\))?\s*(?:calendar\s+|business\s+)?(?:days|months)(?:\s+prior|\s+advance)?\s*written\s+notice',
            re.IGNORECASE
        )

        self.penalty_percent_pattern = re.compile(
            r'([0-9]+(?:\.[0-9]+)?\s*\%(?:\s*(?:p\.a\.|per annum|per month|interest|penal interest|penalty|liquidated damages|margin))?)',
            re.IGNORECASE
        )

        self.date_phrase_pattern = re.compile(
            r'(?:Effective Date|Sanction Date|Agreement Date|expiration date|commence(?:s)? on|expire(?:s)? on|shall expire on|shall commence on|effective as of|entered into as of|dated as of|dated|valid until|valid through|completion date)\s*(?:is|shall be|will be|is set for|set for|\:|\=|\'|\"|\s)?\s*([A-Za-z]+\s+[0-9]{1,2}[,\s]+[0-9]{4}|[0-9]{1,2}(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?[A-Za-z]+[,\s]+[0-9]{4}|[0-9]{4}[-/][0-9]{1,2}[-/][0-9]{1,2}|[0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{4})',
            re.IGNORECASE
        )

    def extract_parties(self, text: str) -> List[Dict[str, str]]:
        """Extracts contracting party names (Borrower, Lender, Bank, Client, Vendor)."""
        parties = []
        
        # 1. Search for Loan / Banking specific parties: 'Borrower', 'Lender', 'Bank'
        bank_match = re.search(r'([A-Z][A-Za-z0-9\s\.\,\&]{3,50}?(?:Bank|Financial Services|Finance|Capital|Lender|Corporation))\s*(?:\([^\)]*?\))?\s*(?:referred to as|called|hereinafter)?\s*(?:\'|\")?(?:the\s+)?(Bank|Lender|Client|Company)(?:\'|\")?', text, re.IGNORECASE)
        borrower_match = re.search(r'([A-Z][A-Za-z0-9\s\.\,\&]{3,50}?(?:Enterprises|Pvt|Private|Limited|Ltd|LLC|Inc|Corporation|Borrower))\s*(?:\([^\)]*?\))?\s*(?:referred to as|called|hereinafter)?\s*(?:\'|\")?(?:the\s+)?(Borrower|Co-Borrower|Contractor|Customer)(?:\'|\")?', text, re.IGNORECASE)

        if bank_match and len(bank_match.group(1).strip()) > 3:
            parties.append({"name": bank_match.group(1).strip(" ,.-"), "role": f"Lender / {bank_match.group(2).strip()}"})
        if borrower_match and len(borrower_match.group(1).strip()) > 3:
            parties.append({"name": borrower_match.group(1).strip(" ,.-"), "role": f"Borrower / {borrower_match.group(2).strip()}"})

        # 2. Standard general pattern fallback
        if not parties:
            m = self.party_pattern.search(text)
            if m:
                p1 = m.group(1).strip(" ,.-")
                p2 = m.group(2).strip(" ,.-")
                if len(p1) > 3 and not p1.lower().startswith("this"):
                    parties.append({"name": p1, "role": "Party 1 / Client"})
                if len(p2) > 3 and not p2.lower().startswith("this"):
                    parties.append({"name": p2, "role": "Party 2 / Contractor / Provider"})

        if not parties:
            named_entities = re.findall(r'([A-Z][A-Za-z0-9\s\.\,\&]{3,40}?)\s*\((?:\'|\")([A-Za-z\s]{3,25})(?:\'|\")\)', text)
            for entity_name, role_name in named_entities[:2]:
                if len(entity_name.strip()) > 3 and entity_name.strip() not in [p["name"] for p in parties]:
                    parties.append({"name": entity_name.strip(), "role": role_name.strip()})

        if not parties:
            parties.append({"name": "Borrower / Commercial Entity", "role": "Party 1"})
            parties.append({"name": "Bank / Lending Institution", "role": "Party 2"})

        return parties

    def extract_dates(self, text: str) -> Dict[str, Any]:
        """Extracts and normalizes effective date, expiry date, and notice periods."""
        results = {
            "effective_date": None,
            "expiry_date": None,
            "notice_period": None,
            "raw_dates_found": []
        }

        for match in self.date_phrase_pattern.finditer(text):
            phrase = match.group(0).lower()
            date_raw = match.group(1)
            iso_date = normalize_to_iso_date(date_raw)

            if any(k in phrase for k in ["effective", "sanction", "agreement date", "commence", "entered into", "as of", "dated"]):
                if not results["effective_date"]:
                    results["effective_date"] = iso_date
            elif any(k in phrase for k in ["expir", "completion", "end", "terminate on", "valid through", "valid until"]):
                if not results["expiry_date"]:
                    results["expiry_date"] = iso_date

            results["raw_dates_found"].append({"raw": date_raw, "iso": iso_date})

        np_match = self.notice_period_pattern.search(text)
        if np_match:
            period_val = np_match.group(1).lower()
            word_num_map = {'ten': '10', 'fifteen': '15', 'twenty': '20', 'thirty': '30', 'sixty': '60', 'ninety': '90'}
            digit_val = word_num_map.get(period_val, period_val)
            results["notice_period"] = f"{digit_val} days written notice"

        return results

    def extract_financials(self, text: str) -> Dict[str, Any]:
        """Extracts monetary values, interest rates, penalty percentages, and payment schedules."""
        raw_amounts = self.money_pattern.findall(text)
        percentages = self.penalty_percent_pattern.findall(text)

        cleaned_amounts = []
        for a in raw_amounts:
            a_str = re.sub(r'\s+', ' ', a).strip(" ,.-;")
            # Filter out non-monetary or tiny noise
            if len(a_str) > 2 and a_str not in cleaned_amounts:
                cleaned_amounts.append(a_str)

        cleaned_percentages = []
        for p in percentages:
            p_str = re.sub(r'\s+', ' ', p).strip(" ,.-;")
            if len(p_str) > 1 and p_str not in cleaned_percentages:
                cleaned_percentages.append(p_str)

        # Inferred payment & loan terms
        payment_terms = []
        if re.search(r'Net\s*(?:15|30|45|60|90)', text, re.IGNORECASE):
            m = re.search(r'(Net\s*(?:15|30|45|60|90)(?:\s*days)?)', text, re.IGNORECASE)
            if m:
                payment_terms.append(m.group(1))
        if re.search(r'monthly\s+installments|equated\s+monthly\s+installments|emi|quarterly\s+installments', text, re.IGNORECASE):
            m = re.search(r'((?:equated\s+monthly\s+installments|monthly\s+installments|emi|quarterly\s+installments))', text, re.IGNORECASE)
            if m:
                payment_terms.append(m.group(1).upper())
        if re.search(r'Schedule\s+I', text, re.IGNORECASE):
            payment_terms.append("As specified in Schedule I (Facility Schedule)")

        # Loan tenure search (e.g. 36 months, 5 years)
        tenure_match = re.search(r'(?:tenure|term|repayment\s+period)\s*(?:of|is|\:)?\s*([0-9]+\s*(?:months|years|installments))', text, re.IGNORECASE)
        if tenure_match:
            payment_terms.append(f"Tenure: {tenure_match.group(1)}")

        return {
            "monetary_amounts": cleaned_amounts[:10],
            "penalties_percentages": cleaned_percentages[:6],
            "payment_terms": payment_terms if payment_terms else ["Standard Commercial Payment Terms"]
        }

    def extract_legal_context(self, text: str) -> Dict[str, Any]:
        """Extracts governing law jurisdictions and arbitration venues."""
        jurisdictions = []
        venues = []

        for m in self.jurisdiction_pattern.finditer(text):
            j = m.group(1).strip(" ,.;")
            if len(j) > 2 and j not in jurisdictions and not j.lower().startswith("the"):
                jurisdictions.append(j)

        for m in self.venue_pattern.finditer(text):
            v = m.group(1).strip(" ,.;")
            if len(v) > 2 and v not in venues and not v.lower().startswith("any"):
                venues.append(v)

        return {
            "governing_jurisdictions": jurisdictions if jurisdictions else ["State / High Court Jurisdiction"],
            "dispute_venues": venues if venues else ["Commercial Court / Arbitration Venue"]
        }

    def extract_all_entities(self, text: str) -> Dict[str, Any]:
        """Runs full entity and key information extraction."""
        parties = self.extract_parties(text)
        dates = self.extract_dates(text)
        financials = self.extract_financials(text)
        legal_ctx = self.extract_legal_context(text)

        return {
            "parties": parties,
            "effective_date": dates["effective_date"],
            "expiry_date": dates["expiry_date"],
            "notice_period": dates["notice_period"],
            "monetary_amounts": financials["monetary_amounts"],
            "percentages": financials["penalties_percentages"],
            "payment_terms": financials["payment_terms"],
            "governing_jurisdiction": legal_ctx["governing_jurisdictions"][0] if legal_ctx["governing_jurisdictions"] else "Applicable Commercial Jurisdiction",
            "all_jurisdictions": legal_ctx["governing_jurisdictions"],
            "dispute_venues": legal_ctx["dispute_venues"]
        }
