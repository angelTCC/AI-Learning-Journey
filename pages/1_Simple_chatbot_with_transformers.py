import streamlit as st
import time
import random

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Selecting the model. You will be using "facebook/blenderbot-400M-distill" in this example.
model_name = "facebook/blenderbot-400M-distill"

# Load the model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

st.title("Simple Chatbot with transformers")

# Define the chat function
def chat_with_bot(input_text):

    # Tokenize input and generate response
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_new_tokens=150) 
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # bot's response
    return response

# Streamed response
def response_generator(input_text):
    
    response = chat_with_bot(input_text)

    for word in response.split():
        yield word + " "
        time.sleep(0.08)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
