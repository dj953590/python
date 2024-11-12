
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

dbPath = 'C:/DJ/db/'
pdfs = 'C:/DJ/docs/query'
modelPath = 'C:/DJ/models/ixl'
collection_name = 'Query_Collection'

def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))


def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 

loader = DirectoryLoader(pdfs, loader_cls=PyPDFLoader)
documents = loader.load()
print(len(documents))

splitter = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 20)
docs = splitter.split_documents(documents)
printdocs(docs)
model_kwargs = {'device': 'cpu'}  # Do not include 'token' here
embedding_function = HuggingFaceInstructEmbeddings(model_name=modelPath, 
                                                    model_kwargs=model_kwargs
                                                    )

vectordb = Chroma.from_documents(collection_name=collection_name, documents=docs, 
                                embedding=embedding_function,
                                persist_directory=dbPath
                               )
vectordb.persist()
vectordb = None
