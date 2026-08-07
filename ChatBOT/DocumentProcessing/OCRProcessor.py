import os
import fitz

from PIL import Image

from paddleocr import PaddleOCR


class OCRProcessor:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_angle_cls=False,
            lang="pt"
        )

    def extract_text(self, pdf_path):

        texto = ""

        pdf = fitz.open(pdf_path)

        print("OCR -> PDF aberto", flush=True)
        print("OCR -> quantidade de páginas:", len(pdf), flush=True)

        for i, pagina in enumerate(pdf):

            print(f"OCR -> processando página {i}", flush=True)

            pix = pagina.get_pixmap(dpi=300)

            imagem = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            image_file = f"temp_page_{i}.png"

            imagem.save(image_file)

            print(
                "OCR -> imagem salva:",
                image_file,
                flush=True
            )

            print(
                "OCR -> chamando self.ocr.ocr()",
                flush=True
            )

            resultado = self.ocr.ocr(
                image_file,
                cls=False,
                rec=True
            )

            print(
                "OCR -> self.ocr.ocr() terminou",
                flush=True
            )

            print(
                "OCR -> tipo resultado:",
                type(resultado),
                flush=True
            )

            print(
                "OCR -> resultado é None?",
                resultado is None,
                flush=True
            )

            if resultado:

                print(
                    "OCR -> processando resultado",
                    flush=True
                )

                for pagina_resultado in resultado:

                    print(
                        "OCR -> quantidade de linhas:",
                        len(pagina_resultado),
                        flush=True
                    )

                    for linha in pagina_resultado:

                        print(
                            "OCR -> linha:",
                            linha,
                            flush=True
                        )

                        try:

                            texto_ocr = linha[1][0]
                            confianca = linha[1][1]

                            print(
                                "OCR -> texto:",
                                texto_ocr,
                                flush=True
                            )

                            print(
                                "OCR -> confiança:",
                                confianca,
                                flush=True
                            )

                            texto += texto_ocr
                            texto += "\n"

                        except Exception as e:

                            print(
                                "OCR -> erro processando linha:",
                                e,
                                flush=True
                            )

                            print(
                                "OCR -> linha problemática:",
                                linha,
                                flush=True
                            )

            os.remove(image_file)

        pdf.close()

        print(
            "OCR -> processamento finalizado",
            flush=True
        )

        print(
            "OCR -> tamanho do texto:",
            len(texto),
            flush=True
        )

        return texto

# import os
# import fitz
#
# from PIL import Image
#
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
#         print("OCR -> PDF aberto")
#         print("OCR -> quantidade de páginas:", len(pdf))
#
#         for i, pagina in enumerate(pdf):
#
#             print(f"OCR -> processando página {i}")
#
#             pix = pagina.get_pixmap(dpi=300)
#
#             imagem = Image.frombytes(
#                 "RGB",
#                 [pix.width, pix.height],
#                 pix.samples
#             )
#
#             image_file = f"temp_page_{i}.png"
#
#             imagem.save(image_file)
#
#             print("OCR -> imagem salva:", image_file)
#             print("OCR -> chamando self.ocr.ocr()")
#
#             resultado = self.ocr.ocr(
#                 image_file,
#                 cls=True,
#                 rec=False
#             )
#
#             print("OCR -> self.ocr.ocr() terminou")
#             print("OCR -> tipo resultado:", type(resultado))
#             print("OCR -> resultado é None?", resultado is None)
#
#             if resultado:
#
#                 print("OCR -> processando resultado", flush=True)
#
#                 for pagina_resultado in resultado:
#
#                     print(
#                         "OCR -> quantidade de linhas:",
#                         len(pagina_resultado),
#                         flush=True
#                     )
#
#                     for linha in pagina_resultado:
#
#                         print("OCR -> linha:", linha, flush=True)
#
#                         try:
#
#                             coordenadas = linha[0]
#                             texto_ocr = linha[1][0]
#                             confianca = linha[1][1]
#
#                             print(
#                                 "OCR -> texto:",
#                                 texto_ocr,
#                                 flush=True
#                             )
#
#                             print(
#                                 "OCR -> confiança:",
#                                 confianca,
#                                 flush=True
#                             )
#
#                             texto += texto_ocr
#                             texto += "\n"
#
#                         except Exception as e:
#
#                             print(
#                                 "OCR -> erro processando linha:",
#                                 e,
#                                 flush=True
#                             )
#
#                             print(
#                                 "OCR -> linha problemática:",
#                                 linha,
#                                 flush=True
#                             )
#
#             os.remove(image_file)
#
#         pdf.close()
#
#         print("OCR -> processamento finalizado")
#         print("OCR -> tamanho do texto:", len(texto))
#
#         return texto
#     # def extract_text(self, pdf_path):
#     #
#     #     texto = ""
#     #
#     #     pdf = fitz.open(pdf_path)
#     #
#     #     for i, pagina in enumerate(pdf):
#     #
#     #         pix = pagina.get_pixmap(
#     #             dpi=300
#     #         )
#     #
#     #         imagem = Image.frombytes(
#     #             "RGB",
#     #             [pix.width, pix.height],
#     #             pix.samples
#     #         )
#     #
#     #         image_file = f"temp_page_{i}.png"
#     #
#     #         imagem.save(image_file)
#     #
#     #         resultado = self.ocr.ocr(
#     #             image_file,
#     #             cls=True
#     #         )
#     #
#     #         if resultado:
#     #
#     #             for bloco in resultado:
#     #
#     #                 for linha in bloco:
#     #
#     #                     texto += linha[1][0]
#     #                     texto += "\n"
#     #
#     #         os.remove(image_file)
#     #
#     #     pdf.close()
#     #
#     #     return texto
#
# # import fitz
# # import numpy as np
# #
# # from PIL import Image
# # from paddleocr import PaddleOCR
# #
# #
# # class OCRProcessor:
# #
# #     def __init__(self):
# #
# #         self.ocr = PaddleOCR(
# #             use_angle_cls=True,
# #             lang="pt"
# #         )
# #
# #     def extract_text(self, pdf_path):
# #
# #         texto = ""
# #
# #         pdf = fitz.open(pdf_path)
# #
# #         for pagina in pdf:
# #
# #             pix = pagina.get_pixmap(dpi=300)
# #
# #             imagem = Image.frombytes(
# #                 "RGB",
# #                 [pix.width, pix.height],
# #                 pix.samples
# #             )
# #             try:
# #                 resultado = self.ocr.ocr(
# #                     np.array(imagem)
# #                 )
# #             except Exception as e:
# #                 print(e)
# #                 raise
# #
# #             if resultado:
# #
# #                 for bloco in resultado:
# #
# #                     for linha in bloco:
# #
# #                         texto += linha[1][0]
# #                         texto += "\n"
# #
# #         pdf.close()
# #
# #         return texto