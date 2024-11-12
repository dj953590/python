
from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language

dbPath = 'C:/DJ/projects/python/db/'
pdf_file = 'C:/DJ/docs/query/Tesla.pdf'

collection_name = 'Tesla_Default'

# dbsettings = Settings(allow_reset=True, is_persistent=True,persist_directory=dbPath)

# client = chromadb.PersistentClient(settings=dbsettings)
# client.reset()

# collection = client.get_or_create_collection(collection_name)
reader = PdfReader(pdf_file)

splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap  = 20, separators=['\n\n', '\n', ' ', '']) #RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap  = 20)
# printing number of pages in pdf file
numofpages = len(reader.pages)
print(len(reader.pages))
id = []
docs = []
# getting a specific page from the pdf file
for i in range(len(reader.pages)):
    page = reader.pages[i]
    # extracting text from page
    text = page.extract_text()
    documents = splitter.split_text(text)
    pageId = 'Page_' +str(i)
    # for index in range(len(documents)) :
    #    id.clear()
    #    docs.clear()
    #    id.append(('Page' + str(i) + str(index)))
    #    mdatas = {}
    #    mdatas['PageNumber'] = pageId
    #    docs.append(documents[index])
    #    #collection.add(documents = docs, metadatas=mdatas, ids=id) 
    #    print(documents[index])
