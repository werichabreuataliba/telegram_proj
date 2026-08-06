from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_core.documents import Document

from ChatBOT.DocumentProcessing.OCRProcessor import OCRProcessor

class DocumentProcessor:

    def __init__(self):
        self.ocr = None

    def load(self, file_path):

        if file_path.endswith(".pdf"):

            return self.load_pdf(file_path)

        return self.load_text(file_path)

    def load_text(self, file_path):

        loader = TextLoader(
            file_path,
            encoding="utf-8"
        )

        return loader.load()

    def load_pdf(self, file_path):

        loader = PyPDFLoader(
            file_path
        )

        documents = loader.load()

        texto = ""

        for doc in documents:

            texto += doc.page_content

        #
        # Existe texto suficiente?
        #
        if len(texto.strip()) > 100:

            print("PDF contém texto.")

            return documents

        print("PDF escaneado.")

        if self.ocr is None:
            self.ocr = OCRProcessor()

        texto = self.ocr.extract_text(
            file_path
        )

        return [
            Document(
                page_content=texto
            )
        ]