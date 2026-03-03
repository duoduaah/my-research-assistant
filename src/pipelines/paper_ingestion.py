import requests
import PyPDF2
from io import BytesIO


class PaperIngestionService:
    def __init__(self, timeout=10):
        self.timeout = timeout

    """
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

    """


    def extract_text_from_pdf_url(self, url):
        """
        Download and extract text from a PDF URL.
        
        Args:
            url (str): The PDF URL
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Download the PDF
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Create a BytesIO object from the PDF content
            pdf_file = BytesIO(response.content)
            
            # Read the PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF: {e}")
            return None
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return None


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
            pdf_text = self.extract_text_from_pdf_url(url)
            #with self._download_pdf(url) as pdf_file:
            #    raw_text = self._extract_text(pdf_file)
            #    cleaned_text = self._clean_text(raw_text)
            cleaned_text = self._clean_text(pdf_text)
            return cleaned_text
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to download the PDF from the URL: {url}. Error: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while processing the PDF: {paper['id']}. Error: {e}")

    
