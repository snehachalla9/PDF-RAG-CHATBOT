import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunker import create_chunks
from utils.embeddings import create_embeddings
from utils.vector_store import create_vectorstore
from utils.retriver import retrieve_documents
from utils.llm import generate_answer


# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


# Title
st.title("PDF RAG Chatbot")


# Sidebar Settings
with st.sidebar:

    chunk_size = st.slider(
        "Chunk Size",
        200,
        2000,
        1000
    )

    chunk_overlap = st.slider(
        "Chunk Overlap",
        0,
        500,
        100
    )

    k = st.slider(
        "Retrieved Chunks",
        1,
        10,
        3
    )


# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=True
)


# Question
query = st.text_input(
    "Ask Question"
)


if uploaded_file:
    st.success(f"{len(uploaded_file)} PDFs Uploaded")
    all_docs=[]

    # Save PDF
    for pdf in uploaded_file:
        with open(pdf.name, "wb") as f:
            f.write(pdf.read())
        docs=load_pdf(pdf.name)
        for doc in docs:
            doc.metadata['source']=pdf.name
        all_docs.extend(docs)

    st.write('Total pages:',len(all_docs))

    # Chunking
    chunks = create_chunks(
        all_docs,
        chunk_size,
        chunk_overlap
    )

    st.write("Chunks:", len(chunks))
    st.subheader("All Chunks")
    for i, chunk in enumerate(chunks):
         st.write(f"Chunk {i+1}") 
         st.write(chunk.metadata) 
         st.write(chunk.page_content[:300]) 
         st.divider()


    # Embeddings
    embeddings = create_embeddings()


    # Vector Store
    db = create_vectorstore(
        chunks,
        embeddings
    )


    # Retrieval + Answer
    if query:

        docs_found = retrieve_documents(
            db,
            query,
            k
        )
        st.subheader("Retrieved Chunks")
        for i, doc in enumerate(docs_found):
            st.write(f"Chunk {i+1}")
            st.write(
                f"Source: {doc.metadata.get('source')}"
                )
            st.write(
                f"Page: {doc.metadata.get('page')}"
                  )
            st.write(doc.page_content)
            st.divider()

        answer = generate_answer(
            query,
            docs_found
        )
        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")
        pages = set()
        sources = set()
        for doc in docs_found:
            sources.add(
                (
                    doc.metadata.get("source"),
                    doc.metadata.get("page")
                    )
                    )
        for source, page in sources:
            st.write(
                f"File: {source} | Page: {page}"
                )


        # Chat History
        st.session_state.messages.append(
            {
                "question": query,
                "answer": answer
            }
        )

        st.subheader("Chat History")

        for msg in st.session_state.messages:
            st.write("Q:", msg["question"])
            st.write("A:", msg["answer"])
            st.divider()