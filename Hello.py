import openai
import streamlit as st
from streamlit_chat import message

openai.api_type = "azure"
openai.api_base = "https://chatgpt-dp-innovation-dev.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "58d9c01f9ced46f480a5356bbb6d94da"

message_history= []
prompt = "tu es un assistant RH qui parle français et répond aux questions de RH. Tu dois être fiable et donner des détails. tu connais parfaitement le droit du travail et tu fais des réponses précises en n'hésitant pas a rapeler les articles du droit du travail français"

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": prompt}
    ]
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

st.title("Bureau RH")

st.sidebar.title("aide RH")
model_name = st.sidebar.radio("modèle :", ("GPT-4", "GPT-4 32k"))
if model_name == "GPT-4":
    model = "gpt-4"
else:
    model = "gpt-4-32k"
clear_button = st.sidebar.button("Repartir à 0", key="clear")

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": prompt}
    ]
    st.session_state['model_name'] = []

def generate_response(input_text):
    st.session_state['messages'].append({"role": "user", "content": input_text})
    response = openai.ChatCompletion.create(
        engine=model,
        messages = st.session_state['messages'],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    st.session_state['messages'].append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    return response['choices'][0]['message']['content']

response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Vos questions :", key='input', height=100)
        submit_button = st.form_submit_button(label='Envoyer')

    if submit_button and user_input:
        response = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(response)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))