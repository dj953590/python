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
from langchain.retrievers.multi_query import MultiQueryRetriever
import pdfplumber
import fitz
import logging
import string
import nltk
from nltk.corpus import stopwords
import os
import re

nltk.download('stopwords')
from langchain.prompts import FewShotPromptTemplate

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

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
collection_name = 'QueryFirstPages_mxbai_pymupdf'

# Assuming pdfs is the directory path containing PDFs
pdf_files = [os.path.join(pdfs, filename) for filename in os.listdir(pdfs) if filename.endswith(".pdf")]


# Set logging level to DEBUG for detailed information
# logging.basicConfig(level=logging.DEBUG)


def printdocs(docs: list[Document]):
    for d in range(len(docs)):
        doc = docs[d].page_content
        print(wraptxt(doc))


def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width))


def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    # text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # # Remove HTML tags
    # text = re.sub(r'<.*?>', '', text)

    # # Remove special characters but keep currency symbols, dates, and numbers
    # text = re.sub(r'[^\w\s\$€£¥%/\-.,]', '', text)

    # # Remove stopwords (optional, based on requirement)
    # #stop_words = set(stopwords.words('english'))
    # #text = ' '.join([word for word in text.split() if word not in stop_words])

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


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


def load_first_page_plumber(pdf_path):
    """
  This function loads a PDF and extracts the text from the first page.

  Args:
      pdf_path: The path to the PDF file.

  Returns:
      The extracted text from the first page of the PDF (or None on error).
  """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            formatted_text = first_page.extract_text()
            # Extract tables from the page
            # tables = first_page.extract_tables()
            # for table in tables:
            #   formatted_text += "\n\nTable:\n"
            #   for row in table:
            #     if row is not None:
            #       formatted_text += " | ".join(row) + "\n"

            return formatted_text  # Extract text from first page

    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    except Exception as e:
        print(f"Error processing PDF: {pdf_path} - {e}")
        return None


def load_first_page_pymupdf(pdf_path):
    """
    This function loads a PDF and extracts the text from the first page.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        The extracted text from the first page of the PDF (or None on error).
    """
    try:
        with fitz.open(pdf_path) as pdf:
            first_page = pdf[0]
            formatted_text = clean_text(first_page.get_text("text"))
            # Extract tables from the page
            # tables = first_page.extract_tables()
            # for table in tables:
            #     formatted_text += "\n\nTable:\n"
            #     for row in table:
            #         if row is not None:
            #             formatted_text += " | ".join(row) + "\n"

            return formatted_text  # Extract text from first page

    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    except Exception as e:
        print(f"Error processing PDF: {pdf_path} - {e}")
        return None


def generate_qa_repsonse(query):
    # Create RetrievalQA object
    retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
                                                      llm=llm_llama)
    #qa_chain = RetrievalQA.from_chain_type(llm=llm_llama, chain_type="stuff", retriever=vectordb.as_retriever(search_kwargs={"k": 3}), chain_type_kwargs={"verbose": True}, return_source_documents=True)       
    qa_chain = RetrievalQA.from_chain_type(llm=llm_llama, chain_type="stuff", retriever=retriever_from_llm,
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

documents = []
for pdf_file in pdf_files:
    first_page_text = load_first_page_pymupdf(pdf_file)
    if first_page_text:
        documents.append(get_document(first_page_text, pdf_file))

# loader = DirectoryLoader(pdfs, loader_cls=PyPDFLoader)
# documents = loader.load()
# print(len(documents))
embeddings = OllamaEmbeddings(model="mxbai-embed-large", show_progress=True)
splitter = SemanticChunker(embeddings=embeddings)
#splitter = RecursiveCharacterTextSplitter(chunk_size = 512, chunk_overlap = 128)
docs = splitter.split_documents(documents)
print(len(docs))

# tp_examples = [
#     {"context": "Target Price $400.", "input": "What is the Target Price  ?", "output": "$400"},
#     {"context": "The Mona Lisa is a painting by Leonardo da Vinci.", "input": "Who painted the Mona Lisa?", "output": "Leonardo da Vinci"},
#     {"context": "The Amazon Rainforest is the world's largest rainforest.", "input": "What is the largest rainforest in the world?", "output": "Amazon Rainforest"},
# ]

# # Create a prompt template
# tp_prompt_template = FewShotPromptTemplate(
#     examples=tp_examples,
#     input_variables=["context", "input"],
#     prefix="Here are some examples:\n",
#     example_separator="\n",
#     suffix="\nContext:\n{context}\nQuestion: {input}",
# )

llm_llama = Ollama(base_url='http://localhost:11434', model="llama3:instruct")

vectordb = PGVector.from_documents(collection_name=collection_name, documents=docs,
                                   embedding=embeddings,
                                   connection=CONNECTION_STRING,
                                   pre_delete_collection=False
                                   )
retriever = vectordb.as_retriever()

query = "What is Target price of Tesla ?"
answer = generate_response(query.lower())
print(answer)
query = "How many vechicles Tesla is recalling ?"
answer = generate_response(query.lower())
print(answer)
query = "What is Target price of Signify NV ?"
answer = generate_response(query.lower())
print(answer)
query = "How much cost savings was announced by Signify NV ?"
answer = generate_response(query.lower())
print(answer)
