import chromadb 
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)

dbPath = 'C:/DJ/projects/python/db/'
pdf_file = 'C:/DJ/projects/python/nlp/pdf/docs/BloombergGPT.pdf'

collection_name = 'Bloomberg_Default'

dbsettings = Settings(allow_reset=True, is_persistent=True,persist_directory=dbPath)

client = chromadb.PersistentClient(settings=dbsettings)
client.reset()

collection = client.get_or_create_collection(collection_name)
reader = PdfReader(pdf_file)

splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap  = 20)
# printing number of pages in pdf file
numofpages = len(reader.pages)
print(len(reader.pages))
id = []
docs = []
# getting a specific page from the pdf file
for i in range(reader.numPages) :
    page = reader.pages[i]
    # extracting text from page
    text = page.extract_text()
    documents = splitter.split_text(text)
    pageId = 'Page_' +str(i)
    for index in range(len(documents)) :
       id.clear()
       docs.clear()
       id.append(('Page' + str(i) + str(index)))
       mdatas = {}
       mdatas['PageNumber'] = pageId
       docs.append(documents[index])
       collection.add(documents = docs, metadatas=mdatas, ids=id) 
       print(documents[index])
