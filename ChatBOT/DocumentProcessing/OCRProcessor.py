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

        print("OCR -> abriu método")

        texto = ""

        pdf = fitz.open(pdf_path)

        print(f"PDF possui {len(pdf)} páginas")

        for i, pagina in enumerate(pdf):

            print(f"Página {i}")

            pix = pagina.get_pixmap(dpi=300)

            imagem = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            image_file = f"temp_page_{i}.png"

            imagem.save(image_file)

            print("Chamando OCR...")

            print("OCR -> antes de chamar self.ocr.ocr()", flush=True)

            resultado = self.ocr.ocr(
                image_file,
                cls=True,
                rec=True
            )

            print("OCR -> self.ocr.ocr() terminou", flush=True)
            print(f"OCR -> resultado recebido: {resultado is not None}", flush=True)

            print(type(resultado))
            print(resultado)

            print("Entrando no IF")

            if resultado:
                print("OCR -> entrou no processamento do resultado", flush=True)

                for bloco in resultado:

                    print("OCR -> processando bloco", flush=True)

                    for linha in bloco:
                        print("OCR -> processando linha", flush=True)

                        texto += linha[1][0]
                        texto += "\n"

            else:
                print("OCR -> resultado vazio", flush=True)
            # if resultado:
            #
            #     print("Resultado não vazio")
            #
            #     for bloco in resultado:
            #
            #         print("Novo bloco")
            #
            #         for linha in bloco:
            #             print("Linha:", linha)
            #
            #             texto += linha[1][0]
            #             texto += "\n"

            print("Removendo imagem")

            os.remove(image_file)

        pdf.close()

        print("OCR finalizado")

        return texto
    # def extract_text(self, pdf_path):
    #
    #     texto = ""
    #
    #     pdf = fitz.open(pdf_path)
    #
    #     for i, pagina in enumerate(pdf):
    #
    #         pix = pagina.get_pixmap(
    #             dpi=300
    #         )
    #
    #         imagem = Image.frombytes(
    #             "RGB",
    #             [pix.width, pix.height],
    #             pix.samples
    #         )
    #
    #         image_file = f"temp_page_{i}.png"
    #
    #         imagem.save(image_file)
    #
    #         resultado = self.ocr.ocr(
    #             image_file,
    #             cls=True
    #         )
    #
    #         if resultado:
    #
    #             for bloco in resultado:
    #
    #                 for linha in bloco:
    #
    #                     texto += linha[1][0]
    #                     texto += "\n"
    #
    #         os.remove(image_file)
    #
    #     pdf.close()
    #
    #     return texto

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