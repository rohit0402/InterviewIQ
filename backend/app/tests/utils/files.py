from pathlib import Path

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"

def pdf_file():
    return open(FIXTURE_DIR / "sample.pdf", "rb")

def text_file():
    return open(FIXTURE_DIR / "sample.txt", "rb")