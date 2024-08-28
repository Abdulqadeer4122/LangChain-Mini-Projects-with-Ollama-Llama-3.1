import os
import dotenv
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import streamlit as st

dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def Translate(text, input_lang, output_lang):
    model = OllamaLLM(model="llama3.1")
    system_template = "you are a helpfull Assistant , Convert the below text from {input_lang} language  to {output_lang} language"
    template = "Text for converting is  in triple backticks ```{text}```"
    prompt_template = ChatPromptTemplate.from_messages([("system", system_template), ("human", template)])
    prompt = prompt_template.format_messages(input_lang=input_lang, output_lang=output_lang, text=text)
    response = model.invoke(prompt)
    return response


st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Translator")
st.title("Translator")

input_language = st.sidebar.selectbox("Select your Input Language", ("English", "French", "Roman Urdu", "hindhi"),
                                      key="input_language")
text = st.sidebar.text_area("Enter The colors of Hamster", max_chars=100)
output_language = st.sidebar.selectbox("Select your Input Language", (
"Select Language", "French", "Persian", "Pashto", "Punjabi", "Arabic", "English", "Roman Urdu", "hindhi"))
if st.sidebar.button("Translate", key="translate"):
    if input_language and output_language != "Select Language" and text:
        st.write(Translate(text, input_language, output_language))
