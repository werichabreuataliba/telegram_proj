import gradio as gr
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain.chains import RetrievalQA

# 🔑 chave Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyA-E22kE7XipFPjk2AbKwdRg2lGUmtmrX0"

vectorstore = None


def load_file(file):
    global vectorstore

    if file is None:
        return "Nenhum arquivo enviado."

    file_path = file.name

    # loader
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # splitter
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # 🔥 embeddings Gemini
    #embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    vectorstore = FAISS.from_documents(docs, embeddings)

    return "Arquivo processado com sucesso!"


def ask_question(question):
    global vectorstore

    if vectorstore is None:
        return "Envie um arquivo primeiro."

    # 🔥 LLM Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    return qa.run(question)


# UI
with gr.Blocks() as app:
    gr.Markdown("# Chatbot RAG com Gemini")

    file_input = gr.File(label="Envie PDF ou TXT")
    upload_btn = gr.Button("Processar arquivo")

    question = gr.Textbox(label="Pergunta")
    answer = gr.Textbox(label="Resposta")

    upload_btn.click(load_file, inputs=file_input, outputs=answer)
    question.submit(ask_question, inputs=question, outputs=answer)

app.launch()