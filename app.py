import os
import requests
import streamlit as st
import pandas as pd
import google.generativeai as genai
from safety_filter import analyze_text
from gemini_helper import generate_response
from utils.logger import log_interaction

# Load API keys from Streamlit Secrets or local .env fallback
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
PERSPECTIVE_KEY = st.secrets.get("PERSPECTIVE_API_KEY", os.getenv("PERSPECTIVE_API_KEY"))
genai.configure(api_key=GEMINI_KEY)

# Configure the Streamlit page
st.set_page_config(page_title="Safe Student AI", page_icon="🧠", layout="centered")

# Title and introduction text
st.title("🧑‍🎓 Safe Student AI Assistant")
st.write("Built with Gemini 2.5 Flash + Perspective API for safe, educational chats.")

# sidebar for logs
st.sidebar.header("📘 Chat Log Viewer")
if st.sidebar.button("Refresh Logs"):
    try:
        df=pd.read_csv("data/prompts_log.csv")
        st.sidebar.dataframe(df.tail(5))      # Display last 5 logs
    except FileNotFoundError:
        st.sidebar.warning("No logs yet. Start chatting!")

# Safety Sloider
st.subheader("Safety Level 🔒")
threshold = st.slider("Choose moderation strictness",0.1, 0.9, 0.4, 0.1)
st.caption(f"Message above{threshold:.2f} are blocked.")

# Input box where user types the question
user_input = st.text_area("Ask me anything related to your studies:")

# Button triggers the processing flow
if st.button("Ask"):
    if user_input.strip():
        scores = analyze_text(user_input)
        toxicity = scores["TOXICITY"]

        # Visual progress bar for toxicity
        st.progress(toxicity)
        st.write(f"**Toxicity Score:** {toxicity:.2f}")

        # Show all category scores
        with st.expander("Detailed Safety Report"):
            for k, v in scores.items():
                st.write(f"**{k.title()}:** {v:.2f}")

        # Route message
        if toxicity < threshold:
            response = generate_response(user_input)
            st.success(response)
        else:
            response = "⚠️ Message blocked for safety reasons."
            st.warning(response)

        # Log result
        log_interaction(user_input, response, toxicity)