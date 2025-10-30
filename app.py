import streamlit as st
from src.helper import download_embeddings
from src.prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

from langchain.chains import LLMChain

# Load environment variables
load_dotenv()
def initialize_chains():
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    # Load embeddings and index
    embeddings = download_embeddings()
    docsearch = PineconeVectorStore.from_existing_index(
        index_name="medical-chatbot",
        embedding=embeddings,
    )
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.4,
        max_output_tokens=500,
        convert_system_message_to_human=True,
    )

    # Create RAG chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # ✅ Create a Query Rewriter Chain
    rewrite_prompt = PromptTemplate(
        input_variables=["query"],
        template=(
            "You are a medical query enhancer. "
            "Rewrite the given user query into a more precise, medically detailed, and clear question "
            "to improve search results.\n\n"
            "User query: {query}\n\n"
            "Rewritten query:"
        ),
    )

    rewrite_chain = LLMChain(llm=llm, prompt=rewrite_prompt)

    return rag_chain,rewrite_chain
