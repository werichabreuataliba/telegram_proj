
import gradio as gr

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv("config.env")

import os

#  coloque sua chave OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#  Variável global (index vetorial)
vectorstore = None


#  Função para carregar arquivo e criar RAG
def load_file(file):
    global vectorstore

    if file is None:
        return "Nenhum arquivo enviado."

    file_path = file.name

    #  Carregar arquivo
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()

    #  Quebrar em pedaços
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    #  Embeddings + banco vetorial
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    return "Arquivo processado com sucesso!"


#  Função de pergunta (RAG)
def ask_question(question):
    global vectorstore

    if vectorstore is None:
        return "Envie um arquivo primeiro."

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    result = qa.run(question)

    return result


# 🎨 Interface Gradio
with gr.Blocks() as app:
    gr.Markdown("# 🤖 Chatbot com RAG (LangChain)")

    file_input = gr.File(label="Envie PDF ou TXT")
    upload_btn = gr.Button("Processar arquivo")

    question = gr.Textbox(label="Pergunta")
    answer = gr.Textbox(label="Resposta")

    upload_btn.click(load_file, inputs=file_input, outputs=answer)
    question.submit(ask_question, inputs=question, outputs=answer)

app.launch()