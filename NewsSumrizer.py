import streamlit as st
import requests
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from typing import List, Dict

import dotenv
import os
dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

news_api_key = os.getenv("NEWS_API_KEY")

def fetch_news(query: str) -> List[Dict]:
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    return articles



def summarize_text(text: str) -> str:
    template = "Summarize the following text: {text}"
    prompt_template = ChatPromptTemplate.from_template(template=template)
    prompt=prompt_template.format_messages(text=text)
    model = OllamaLLM(model="llama3.1")  # Adjust temperature for creativity
    response=model.invoke(prompt)

    return response



def categorize_summary(summary: str) -> str:
    categories = ["Technology", "Health", "Finance", "Sports", "Entertainment", "Science"]
    template = "Categorize the following text into one of these categories: {categories}. Text: {text}"
    prompt_template = ChatPromptTemplate.from_template(template=template)
    prompt=prompt_template.format_messages(categories=", ".join(categories),text=summary)
    model = OllamaLLM(model="llama3.1")  # Adjust temperature for creativity
    response = model.invoke(prompt)
    return response



st.title("News Summarizer & Categorizer")
query = st.text_input("Enter a topic or keyword", "")

if st.button("Fetch and Summarize News"):
    if query:
        st.write(f"Fetching news for: {query}")
        articles = fetch_news(query)
        if articles:
            st.write(f"Found {len(articles)} articles.")
            st.write(f"Top Five News about {query}")
            for article in articles[:5]:
                title = article.get("title")
                content = article.get("content")
                source = article.get("source", {}).get("name")

                if content:
                    st.subheader(title)
                    st.write(f"**Source:** {source}")

                    # Generate summary
                    summary = summarize_text(content)
                    st.write(f"**Summary:** {summary}")

                    # Categorize summary
                    category = categorize_summary(summary)
                    st.write(f"**Category:** {category}")
                    st.write("---")
        else:
            st.write("No articles found. Please try a different query.")
    else:
        st.write("Please enter a topic or keyword.")
