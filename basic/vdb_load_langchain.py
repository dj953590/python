
import chromadb 
import textwrap
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
from langchain.embeddings import HuggingFaceInstructEmbeddings

dbPath = 'C:/DJ/projects/python/dblangmini/'
pdf_file = 'C:/DJ/projects/python/nlp/pdf/docs/Sunoco.pdf'
modelPath = "C:/DJ/projects/python/mini"
collection_name = 'Bloomberg_langchain'

def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))


def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 

loader = PyPDFLoader(pdf_file)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap  = 100)
docs = splitter.split_documents(documents)
embedding_function = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", 
                                                      model_kwargs={"device": "cpu"})
#embedding_function = embedding_functions.InstructorEmbeddingFunction() 

#embedding_function = SentenceTransformerEmbeddings(model_name=modelPath)

vectordb = Chroma.from_documents(documents=docs, 
                                 embedding=embedding_function,
                                 persist_directory=dbPath)
vectordb.persist()
vectordb = None
