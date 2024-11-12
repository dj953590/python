
import chromadb 
import textwrap
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions
import logging

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

dbPath = 'C:/DJ/db/'
pdfs = 'C:/DJ/docs/query'
collection_name = 'Query_Collection'
# Set logging level to DEBUG for detailed information
# logging.basicConfig(level=logging.DEBUG)

def split_into_n_lists(data, n):
  """
  This function splits a list into n sub-lists of approximately equal size.

  Args:
      data: The list to be split.
      n: The number of sub-lists to create.

  Returns:
      A list of sub-lists, each containing approximately an equal share of elements.
  """
  return [data[i::n] for i in range(n)]

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
print(len(docs))
model_kwargs = {'device': 'cpu'}  # Do not include 'token' here
embeddings = OllamaEmbeddings(model="llama3", show_progress=True)
split_docs = split_into_n_lists(docs, 25)
print("Total number of chunks: " + str(len(split_docs)) )

for i in range(len(split_docs)):
    vectordb = Chroma.from_documents(collection_name=collection_name, documents=split_docs[i], 
                                    embedding=embeddings,
                                    persist_directory=dbPath
                               )
    vectordb.persist()
    vectordb = None
    print("finished iteration: " + str(i))
