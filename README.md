

# PDF Rectangle Tool

This Python application allows you to open a PDF file, visually draw rectangles on a page, move them interactively, and get their exact positions in PDF coordinates.

It’s useful for:
- Selecting regions of interest (ROI) in a PDF
- Manual labeling or annotation prep
- Planning out clear zones in of addresses and other controls

---

## 📦 Features

- Load and display the **first page** of a PDF
- **Draw** rectangles by click-drag
- **Move** existing rectangles by clicking and dragging them
- Each rectangle has a **vivid color**
- The color-coded coordinates are printed to the terminal
- Scales PDF to fit screen for easy viewing

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/yourname/pdf-rectangle-tool.git
cd pdf-rectangle-tool

## 2. Install dependencies
pip install -r requirements.txt
```
### 3. Run the application

```bash
python pdf_rectangle_tool.py path/to/your/file.pdf
```
### 4. Interact with the PDF
- **Draw rectangles**: Click and drag to create a rectangle.
- **Move rectangles**: Click and drag an existing rectangle to reposition it.
- **View coordinates**: The terminal will print the coordinates of each rectangle in PDF units.

