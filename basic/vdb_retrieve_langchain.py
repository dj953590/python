import textwrap
from langchain.docstore.document import Document
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
import os
from langchain.chains import RetrievalQA


collection_name = 'Query_Collection'


CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))
        
def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 



embeddings = OllamaEmbeddings(model="llama3", show_progress=True)
# Create Chroma object for vector database
vectordb = PGVector(collection_name=collection_name,connection=CONNECTION_STRING, embeddings=embeddings, distance_strategy = 'cosine')

#retriever = vectordb.as_retriever(search_kwargs={"k": 5})

#docs = retriever.get_relevant_documents(query)

query = " What is Expected total return of Tesla ? "
embedding = embeddings.embed_query(query)

similar = vectordb.similarity_search_with_score(query, k=4 )

for doc in similar:
    print(doc, end="\n\n")
    
#printdocs(docs)