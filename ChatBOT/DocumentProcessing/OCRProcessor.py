import os
import fitz

from PIL import Image

from paddleocr import PaddleOCR


class OCRProcessor:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="pt"
        )

    def extract_text(self, pdf_path):

        texto = ""

        pdf = fitz.open(pdf_path)

        for i, pagina in enumerate(pdf):

            pix = pagina.get_pixmap(
                dpi=300
            )

            imagem = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            image_file = f"temp_page_{i}.png"

            imagem.save(image_file)

            resultado = self.ocr.ocr(
                image_file,
                cls=True
            )

            if resultado:

                for bloco in resultado:

                    for linha in bloco:

                        texto += linha[1][0]
                        texto += "\n"

            os.remove(image_file)

        pdf.close()

        return texto

# import fitz
# import numpy as np
#
# from PIL import Image
# from paddleocr import PaddleOCR
#
#
# class OCRProcessor:
#
#     def __init__(self):
#
#         self.ocr = PaddleOCR(
#             use_angle_cls=True,
#             lang="pt"
#         )
#
#     def extract_text(self, pdf_path):
#
#         texto = ""
#
#         pdf = fitz.open(pdf_path)
#
#         for pagina in pdf:
#
#             pix = pagina.get_pixmap(dpi=300)
#
#             imagem = Image.frombytes(
#                 "RGB",
#                 [pix.width, pix.height],
#                 pix.samples
#             )
#             try:
#                 resultado = self.ocr.ocr(
#                     np.array(imagem)
#                 )
#             except Exception as e:
#                 print(e)
#                 raise
#
#             if resultado:
#
#                 for bloco in resultado:
#
#                     for linha in bloco:
#
#                         texto += linha[1][0]
#                         texto += "\n"
#
#         pdf.close()
#
#         return texto