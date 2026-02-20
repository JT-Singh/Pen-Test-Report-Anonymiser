
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

# Penetration Test Report Anonymiser


A production-ready Python tool for anonymising infrastructure identifiers in penetration testing DOCX reports while preserving CVE IDs and original document formatting.

Designed for professional security consulting, red team reporting, and secure report sharing.

## Overview

This tool processes Microsoft Word .docx penetration testing reports and masks infrastructure identifiers such as:

* IPv4 addresses
* URLs
* Email addresses
* MAC addresses
* Port numbers
* Hostnames and internal domains

All matched values are replaced with "x" characters of equal length to preserve formatting and alignment.

CVE identifiers are intentionally preserved to maintain technical clarity.

## Key Features

* Operates at Word run level to retain formatting
* Preserves:
    * Bold, italic, underline
    * Headings and lists
    * Table structure
    * Nested tables
    * Headers and footers
    * Skips already anonymised files
    * Displays progress bar during batch processing
    * Graceful error handling
    * Clean CLI interface


## Installation
1. Clone Repository
```bash
git clone https://github.com/<your-username>/Pen-Test-Report-Anonymiser.git
cd Pen-Test-Report-Anonymiser
```
2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
## Usage
```bash
python pen_test_report_anonymiser.py <folder_path>
```

Example:
```bash
python pen_test_report_anonymiser.py ./reports
```
Output:
* Creates `Anonymised_<original_filename>.docx`
* Shows live progress bar
* Prints Anonymisation complete when finished

## Example
Original
```
The internal server 10.10.14.23 was accessible on port 8443.
Access confirmed via https://internal.company.local/login.
The system is vulnerable to CVE-2023-12345.
```
Anonymised
```
The internal server xxxxxxxxxxxxx was accessible on xxxx xxxxx.
Access confirmed via xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
The system is vulnerable to CVE-2023-12345.
```
## Project Structure
```
Pen-Test-Report-Anonymiser/
│
├── pen_test_report_anonymiser.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```
## Continuous Integration (CI)

This repository supports GitHub Actions for automated validation.

### Example CI Workflow

Create .github/workflows/python-ci.yml
```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint check (optional)
        run: |
          pip install flake8
          flake8 docx_anonymiser.py || true
```
This ensures:
* Multi-version compatibility
* Dependency validation
* Optional linting

## Security Considerations

This tool:
* Masks technical infrastructure identifiers
* Preserves vulnerability references
* Does not perform narrative redaction
* Does not detect organisation names
* Does not process embedded images
Always conduct manual review before external publication.

## Versioning

This project follows semantic versioning.

Example:
```
v1.0.0
```
Tag a release:
```
git tag v1.0.0
git push origin v1.0.0
```
## Contributing

1. Create a feature branch:
```bash
git checkout -b feature/improvement-name
```
2. Commit changes:
```bash
git commit -m "Improve hostname masking logic"
```
3. Push and open Pull Request.

## Roadmap

Potential future enhancements:
* Configurable masking policy
* Pseudonym mapping instead of masking
* OCR for embedded screenshots
* SmartArt and shapes processing
* Structured logging and audit trail
* Packaging as installable CLI tool

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Maintainer Notes

Designed for:
* Security consultancies
* Red team operators
* Cyber assurance teams
* Internal security functions

This tool is intended to support controlled disclosure workflows, not replace formal information classification review.
