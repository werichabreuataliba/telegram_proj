from setuptools import setup, find_packages

setup(
    name="chatbot_rag",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "langchain==0.1.20",
        "langchain-community==0.0.38",
        "langchain-openai==0.0.8",
        "langchain-text-splitters",
        "langchain-google-genai",
        "google-generativeai",
        "python-dotenv",
        "faiss-cpu",
        "pypdf",
        "gradio"
    ],
)