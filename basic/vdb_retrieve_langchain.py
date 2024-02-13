import textwrap
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
modelPath = "C:/DJ/models/ixl"
dbPath = 'C:/DJ/db/'
collection_name = 'Query_Collection'

def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))
        
def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 


query = "What is Target price of Signify?"

#embedding = SentenceTransformerEmbeddings(model_name=modelPath)
embedding = HuggingFaceInstructEmbeddings(model_name=modelPath, 
                                                      model_kwargs={"device": "cpu"})
vectordb = Chroma(collection_name=collection_name,persist_directory=dbPath, embedding_function=embedding)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})

docs = retriever.get_relevant_documents(query)
    
printdocs(docs)