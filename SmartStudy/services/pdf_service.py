
import pymupdf


def extract_pdf_text(pdf_bytes: bytes) -> dict:
    MAX_FILE_SIZE = 100 * 1024 * 1024

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise ValueError("PDF exceeds the 100 MB size limit.")

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("The uploaded file is not a valid PDF.")
    
    pages = []
    document = None

    try:
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

        full_text = "\n\n".join(
            page["text"]
            for page in pages
            if page["text"]
        )

        return {
            "page_count": len(document),
            "pages": pages,
            "full_text": full_text,
            "has_text": bool(full_text.strip())
        }

    finally:
        if document is not None:
            document.close()
