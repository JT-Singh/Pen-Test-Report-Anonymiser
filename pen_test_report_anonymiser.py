"""
DOCX Penetration Test Report Anonymiser

Purpose:
    Anonymise infrastructure identifiers in penetration testing DOCX reports
    while preserving CVE identifiers and document formatting.

Key Design Principles:
    - Preserve document structure and styling
    - Preserve CVE IDs for technical integrity
    - Mask infrastructure identifiers with 'x'
    - Process documents safely and gracefully
    - Maintain readability and maintainability

Author: <Your Name>
Version: 1.0
"""

import re
import sys
from pathlib import Path
from docx import Document
from tqdm import tqdm


class DocxPentestAnonymiser:
    """
    Core anonymiser class responsible for:

    1. Defining sensitive infrastructure patterns
    2. Replacing matched values with masked characters
    3. Traversing DOCX document structure safely
    4. Preserving formatting by operating at run level
    """

    def __init__(self):
        """
        Initialise anonymiser and compile regex patterns once.
        Compiling once improves performance when processing multiple documents.
        """
        self.patterns = self._compile_patterns()

    def _compile_patterns(self):
        """
        Compile regex patterns for infrastructure identifiers.

        IMPORTANT:
        - CVE IDs are intentionally NOT included.
        - Patterns are designed to match infrastructure data only.
        """
        return [
            # IPv4 addresses (e.g. 192.168.1.10)
            re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),

            # URLs (http or https)
            re.compile(r'\bhttps?://[^\s]+'),

            # Email addresses
            re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'),

            # MAC addresses (e.g. AA:BB:CC:DD:EE:FF)
            re.compile(r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b'),

            # Port numbers referenced as "port 443"
            re.compile(r'\bport\s+\d{1,5}\b', re.IGNORECASE),

            # Hostnames and domains (e.g. internal.company.local)
            re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
        ]

    def _mask_match(self, match):
        """
        Replace matched string with 'x' characters
        equal in length to original match.

        This preserves layout alignment and readability.
        """
        return "x" * len(match.group())

    def anonymise_text(self, text):
        """
        Apply all infrastructure masking patterns
        to a block of text.

        Order matters:
        Patterns are applied sequentially.
        """
        for pattern in self.patterns:
            text = pattern.sub(self._mask_match, text)
        return text

    def _process_runs(self, paragraph):
        """
        Process individual runs inside a paragraph.

        Why runs?
        Word stores formatting (bold, italic, underline)
        at the run level.

        Replacing paragraph.text destroys formatting.
        Therefore we modify run.text only.
        """
        for run in paragraph.runs:
            if run.text:
                run.text = self.anonymise_text(run.text)

    def _process_paragraphs(self, paragraphs):
        """
        Iterate through all paragraphs and process
        each one at run level.
        """
        for paragraph in paragraphs:
            self._process_runs(paragraph)

    def _process_tables(self, tables):
        """
        Recursively process tables.

        Word tables may contain:
            - Paragraphs
            - Nested tables

        This method ensures deep traversal.
        """
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    self._process_paragraphs(cell.paragraphs)
                    self._process_tables(cell.tables)

    def _process_headers_footers(self, doc):
        """
        Process headers and footers in each section.

        Penetration test reports often contain:
            - Confidential banners
            - Client names
            - System references

        These must also be anonymised.
        """
        for section in doc.sections:
            self._process_paragraphs(section.header.paragraphs)
            self._process_tables(section.header.tables)

            self._process_paragraphs(section.footer.paragraphs)
            self._process_tables(section.footer.tables)

    def anonymise_docx(self, file_path):
        """
        Perform anonymisation on a single DOCX file.

        Steps:
            1. Load document
            2. Process paragraphs
            3. Process tables
            4. Process headers/footers
            5. Save anonymised copy
        """
        try:
            doc = Document(file_path)

            # Main body
            self._process_paragraphs(doc.paragraphs)
            self._process_tables(doc.tables)

            # Headers and footers
            self._process_headers_footers(doc)

            # Save new file with prefix
            new_file_name = f"Anonymised_{file_path.name}"
            new_file_path = file_path.parent / new_file_name

            doc.save(new_file_path)

        except Exception as e:
            # Do not crash entire batch if one file fails
            print(f"\nError processing {file_path.name}: {e}")

    def process_folder(self, folder_path):
        """
        Process all eligible DOCX files within a folder.

        Behaviour:
            - Skips already anonymised files
            - Displays progress bar
            - Handles unexpected errors gracefully
        """
        folder = Path(folder_path)

        if not folder.exists() or not folder.is_dir():
            print("Invalid folder path provided.")
            return

        # Collect target files
        files = [
            f for f in folder.iterdir()
            if f.is_file()
            and f.suffix.lower() == ".docx"
            and not f.name.startswith("Anonymised_")
        ]

        if not files:
            print("No DOCX reports found.")
            return

        try:
            # tqdm provides visual percentage completion
            for file in tqdm(files, desc="Anonymising DOCX reports", unit="file"):
                self.anonymise_docx(file)

            print("\nAnonymisation complete")

        except KeyboardInterrupt:
            print("\nProcess interrupted by user.")

        except Exception as e:
            print(f"\nUnexpected error occurred: {e}")


def main():
    """
    CLI entry point.

    Usage:
        python docx_anonymiser.py <folder_path>
    """
    if len(sys.argv) != 2:
        print("Usage: python docx_anonymiser.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    anonymiser = DocxPentestAnonymiser()
    anonymiser.process_folder(folder_path)


if __name__ == "__main__":
    main()