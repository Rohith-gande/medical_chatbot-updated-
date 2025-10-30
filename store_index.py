from src.helper import load_pdf_file,text_split,download_embeddings
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data=load_pdf_file(data="Data/")
text_chunks=text_split(extracted_data)
embeddings=download_embeddings()

docsearch= PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name="medical-chatbot",
    # namespace="medical-chatbot",
)