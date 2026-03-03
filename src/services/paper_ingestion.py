import requests
import tempfile
from pypdf import PdfReader

class PaperIngestionService:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def _download_pdf(self, url):
        headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/pdf"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Check if the content type is PDF
        if "application/pdf" not in response.headers.get("Content-Type", ""):
            print(f"Skipping non-PDF file: {url}")
            return None

        tmp = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")
        tmp.write(response.content)
        tmp.flush() #memory to disk
        return tmp
    
    def _extract_text(self, pdf_file):
        reader = PdfReader(pdf_file)
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages)


    def _clean_text(self, text):
        """  
        Cleans text, removes empty lines
        :param text: str text
        """
        splitted = text.splitlines()
        cleaned = []
        for line in splitted:
            stripped = line.strip()
            if not stripped:
                continue
            cleaned.append(stripped)

        return "\n".join(cleaned)


    def get_text(self, paper):
        """
        Docstring for get_text
        :param paper: dict containing at least 'pdf_url'
        """
        try:
            url = paper.get("pdf_url")
            with self._download_pdf(url) as pdf_file:
                raw_text = self._extract_text(pdf_file)
                cleaned_text = self._clean_text(raw_text)
                return cleaned_text
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to download the PDF from the URL: {url}. Error: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while processing the PDF: {paper['id']}. Error: {e}")

    
