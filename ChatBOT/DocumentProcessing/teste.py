from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="pt"
)

resultado = ocr.ocr(
    "teste.jpeg",
    cls=True
)

print(resultado)