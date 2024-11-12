import gradio as gr

# Define the input and output
text_input = gr.Textbox(label="User Input")
chatbot_response = gr.Textbox(label="Chatbot Response")

# Define the chatbot function
def chatbot(text):
    # Process the user input and generate a response
    response = "Hello, how can I help you?"
    return response

# Create the interface
interface = gr.Interface(fn=chatbot, inputs=text_input, outputs=chatbot_response)

# Launch the interface
interface.launch()