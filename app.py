# import streamlit as st
# import tempfile
# from pdf_loader import load_pdf
# from chunking import split_documents
# from vector_store import create_vector_store
# from rag_chain import get_answer
# from website_loader import load_website

# st.title("RAG PDF Chatbot")

# uploaded_file = st.file_uploader(
#     "Upload PDF",
#     type="pdf"
# )
# website_url = st.text_input(
#     "Enter Website URL"
# )
# question = st.text_input(
#     "Ask a Question"
# )

# if st.button("Submit"):
#     if uploaded_file is not None:
#         # PDF workflow
#         with tempfile.NamedTemporaryFile(
#             delete=False,
#             suffix=".pdf"
#         ) as tmp_file:
#             tmp_file.write(
#                 uploaded_file.getbuffer()
#             )
#             pdf_path = tmp_file.name
#         documents = load_pdf(pdf_path)

#     elif website_url:
#         # Website workflow
#         documents = load_website(
#             website_url
#         )

#     else:
#         st.error(
#             "Upload a PDF or enter a website URL"
#         )
#         st.stop()

#     chunks = split_documents(
#         documents
#     )
#     db = create_vector_store(
#         chunks
#     )
#     docs = db.similarity_search(
#         question,
#         k=3
#     )
#     answer = get_answer(
#         question,
#         docs
#     )
#     st.write(answer)



import streamlit as st
import tempfile

from pdf_loader import load_pdf
from website_loader import load_website
from chunking import split_documents
from vector_store import create_vector_store
from rag_chain import get_answer

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="RAG AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- HEADER ----------------

st.markdown("""
<h1 style='text-align:center; color:#4F8BF9;'>
🤖 RAG AI Assistant
</h1>

<h4 style='text-align:center;'>
Ask questions from PDFs or Websites using AI
</h4>
""", unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("📌 Instructions")

    st.markdown("""
    ### PDF Mode
    1. Upload a PDF
    2. Ask a question
    3. Get answers from the PDF

    ### Website Mode
    1. Enter website URL
    2. Ask a question
    3. Get answers from that website only
    """)

    st.success("Powered by Gemini + FAISS")

# ---------------- INPUT AREA ----------------

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

with col2:
    website_url = st.text_input(
        "🌐 Website URL",
        placeholder="https://example.com"
    )

question = st.text_area(
    "❓ Ask a Question",
    placeholder="What is this document about?"
)

# ---------------- SUBMIT BUTTON ----------------

submit = st.button(
    "🚀 Generate Answer",
    use_container_width=True
)

# ---------------- PROCESSING ----------------

if submit:

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Analyzing content..."):

        if uploaded_file is not None:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getbuffer()
                )

                pdf_path = tmp_file.name

            documents = load_pdf(pdf_path)

        elif website_url:

            documents = load_website(
                website_url
            )

        else:

            st.error(
                "Upload a PDF or enter a Website URL."
            )

            st.stop()

        chunks = split_documents(
            documents
        )

        db = create_vector_store(
            chunks
        )

        docs = db.similarity_search(
            question,
            k=3
        )

        answer = get_answer(
            question,
            docs
        )

    st.success("Answer Generated Successfully!")

    st.markdown("## 📖 Answer")

    st.info(answer)