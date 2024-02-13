import time
import textwrap
import gradio as gr
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
dbPath = 'C:/DJ/db'
collection_name = 'Query_Collection'

def print_text(text): 
    for char in text:
        print(char, end = "", flush = True)
        time.sleep(0.02)

def wraptxt(text: str, width: int = 120) -> str:
    return '\n'.join(textwrap.wrap(text, width))        


embedding = HuggingFaceInstructEmbeddings(model_name=modelPath, 
                                                      model_kwargs={"device": "cpu"})
# Create Chroma object for vector database
vectordb = Chroma(collection_name=collection_name,persist_directory=dbPath, embedding_function=embedding)
# Create retriever from vector database
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    # Load model for sequence-to-sequence generation
model = AutoModelForSeq2SeqLM.from_pretrained(queryModelPath)
    # Load tokenizer for sequence-to-sequence generation
tokenizer = AutoTokenizer.from_pretrained(queryModelPath, trust_remote_code=True)
    # Create pipeline for text-to-text generation
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=500)
    # Create HuggingFacePipeline object
llm_flan = HuggingFacePipeline(pipeline=pipe)

def generate_qa_repsonse(query):
    # Create RetrievalQA object
    qa_chain = RetrievalQA.from_chain_type(llm=llm_flan, chain_type="stuff", retriever=retriever, return_source_documents=True)       
    response = qa_chain(query)
    result_str = (wraptxt(response['result']))
    source_str = (wraptxt(response['source_documents'][0].metadata['source']))
    #page_no = response['source_documents'][0].metadata['page']
    return result_str + '\n' + source_str #+ ' Page Number :' + str(page_no)

def generate_response(prompt):
    completion = generate_qa_repsonse(prompt)
    return completion


def qa_bot(input, history):
    history = history or []
    output = generate_response(input)
    history.append((input, output))
    return history, history

with gr.Blocks(title="Helios RAG Demo", theme=gr.themes.Base(font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"], primary_hue=gr.themes.colors.red, secondary_hue=gr.themes.colors.pink)) as qa_demo:
    gr.Markdown("""<h1><center>Question Answer & Classification Demo</center></h1>""")
    with gr.Tab("Question Answer"):
        bot = gr.Chatbot(bubble_full_width=False, show_label=False,height=500) #.style(width=700, height=500, color_map=["blue", "green"])
        state = gr.State()
        txt = gr.Textbox(show_label=False, placeholder="Ask a question and press enter.")
        txt.submit(qa_bot, inputs=[txt, state], outputs=[bot, state])
    with gr.Tab("Document Classification"):
        with gr.Row():
            file_component = gr.File(label="Upload Single File", file_count="single")
            image_output = gr.Image()
        classify_button= gr.Button("Classify File")

if __name__ == "__main__":
    qa_demo.launch(share = False)