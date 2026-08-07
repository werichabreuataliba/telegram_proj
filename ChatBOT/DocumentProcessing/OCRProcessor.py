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

        print("OCR -> PDF aberto")
        print("OCR -> quantidade de páginas:", len(pdf))

        for i, pagina in enumerate(pdf):

            print(f"OCR -> processando página {i}")

            pix = pagina.get_pixmap(dpi=300)

            imagem = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            image_file = f"temp_page_{i}.png"

            imagem.save(image_file)

            print("OCR -> imagem salva:", image_file)
            print("OCR -> chamando self.ocr.ocr()")

            resultado = self.ocr.ocr(
                image_file,
                cls=True,
                rec=False
            )

            print("OCR -> self.ocr.ocr() terminou")
            print("OCR -> tipo resultado:", type(resultado))
            print("OCR -> resultado é None?", resultado is None)

            if resultado:

                print("OCR -> entrou no processamento do resultado")

                for bloco in resultado:

                    print("OCR -> processando bloco")
                    print("OCR -> tipo bloco:", type(bloco))

                    for linha in bloco:

                        print("OCR -> processando linha")
                        print("OCR -> linha:", linha)
                        print("OCR -> tipo linha:", type(linha))

                        try:

                            valor = linha[1][0]

                            print("OCR -> valor:", valor)
                            print("OCR -> tipo valor:", type(valor))

                            if isinstance(valor, str):
                                texto += valor
                                texto += "\n"
                            else:
                                print(
                                    "OCR -> ATENÇÃO: valor não é string:",
                                    type(valor)
                                )

                        except Exception as e:

                            print("OCR -> ERRO PROCESSANDO LINHA:", e)
                            print("OCR -> linha problemática:", linha)

            os.remove(image_file)

        pdf.close()

        print("OCR -> processamento finalizado")
        print("OCR -> tamanho do texto:", len(texto))

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