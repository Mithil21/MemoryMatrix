# import streamlit as st
# import requests

# st.set_page_config(page_title="Code Retriever", layout="wide")
# st.title("🧠 RAG Code Search & Generator")
# st.markdown("Upload a file to find relevant code snippets and their explanations.")

# # Upload file
# uploaded_file = st.file_uploader("📄 Upload your use-case file", type=["txt", "md", "py", "java"])

# # Submit
# if uploaded_file and st.button("🚀 Search Code"):
#     with st.spinner("Searching for relevant code..."):
#         files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
#         try:
#             response = requests.post("http://localhost:5000/search", files=files)
#             data = response.json()

#             if "results" in data:
#                 all_snippets = data["results"]
#                 languages = sorted(set(snippet.get("language", "Unknown") for snippet in all_snippets))
                
#                 st.info(f"**Summarized Use Case:**\n{data.get('summarized_use_case')}")

#                 # Filter dropdown
#                 selected_language = st.selectbox("Filter by language:", ["All"] + languages)

#                 filtered_snippets = all_snippets if selected_language == "All" else [
#                     s for s in all_snippets if s.get("language", "").lower() == selected_language.lower()
#                 ]

#                 for idx, item in enumerate(filtered_snippets, 1):
#                     lang = item.get('language', 'Unknown')
#                     st.subheader(f"🔹 Snippet {idx} ({lang})")
#                     st.code(item['code'], language=lang.lower() if lang else "text")
#                     st.caption(f"🔗 Source: {item['link']}")
#                     explanation = item.get("explanation", "No explanation available.")
#                     st.markdown(f"🧠 **Explanation:** {explanation}")
#             else:
#                 st.warning("No relevant code snippets found.")

#         except Exception as e:
#             st.error(f"Error: {e}")


import streamlit as st
import requests

st.set_page_config(page_title="Code Retriever", layout="wide")
st.title("🧠 Memory Matrix: A RAG-Based Approach to Boost Developer Productivity")
st.markdown("Upload a file to find relevant code snippets and their explanations.")

# Initialize session state for storing results
if "all_snippets" not in st.session_state:
    st.session_state.all_snippets = []
    st.session_state.summarized_use_case = ""

# Upload file
uploaded_file = st.file_uploader("📄 Upload your use-case file", type=["txt", "md", "py", "java"])

# Search and fetch snippets
if uploaded_file and st.button("🚀 Search Code"):
    with st.spinner("Searching for relevant code..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post("http://localhost:5000/search", files=files)
            data = response.json()

            if "results" in data:
                st.session_state.all_snippets = data["results"]
                st.session_state.summarized_use_case = data.get("summarized_use_case", "")
            else:
                st.warning("No relevant code snippets found.")
                st.session_state.all_snippets = []
                st.session_state.summarized_use_case = ""

        except Exception as e:
            st.error(f"Error: {e}")

# Display and filter snippets
if st.session_state.all_snippets:
    st.info(f"**Summarized Use Case:**\n{st.session_state.summarized_use_case}")

    all_snippets = st.session_state.all_snippets
    languages = sorted(set(s.get("language", "Unknown") for s in all_snippets))
    selected_language = st.selectbox("Filter by language:", ["All"] + languages)

    filtered_snippets = all_snippets if selected_language == "All" else [
        s for s in all_snippets if s.get("language", "").lower() == selected_language.lower()
    ]

    if not filtered_snippets:
        st.warning(f"No snippets found for language: {selected_language}")

    for idx, item in enumerate(filtered_snippets, 1):
        lang = item.get('language', 'Unknown')
        st.subheader(f"🔹 Snippet {idx} ({lang})")
        st.code(item['code'], language=lang.lower() if lang else "text")
        st.caption(f"🔗 Source: {item['link']}")
        explanation = item.get("explanation", "No explanation available.")
        st.markdown(f"🧠 **Explanation:** {explanation}")