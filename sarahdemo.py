import streamlit as st
import requests
import json
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def get_response(question):
    response = requests.post("https://europe-west8-sarah-404819.cloudfunctions.net/saraheu", data=json.dumps({
                "latestmessage":question,
                "splenderai_id":"gNB2aKBzX1WX3CH2lX3B",
                "sender_name": st.session_state.uid,
                "sender_medium":"whatsapp"
    }), headers={'Content-Type': 'application/json'})
    return response.json()['output']


st.title("Sarah AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "uid" not in st.session_state:
    st.session_state.uid = generate_random_string(10)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = get_response(prompt)
        st.session_state.history.append(prompt)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
