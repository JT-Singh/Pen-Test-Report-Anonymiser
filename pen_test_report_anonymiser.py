"""
Advanced DOCX Pentest Report Anonymiser

Features
--------
• Infrastructure identifier masking
• Email masking
• Automatic organisation detection
• Domain inference
• ML-based entity extraction (spaCy NER)
• Custom masking terms
• Header/footer/table processing
• Formatting preservation
• Progress bar
• Graceful error handling
"""

import re
import sys
from pathlib import Path
from docx import Document
from tqdm import tqdm
import spacy


class PentestReportAnonymiser:

    def __init__(self, custom_terms=None):

        # Load spaCy model for entity recognition
        self.nlp = spacy.load("en_core_web_sm")

        self.custom_terms = custom_terms
        self.detected_terms = set()

        self.infrastructure_patterns = self._compile_patterns()

        if custom_terms:
            for term in custom_terms.split("|"):
                self.detected_terms.add(term.strip())

    # ------------------------------------------------

    def _compile_patterns(self):

        return [

            re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),           # IPv4
            re.compile(r'https?://[^\s]+'),                       # URL
            re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b'),  # email
            re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'),  # domain
            re.compile(r'\bport\s+\d{1,5}\b', re.IGNORECASE),     # port
            re.compile(r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b') # MAC
        ]

    # ------------------------------------------------

    def _mask(self, text):

        return "x" * len(text)

    # ------------------------------------------------
    # TEXT EXTRACTION PHASE
    # ------------------------------------------------

    def extract_all_text(self, doc):

        text_blocks = []

        for p in doc.paragraphs:
            text_blocks.append(p.text)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        text_blocks.append(p.text)

        for section in doc.sections:

            for p in section.header.paragraphs:
                text_blocks.append(p.text)

            for p in section.footer.paragraphs:
                text_blocks.append(p.text)

        return text_blocks

    # ------------------------------------------------
    # ORGANISATION DETECTION
    # ------------------------------------------------

    def detect_organisations(self, text_blocks):

        for text in text_blocks:

            doc = self.nlp(text)

            for ent in doc.ents:
                if ent.label_ == "ORG":
                    self.detected_terms.add(ent.text)

    # ------------------------------------------------
    # DOMAIN INFERENCE
    # ------------------------------------------------

    def detect_domains(self, text_blocks):

        domain_pattern = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')

        for text in text_blocks:

            matches = domain_pattern.findall(text)

            for domain in matches:

                self.detected_terms.add(domain)

                root = domain.split(".")[0]

                if len(root) > 3:
                    self.detected_terms.add(root)

    # ------------------------------------------------
    # APPLY ANONYMISATION
    # ------------------------------------------------

    def anonymise_text(self, text):

        # Infrastructure masking

        for pattern in self.infrastructure_patterns:

            text = pattern.sub(lambda m: self._mask(m.group()), text)

        # Organisation masking

        for term in sorted(self.detected_terms, key=len, reverse=True):

            pattern = re.compile(re.escape(term), re.IGNORECASE)

            text = pattern.sub(lambda m: self._mask(m.group()), text)

        return text

    # ------------------------------------------------

    def process_runs(self, paragraph):

        for run in paragraph.runs:

            if run.text:

                run.text = self.anonymise_text(run.text)

    # ------------------------------------------------

    def process_paragraphs(self, paragraphs):

        for paragraph in paragraphs:

            self.process_runs(paragraph)

    # ------------------------------------------------

    def process_tables(self, tables):

        for table in tables:

            for row in table.rows:

                for cell in row.cells:

                    self.process_paragraphs(cell.paragraphs)

                    self.process_tables(cell.tables)

    # ------------------------------------------------

    def process_headers_footers(self, doc):

        for section in doc.sections:

            self.process_paragraphs(section.header.paragraphs)

            self.process_tables(section.header.tables)

            self.process_paragraphs(section.footer.paragraphs)

            self.process_tables(section.footer.tables)

    # ------------------------------------------------

    def anonymise_doc(self, file_path):

        try:

            doc = Document(file_path)

            # ------------------------------
            # Phase 1: detection
            # ------------------------------

            text_blocks = self.extract_all_text(doc)

            self.detect_organisations(text_blocks)

            self.detect_domains(text_blocks)

            # ------------------------------
            # Phase 2: masking
            # ------------------------------

            self.process_paragraphs(doc.paragraphs)

            self.process_tables(doc.tables)

            self.process_headers_footers(doc)

            output = file_path.parent / f"Anonymised_{file_path.name}"

            doc.save(output)

        except Exception as e:

            print(f"Error processing {file_path.name}: {e}")

    # ------------------------------------------------

    def process_folder(self, folder):

        folder = Path(folder)

        if not folder.exists():

            print("Invalid folder path provided.")

            return

        files = [f for f in folder.glob("*.docx") if not f.name.startswith("Anonymised_")]

        if not files:

            print("No DOCX files found.")

            return

        for file in tqdm(files, desc="Anonymising Reports", unit="file"):

            self.anonymise_doc(file)

        print("\nAnonymisation complete")

# ------------------------------------------------

def main():

    if len(sys.argv) < 2:

        print(
            "Usage:\n"
            "python anonymiser.py <folder_path>\n"
            "python anonymiser.py <folder_path> \"Term1|Term2\""
        )

        return

    folder = sys.argv[1]

    custom_terms = None

    if len(sys.argv) >= 3:
        custom_terms = sys.argv[2]

    anonymiser = PentestReportAnonymiser(custom_terms)

    anonymiser.process_folder(folder)


if __name__ == "__main__":
    main()
