import pdfplumber # pyright: ignore[reportMissingImports]

def read_resume(cv_path):
    text = ""
    with pdfplumber.open(cv_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
