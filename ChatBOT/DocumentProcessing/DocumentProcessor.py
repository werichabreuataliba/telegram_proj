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
        texto = "\n".join(doc.page_content for doc in documents)

        print("========== TEXTO EXTRAÍDO ==========", flush=True)
        print(texto, flush=True)
        print("========== FIM TEXTO EXTRAÍDO ==========", flush=True)

        # Verifica se o texto extraído parece estar incompleto
        campos_importantes = [
            "NOME:",
            "IDADE:",
            "FUNÇÃO:",
            "EMPRESA:"
        ]

        texto_incompleto = sum(
            campo not in texto.upper()
            for campo in campos_importantes
        ) >= 2

        if texto_incompleto:
            print("PDF -> texto aparentemente incompleto.", flush=True)
            print("PDF -> será necessário OCR.", flush=True)

            if self.ocr is None:
                self.ocr = OCRProcessor()
            # Aqui chamamos seu OCRProcessor
            texto_ocr = self.ocr.extract_text(file_path)

            print("========== TEXTO OCR ==========", flush=True)
            print(texto_ocr, flush=True)
            print("========== FIM TEXTO OCR ==========", flush=True)

            documents = [
                Document(page_content=texto_ocr)
            ]

        else:
            print("PDF -> texto aparentemente completo.", flush=True)

        return documents

        # texto = ""
        #
        # for doc in documents:
        #
        #     texto += doc.page_content
        #
        # #
        # # Existe texto suficiente?
        # #
        # if len(texto.strip()) > 100:
        #
        #     print("PDF contém texto.")
        #
        #     return documents
        #
        # print("PDF escaneado.")
        #
        # if self.ocr is None:
        #     self.ocr = OCRProcessor()
        #
        # texto = self.ocr.extract_text(
        #     file_path
        # )
        #
        # return [
        #     Document(
        #         page_content=texto
        #     )
        # ]