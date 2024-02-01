import time
import textwrap
from langchain_community.vectorstores import Chroma

from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
from langchain.chains import RetrievalQA
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

# This code sets up a retrieval-based question answering system using a pre-trained language model and a vector database. 
# The system takes a query, retrieves relevant documents from the vector database, and uses a pre-trained language model to generate an answer. 

# Define file paths
modelPath = "C:/DJ/models/ixl"
queryModelPath = "C:/DJ/models/t5"
dbPath = 'C:/DJ/projects/python/dbdir/'

def print_text(text): 
    for char in text:
        print(char, end = "", flush = True)
        time.sleep(0.02)

def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width))        

# Define query
query = "What is Target price of Signify NV ?"

embedding = HuggingFaceInstructEmbeddings(model_name=modelPath, 
                                                      model_kwargs={"device": "cpu"})
# Create SentenceTransformerEmbeddings object
#embedding = SentenceTransformerEmbeddings(model_name=modelPath)

# Create Chroma object for vector database
vectordb = Chroma(persist_directory=dbPath, embedding_function=embedding)

# Create retriever from vector database
retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# Load model for sequence-to-sequence generation
model = AutoModelForSeq2SeqLM.from_pretrained(queryModelPath)

# Load tokenizer for sequence-to-sequence generation
tokenizer = AutoTokenizer.from_pretrained(queryModelPath, trust_remote_code=True)

# Create pipeline for text-to-text generation
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=500)

# Create HuggingFacePipeline object
llm_flan = HuggingFacePipeline(pipeline=pipe)

# Create RetrievalQA object
qa_chain = RetrievalQA.from_chain_type(llm=llm_flan, chain_type="stuff", retriever=retriever, return_source_documents=True)

# Get response from QA chain
response = qa_chain(query)

# Print response
print_text(wraptxt(response['result']))


