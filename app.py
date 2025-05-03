import streamlit as st
import requests

st.set_page_config(page_title="Code Retriever", layout="wide")

st.title("🧠 RAG Code Search & Generator")

st.markdown("Upload a file and enter a prompt to find relevant code snippets.")

# Upload file
uploaded_file = st.file_uploader("📄 Upload your use-case file", type=["txt", "md", "py", "java"])

# Prompt
prompt = st.text_input("🔍 Enter your specific prompt (what you're looking for):", "")

# Submit
if uploaded_file and prompt and st.button("🚀 Search Code"):
    with st.spinner("Searching for relevant code..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"prompt": prompt}
        try:
            response = requests.post("http://localhost:5000/search", files=files, data=data)
            results = response.json().get("results", [])

            if results:
                for idx, item in enumerate(results, 1):
                    st.code(item['code'], language="java")
                    st.caption(f"🔗 Source: `{item['link']}`")
            else:
                st.warning("No relevant code snippets found.")

        except Exception as e:
            st.error(f"Error: {e}")
