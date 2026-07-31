from ChatBOT.repositorio_perguntas import (
    clinica_medica,
    pediatria,
    cardiologia,
    psiquiatria
)

class ProtocolRepository:
    protocolos = [
        clinica_medica,
        pediatria,
        cardiologia,
        psiquiatria
    ]

    @staticmethod
    def carregar_protocolo(
            especialidade,
            categoria
    ):

        for protocolo in ProtocolRepository.protocolos:

            if (

                protocolo["especialidade"] == especialidade

                and

                protocolo["categoria"] == categoria

            ):

                return protocolo

        return None