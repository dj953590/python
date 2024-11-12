
import textwrap
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
import os


from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

pdfs = 'C:/DJ/docs/query'
collection_name = 'Query_Collection'
# Set logging level to DEBUG for detailed information
# logging.basicConfig(level=logging.DEBUG)


def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))


def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width)) 

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

loader = DirectoryLoader(pdfs, loader_cls=PyPDFLoader)
documents = loader.load()
print(len(documents))
splitter = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 20)
docs = splitter.split_documents(documents)
print(len(docs))

#split_docs = split_into_n_lists(docs, 25)

embeddings = OllamaEmbeddings(model="llama3", show_progress=True)

#for i in range(len(split_docs)):
#    vectordb = PGVector.from_documents(collection_name=collection_name, documents=split_docs[i], 
#                                embedding=embeddings,
#                                connection=CONNECTION_STRING,
#                                use_jsonb=True,
#                                async_mode=False,
#                              )
#    print("finished iteration: " + str(i))
vectordb = PGVector.from_documents(collection_name=collection_name, documents=docs, 
                                embedding=embeddings,
                                connection=CONNECTION_STRING,
                                pre_delete_collection=False
                               )
#vectordb.persist()
vectordb = None
