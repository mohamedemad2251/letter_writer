# Letter Writer

**Letter Writer** is a customizable Odoo module that allows users to generate and manage templated letters or emails within the Odoo backend. It supports dynamic placeholders, relationships with employees and partners, and export options including PDF and Word formats.

---

## ✨ Features

- Create and manage reusable letter templates.
- Insert dynamic placeholders like:
  - `**partner**`
  - `**employee**`
  - `**sender**`
- Select a partner and employee per letter.
- Download letters as:
  - 📄 PDF (via QWeb report)
  - 📝 Word document (via `python-docx`)
- Simple, clean editor interface.
- Extended via the `letter_base` abstract module.
- Can be extended even further using `letter_(module_name)` (Note that it'd be required to make a seperate directory inside the addons/ that is a sibling directory)

---

## 📦 Dependencies

- Odoo 18
- Python package: `html2docx` (and its dependencies)
- Required module: `letter_base` (custom module)

---

## ⚙️ Installation

### 1. Place the modules

Make sure both `letter_writer` and `letter_base` are inside your Odoo `addons/` directory.

### 2. Install Python dependency

Install the required Python package manually:

```bash
pip install -r requirements.txt
```

---
## NOTE

1. The module will NOT work if the dependency is not installed.
2. Make sure you follow the hierarchy of relative path when adding the modules
3. Installing "Letter Writer" from the Apps window on Odoo automatically installs "Letter Writer - Base"