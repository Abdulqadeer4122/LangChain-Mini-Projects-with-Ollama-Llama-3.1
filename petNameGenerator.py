import os
import dotenv
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import streamlit as st

dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def generate_pet_name(animal_type, pet_color):
    model = OllamaLLM(model="llama3.1")
    system_msg = "You are a helpful assistant , you can create the pet names"
    template = "I have a boy {animal_type} , general and palyfull, The color of my pet is {pet_color} and i want a cool name for that pet .please suggest me five name for that pet , only name , no description"
    prompt_template = ChatPromptTemplate.from_messages([("system", system_msg), ("human", template)])
    prompt = prompt_template.format_messages(animal_type=animal_type, pet_color=pet_color)
    response = model.invoke(prompt)
    return response


st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="PET NAME GENERATOR")
st.title("PET NAME GENERATOR")
pet_color=""
pet_name = st.sidebar.selectbox("Select your pet name", ("Cat", "Dog", "Cow", "Hamster", "Horse", "Fish"),
                                placeholder="Select your pet name")

if pet_name == "Cat":
    pet_color = st.sidebar.text_area("Enter The colors of cat with coma separation", max_chars=25)

if pet_name == "Dog":
    pet_color = st.sidebar.text_area("Enter The colors of Dog with coma separation", max_chars=25)

if pet_name == "Hamster":
    pet_color = st.sidebar.text_area("Enter The colors of Hamster", max_chars=15)
if st.sidebar.button("Generate Pet Name"):
    if pet_color:
        response = generate_pet_name(pet_name, pet_color)
        st.text(response)
