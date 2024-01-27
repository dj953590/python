
import chromadb 
import textwrap
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions


from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

dbPath = 'C:/DJ/projects/python/dbdir/'
pdfs = 'C:/DJ/projects/python/nlp/pdf/docs/'
modelPath = "C:/DJ/projects/python/ixl"
collection_name = 'Bloomberg_langchain'

def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))


def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 

loader = DirectoryLoader(pdfs, loader_cls=PyPDFLoader)
documents = loader.load()
print(len(documents))

splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap  = 100)
docs = splitter.split_documents(documents)
printdocs(docs)

embedding_function = HuggingFaceInstructEmbeddings(model_name=modelPath, 
                                                      model_kwargs={"device": "cpu"})
#embedding_function = embedding_functions.InstructorEmbeddingFunction() 

#embedding_function = SentenceTransformerEmbeddings(model_name=modelPath)

vectordb = Chroma.from_documents(documents=docs, 
                                 embedding=embedding_function,
                                 persist_directory=dbPath)
vectordb.persist()
vectordb = None
