import os

from dotenv import load_dotenv

# ==========================================
# LangChain
# ==========================================
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    CharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)

from langchain.chains import (
    RetrievalQA
)

from ChatBOT.DocumentProcessing.ProtocolRepository import ProtocolRepository
from DocumentProcessing.DocumentProcessor import (
    DocumentProcessor
)
document_processor = DocumentProcessor()

# ==========================================
# Telegram
# ==========================================
from telegram import Update, Bot

from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from ChatBOT.Uteis.Estrutura import extract_patient_data, patient_sessions, generate_summary

# ==========================================
# Configuração
# ==========================================
load_dotenv("config.env")

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)

os.environ["OPENAI_API_KEY"] = (
    OPENAI_API_KEY
)

# ==========================================
# Um vetor por usuário
# ==========================================
vectorstores = {}

async def send_hello():

    bot = Bot(token=TELEGRAM_TOKEN)

    chat_id = 7749850190
    contacts = {
        "11988877009": chat_id
    }
    numero = "11988877009"

    chat_id = contacts[numero]

    await bot.send_message(
        chat_id=chat_id,
        text="Olá! Sou sua assistente virtual."
    )
# ==========================================
# Processamento do documento
# ==========================================
def load_file(
    user_id,
    file_path
):
    documents = document_processor.load(
        file_path
    )

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(
        documents
    )

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    vectorstores[user_id] = vectorstore

    # if file_path.endswith(".pdf"):
    #
    #     loader = PyPDFLoader(
    #         file_path
    #     )
    #
    # else:
    #
    #     loader = TextLoader(
    #         file_path,
    #         encoding="utf-8"
    #     )
    #
    # documents = loader.load()
    #
    # splitter = CharacterTextSplitter(
    #     chunk_size=1000,
    #     chunk_overlap=200
    # )
    #
    # docs = splitter.split_documents(
    #     documents
    # )
    #
    # embeddings = OpenAIEmbeddings()
    #
    # vectorstore = (
    #     FAISS.from_documents(
    #         docs,
    #         embeddings
    #     )
    # )
    #
    # vectorstores[user_id] = (
    #     vectorstore
    # )

# ==========================================
# Perguntas
# ==========================================
def ask_question(
    user_id,
    question
):

    if user_id not in vectorstores:
        return (
            "Envie um PDF ou TXT primeiro."
        )

    vectorstore = (
        vectorstores[user_id]
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={
                "k": 4
            }
        )
    )

    result = qa.run(question)

    return result

# ==========================================
# /start
# ==========================================
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=7749850190,
        text="Olá! Sou sua assistente virtual."
    )

    await update.message.reply_text(
        """
Olá!

Envie um PDF ou TXT.

Depois faça perguntas sobre ele.

Exemplo:

1 - Envie contrato.pdf

2 - Pergunte:

"Qual é o prazo do contrato?"
"""
    )

# ==========================================
# Upload de documentos
# ==========================================
async def receive_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update.effective_user.id
    )

    document = (
        update.message.document
    )

    file_name = (
        document.file_name
    )

    telegram_file = (
        await document.get_file()
    )

    os.makedirs(
        "docs",
        exist_ok=True
    )

    file_path = (
        f"docs/{user_id}_{file_name}"
    )

    await telegram_file.download_to_drive(
        file_path
    )

    await update.message.reply_text(
        "Processando documento..."
    )

    try:

        load_file(
            user_id,
            file_path
        )

        dados_paciente = extract_patient_data(
            user_id, vectorstores
        )

        protocolo = ProtocolRepository.carregar_protocolo(

            dados_paciente["especialidade"],

            dados_paciente["categoria"]

        )

        patient_sessions[user_id] = {

            "step": 1,

            "protocolo": protocolo,

            "nome": dados_paciente["nome"],

            "idade": dados_paciente["idade"],

            "sexo": dados_paciente["sexo"],

            "diagnostico": dados_paciente["diagnostico"],

            "retorno": dados_paciente["retorno"],

            "respostas": {}

        }

        await update.message.reply_text(
            "Documento processado com sucesso."
        )
        await update.message.reply_text(
            f"""
        Identificamos o seguinte paciente:

        Nome: {patient_sessions[user_id]["nome"]}
        Idade: {patient_sessions[user_id]["idade"]}

        Você é {patient_sessions[user_id]["nome"]} ou responsável pelo paciente?

        1 - Sim
        2 - Não
        """
        )

    except Exception as e:

        await update.message.reply_text(
            f"Erro: {str(e)}"
        )

# ==========================================
# Perguntas
# ==========================================
async def receive_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    #print(update.effective_chat.id)
    user_id = (
        update.effective_user.id
    )

    question = (
        update.message.text
    )

    try:

        # answer = ask_question(
        #     user_id,
        #     question
        # )
        await receive_sections(update, ContextTypes.DEFAULT_TYPE)
        #
        # await update.message.reply_text(
        #     answer.
        # )

    except Exception as e:

        await update.message.reply_text(
            f"Erro: {str(e)}"
        )

async def receive_sections(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    try:

        user_id = update.effective_user.id

        resposta = update.message.text

        if user_id not in patient_sessions:

            answer = ask_question(
                user_id,
                resposta
            )

            await update.message.reply_text(
                answer
            )

            return

        session = patient_sessions[user_id]

        protocolo = session["protocolo"]

        step_atual = session["step"]

        # procura o step no protocolo
        pergunta = next(
            (
                item
                for item in protocolo["steps"]
                if item["step"] == step_atual
            ),

            None

        )

        if pergunta is None:

            resumo = generate_summary(session)

            await update.message.reply_text(
                resumo
            )

            del patient_sessions[user_id]

            return

        # salva resposta
        print('Pergunta:', pergunta)
        session["respostas"][
            pergunta["step"]
        ] = resposta

        # terminou protocolo?
        if pergunta["proximo_step"] == 999:

            resumo = generate_summary(session)

            await update.message.reply_text(
                resumo
            )

            del patient_sessions[user_id]

            return

        # próximo passo
        session["step"] = pergunta["proximo_step"]

        proxima = next(

            (
                item
                for item in protocolo["steps"]
                if item["step"] == session["step"]
            ),

            None

        )

        texto = proxima["pergunta"]

        for indice, opcao in enumerate(

                proxima["opcoes"],

                start=1

        ):

            texto += f"\n\n{indice} - {opcao}"

        await update.message.reply_text(
            texto
        )
    except Exception as e:
        print("Erro ao ler a reposta: " ,e)
# async def receive_sectios(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE
# ):
#
#     user_id = update.effective_user.id
#
#     question = update.message.text
#
#     # verifica se existe uma sessão ativa
#     if user_id in patient_sessions:
#
#         session = patient_sessions[user_id]
#
#         step = session["step"]
#
#         # ===================================
#         # ETAPA 1
#         # ===================================
#         if step == 1:
#
#             if question == "1":
#
#                 session["step"] = 2
#
#                 await update.message.reply_text(
# """
# Desde a cirurgia você percebeu melhora da visão?
#
# 1 - Sim
# 2 - Parcialmente
# 3 - Não
# """
#                 )
#
#                 return
#
#             else:
#
#                 await update.message.reply_text(
#                     "Atendimento encerrado."
#                 )
#
#                 return
#
#         # ===================================
#         # ETAPA 2
#         # ===================================
#         if step == 2:
#
#             session["respostas"][
#                 "melhora_visao"
#             ] = question
#
#             session["step"] = 3
#
#             await update.message.reply_text(
# """
# Está utilizando corretamente os medicamentos prescritos?
#
# 1 - Sim
# 2 - Não
# """
#             )
#
#             return
#
#         # ===================================
#         # ETAPA 3
#         # ===================================
#         if step == 3:
#
#             session["respostas"][
#                 "medicacao"
#             ] = question
#
#             session["step"] = 4
#
#             await update.message.reply_text(
# """
# Está sentindo algum dos sintomas abaixo?
#
# 1 - Dor ocular
#
# 2 - Vermelhidão
#
# 3 - Visão embaçada
#
# 4 - Nenhum
# """
#             )
#
#             return
#
#         # ===================================
#         # ETAPA 4
#         # ===================================
#         if step == 4:
#
#             session["respostas"][
#                 "sintomas"
#             ] = question
#
#             session["step"] = 5
#
#             resumo = generate_summary(
#                 session
#             )
#
#             await update.message.reply_text(
#                 resumo
#             )
#
#             return
#
#     # ===================================
#     # FLUXO NORMAL DO RAG
#     # ===================================
#
#     try:
#
#         answer = ask_question(
#             user_id,
#             question
#         )
#
#         await update.message.reply_text(
#             answer
#         )
#
#     except Exception as e:
#
#         await update.message.reply_text(
#             f"Erro: {str(e)}"
#         )
# ==========================================
# Main
# ==========================================
def main():

    app = (
        ApplicationBuilder()
        .token(
            TELEGRAM_TOKEN
        )
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            receive_document
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT &
            ~filters.COMMAND,
            receive_text
        )
    )

    print(
        "Bot iniciado..."
    )

    app.run_polling()

# ==========================================
# Inicialização
# ==========================================
if __name__ == "__main__":
    main()