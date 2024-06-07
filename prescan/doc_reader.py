import os
import pytesseract as tess
from pdf2image import convert_from_path


class DocReader:
    """
    Reads a PDF (fax) document, performing OCR to determine whether or not the document is a prescription.
    """

    def __init__(self, path_to_file: str):
        self.file_name = path_to_file

    def get_output_file_path(self, batch_name: str, file_name: str):
        """
        Determines the output destination, based on the contents of the document (prescription vs not prescription)
        """
        dir = "presc" if self.is_prescription() else "non-presc"
        output_dir = os.path.join("outputs", batch_name, dir)
        self.ensure_dir_exists(output_dir)
        return os.path.join(output_dir, file_name)

    def ensure_dir_exists(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def is_prescription(self) -> bool:
        """
        Determines whether or not this document corresponds to a prescription
        """
        text = self.extract_text_from_file().lower()
        keywords = [
            "pharmacist",
            "authorize-rx",
            "pharmacy",
            "refill authorization",
            "medscheck",
            "healthwatch",
            "doctor authorization",
            "authorization request",
        ]
        return any(word in text for word in keywords)

    def extract_text_from_file(self) -> str:
        """
        Extract text from the file using Optical Character Recognition.
        This process involves two steps:
        1) converting the PDF file to a series of images
        2) performing OCR on each of the images to extract the text
        """
        pages = []
        try:
            # Convert the PDF file to a list of PIL images:
            images = convert_from_path(self.file_name)
            # Extract text from each image:
            for image in images:
                text = tess.image_to_string(image)
                pages.append(text)
        except Exception as e:
            print(str(e))

        return "\n".join(pages)
