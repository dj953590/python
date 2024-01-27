import chromadb 

dbPath = 'C:/DJ/projects/python/db/'

client = chromadb.PersistentClient(dbPath)

# using the chroma db 

collection = client.get_or_create_collection(name="Bloomberg_Default")

query = "What dataset BloombergGPT created? "

querytxts = [query]

results = collection.query(
    query_texts=querytxts,
    n_results=5
)

print(results)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
modelPath = "C:/DJ/projects/python/mini"

embedding = SentenceTransformerEmbeddings(model_name=modelPath)
vectordb = Chroma(persist_directory=dbPath, embedding_function=embedding)

retriever = vectordb.as_retriever()

docs = retriever.get_relevant_documents(query)
    
len(docs)

print(docs[0])