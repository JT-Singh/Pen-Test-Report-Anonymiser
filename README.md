# Pentest Report Anonymiser

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A Python tool designed to **automatically anonymise penetration testing reports (.DOCX)** by masking sensitive infrastructure identifiers, organisation names, domains, emails, and other technical artefacts while **preserving the original document formatting**.

This tool is useful when sharing reports for:

- Training
- Research
- Public disclosure
- Internal knowledge bases
- Conference material
- Anonymised case studies

Sensitive values are replaced using **`x` characters**, preserving the original word length so that report readability and structure remain intact.

---

# Features

## Infrastructure Identifier Masking

Automatically detects and anonymises:

- IP addresses
- URLs
- Domains
- Email addresses
- MAC addresses
- Port references (e.g. `port 443`)

Example:

```
10.10.20.5 → xxxxxxxxx
https://portal.acme.com → xxxxxxxxxxxxxxxxxxxxx
security@acme.com → xxxxxxxxxxxxxxxxx
```

---

## Automatic Organisation Detection (ML-Based)

The tool uses **spaCy Named Entity Recognition (NER)** to detect organisation names automatically.

Examples detected:

```
Acme Corporation
Barclays Bank
Internal AcmeCorp Portal
```

These are automatically anonymised across the report.

---

## Domain Inference

If the tool detects domains such as:

```
portal.acme.com
vpn.acme.local
```

It automatically infers the root organisation keyword:

```
acme
```

All occurrences are masked throughout the document.

---

## Custom Term Masking

You can optionally provide **custom organisation names or keywords** to anonymise.

Example terms:

```
AcmeCorp
InternalPortal
CustomerName
```

Multiple terms can be supplied using the `|` separator.

---

## Full Document Coverage

The anonymiser processes **all parts of a Word document**:

- Body text
- Tables
- Nested tables
- Headers
- Footers

This ensures sensitive identifiers in templates and document metadata are also anonymised.

---

## Formatting Preservation

The script modifies only the **text inside document runs**, ensuring the following remain unchanged:

- Bold text
- Italics
- Underline
- Fonts
- Headings
- Tables
- Layout structure

The anonymised report visually matches the original document.

---

## Batch Processing

The tool processes **all `.docx` files in a folder**.

Example:

Input folder:

```
Report1.docx
Report2.docx
Report3.docx
```

Output:

```
Anonymised_Report1.docx
Anonymised_Report2.docx
Anonymised_Report3.docx
```

---

## Progress Bar

During execution the tool displays a progress indicator.

Example:

```
Anonymising Reports: 60% |██████████        | 3/5 files
```

When finished:

```
Anonymisation complete
```

---

# Installation

## 1. Clone the Repository

```
git clone https://github.com/yourusername/pentest-report-anonymiser.git
cd pentest-report-anonymiser
```

---

## 2. Install Dependencies

```
pip install -r requirements.txt
```

---

## 3. Install the NLP Model

The organisation detection capability requires a spaCy language model.

```
python -m spacy download en_core_web_sm
```

---

# Usage

## Basic Usage

```
python src/pen_test_report_anonymiser.py <folder_path>
```

Example:

```
python src/pen_test_report_anonymiser.py Data/Test_Reports
```

---

## Mask Additional Custom Terms

You can optionally provide custom terms to anonymise.

```
python src/pen_test_report_anonymiser.py <folder_path> "Term1|Term2|Term3"
```

Example:

```
python src/pen_test_report_anonymiser.py Data/Test_Reports "AcmeCorp|InternalPortal|CustomerName"
```

These terms will be masked throughout the report.

---

# Example

## Original Report Text

```
The AcmeCorp VPN gateway vpn.acmecorp.com
was accessible via 10.10.20.5:443.

Contact security@acmecorp.com for remediation.
```

## Anonymised Output

```
The xxxxxxxx VPN gateway xxxxxxxxxxxxxxxx
was accessible via xxxxxxxxxxxx.

Contact xxxxxxxxxxxxxxxxxxxx for remediation.
```

---

# Project Structure

```
pentest-report-anonymiser
│
├── src
│   └── pen_test_report_anonymiser.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# Error Handling

The script includes defensive error handling:

- Invalid folder paths are detected
- Processing errors are reported per file
- The script exits gracefully without crashing

Example:

```
Error processing Report3.docx: <error details>
```

---

# Limitations

Certain identifiers may not always be detected automatically:

- Internal environment identifiers (`ACME_PROD`, `ACME_INT`)
- Uncommon organisation abbreviations
- Proprietary internal system names

These can be addressed using the **custom term masking feature**.

---

# Security Considerations

This tool is intended to anonymise sensitive infrastructure details including:

- Client organisation names
- Internal hostnames
- Domains
- IP addresses
- Email addresses

Always **review anonymised reports manually** before external publication.

---

# License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# Contributing

Contributions are welcome. Possible improvements include:

- Internal hostname detection
- Active Directory domain detection
- Environment detection (PROD / DEV / UAT)
- PDF report support
- CLI packaging
- Automated testing

---

# Disclaimer

This tool is provided **as-is without warranty**.  
Always manually review anonymised reports before sharing externally to ensure that no sensitive information remains.
