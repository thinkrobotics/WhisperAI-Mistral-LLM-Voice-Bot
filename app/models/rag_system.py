from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.config import Config
import os

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_db = None
        self._initialize_db()

    def _initialize_db(self):
        """Load documents from the data directory"""
        if not os.path.exists(Config.RAG_DOCS_PATH):
            os.makedirs(Config.RAG_DOCS_PATH)
            print(f"Created directory: {Config.RAG_DOCS_PATH}")
            return

        try:
            loader = DirectoryLoader(Config.RAG_DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
            documents = loader.load()
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = splitter.split_documents(documents)
            
            self.vector_db = FAISS.from_documents(texts, self.embeddings)
            print("RAG system initialized successfully!")
        except Exception as e:
            print(f"RAG initialization failed: {str(e)}")

    def query(self, question: str) -> str:
        if not self.vector_db:
            return ""
            
        docs = self.vector_db.similarity_search(question, k=2)
        return "\n".join([doc.page_content for doc in docs])