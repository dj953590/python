import textwrap
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
from PyPDF2 import PdfReader
import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)
pdf_file = 'C:/DJ/docs/query/Tesla.pdf'
pdfs = 'C:/DJ/docs/query'
collection_name = 'QueryFirstPages_mxbai_semantic'


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


def load_first_page(pdf_path):
    """
  This function loads a PDF and extracts the text from the first page.

  Args:
      pdf_path: The path to the PDF file.

  Returns:
      The extracted text from the first page of the PDF (or None on error).
  """
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            return reader.pages[0].extract_text()  # Extract text from first page
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    except Exception as e:
        print(f"Error processing PDF: {pdf_path} - {e}")
        return None


def generate_qa_repsonse(query):
    # Create RetrievalQA object
    qa_chain = RetrievalQA.from_chain_type(llm=llm_llama, chain_type="stuff",
                                           retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
                                           chain_type_kwargs={"verbose": True}, return_source_documents=True)
    response = qa_chain(query)
    result_str = (wraptxt(response['result']))
    source_str = (wraptxt(response['source_documents'][0].metadata['source']))
    #page_no = response['source_documents'][0].metadata['page']
    return result_str + '\n' + source_str  #+ ' Page Number :' + str(page_no)


def generate_response(prompt):
    completion = generate_qa_repsonse(prompt)
    return completion


def get_document(first_page, pdf_file):
    # Create a langchain.docstore.Document object with metadata
    metadata = {"page": 1, "source": pdf_file}  # Example metadata (adjust as needed)
    document = Document(page_content=first_page, metadata=metadata)
    return document


# Assuming pdfs is a list containing paths to PDF files
embeddings = OllamaEmbeddings(model="mxbai-embed-large", show_progress=True)
splitter = SemanticChunker(embeddings=embeddings)
# Assuming pdfs is the directory path containing PDFs
pdf_files = [os.path.join(pdfs, filename) for filename in os.listdir(pdfs) if filename.endswith(".pdf")]
collection_pdf_names = [os.path.basename(pdf_file) for pdf_file in pdf_files]
vectordb = None
for pdf_file_path in pdf_files:
    documents = []
    pdf = os.path.basename(pdf_file_path)
    if pdf in collection_pdf_names:
        first_page_text = load_first_page(pdf_file_path)
        if first_page_text:
            documents.append(get_document(first_page_text, pdf_file_path))
            #splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap = 0)
            docs = splitter.split_documents(documents)
            print(len(docs))
            vectordb = PGVector.from_documents(collection_name=pdf, documents=docs,
                                               embedding=embeddings,
                                               connection=CONNECTION_STRING,
                                               pre_delete_collection=False
                                               )

llm_llama = Ollama(base_url='http://localhost:11434', model="llama3:instruct")

# based on the pdf file generate the query
collection_name = 'Tesla.pdf'
vectordb = PGVector(collection_name=collection_name, connection=CONNECTION_STRING, embeddings=embeddings)
retriever = vectordb.as_retriever()
query = "What is Target price of Tesla ?"
docs = retriever.get_relevant_documents(query)
answer = generate_response(query)
print(answer)
query = "How many vechicles Tesla is recalling ?"
retriever = vectordb.as_retriever()
docs = retriever.get_relevant_documents(query)
answer = generate_response(query)
print(answer)
