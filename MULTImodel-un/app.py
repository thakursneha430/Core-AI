import streamlit as st
from pathlib import Path
import html

from src.utils.file_handler import save_uploaded_file
from src.pipeline.document_pipeline import DocumentPipeline
from src.rag.rag_pipeline import RAGPipeline


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="CORE AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>
    /* Main application */

    .stApp {
        background-color: #f6f7fb;
        color: #111827;
        font-family: "Segoe UI", sans-serif;
    }

    [data-testid="stHeader"] {
        background-color: #f6f7fb;
    }

    .block-container {
        max-width: 1600px;
        padding: 2rem 2rem 3rem 2rem;
    }

    /* Application title */

    .main-title {
        font-size: 34px;
        font-weight: 750;
        color: #24334d !important;
        margin-bottom: 8px;
        letter-spacing: -0.8px;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b !important;
        margin-bottom: 28px;
    }

    /* Cards */

    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }

    .section-heading {
        font-size: 19px;
        font-weight: 700;
        color: #24334d !important;
        margin: 0;
    }

    /* Chat messages */

    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }

    /* Force chat text to black */

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
        color: #111827 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4 {
        color: #111827 !important;
    }

    /* Chat input */

    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 1px solid #d8deea !important;
        border-radius: 14px !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #7967ed !important;
        box-shadow: 0 0 0 2px rgba(121, 103, 237, 0.12);
    }

    [data-testid="stChatInput"] textarea {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        background-color: #ffffff !important;
        caret-color: #6d5ce8 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    /* PDF uploader */

    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 1.5px dashed #c7cde0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        transition: border-color 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #7967ed !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
    }

    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {
        color: #334155 !important;
    }

    /* Buttons */

    .stButton > button {
        min-height: 42px;
        border-radius: 10px;
        border: 1px solid #e0e4ed;
        background-color: #ffffff;
        color: #334155;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #7967ed;
        color: #6554d8;
        background-color: #f8f7ff;
    }

    .stButton > button[kind="primary"] {
        background-color: #6d5ce8 !important;
        color: #ffffff !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #5948d6 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(109, 92, 232, 0.2);
    }

    /* Tabs */

    button[data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600;
        font-size: 15px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #6d5ce8 !important;
    }

    [data-baseweb="tab-highlight"] {
        background-color: #6d5ce8 !important;
    }

    /* Source expander */

    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: #111827 !important;
    }

    /* General text */

    .stMarkdown p,
    .stMarkdown li {
        color: #111827;
    }

    [data-testid="stAlert"] p {
        color: #111827 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #64748b !important;
    }

    /* Scrollbar */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f6f7fb;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Hide footer */

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "active_file_path" not in st.session_state:
    st.session_state.active_file_path = None

if "active_file_name" not in st.session_state:
    st.session_state.active_file_name = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_upload_directory():
    return Path("data") / "uploads"


def get_uploaded_pdfs():
    upload_dir = get_upload_directory()

    if not upload_dir.exists():
        return []

    return sorted(
        upload_dir.glob("*.pdf"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def process_document(uploaded_file):
    """Save and process an uploaded PDF."""

    try:
        with st.spinner("Processing your PDF document..."):
            file_path = save_uploaded_file(uploaded_file)

            pipeline = DocumentPipeline()
            pipeline.process(file_path)

        st.session_state.document_processed = True
        st.session_state.active_file_path = str(file_path)
        st.session_state.active_file_name = uploaded_file.name
        st.session_state.chat_history = []

        st.success(
            f"✅ {uploaded_file.name} is ready for questions!"
        )

    except Exception as exc:
        st.error("The document could not be processed.")
        st.exception(exc)


def display_sources(sources):
    """Display retrieved sources and remove exact duplicates."""

    if not sources:
        return

    seen = set()
    unique_sources = []

    for source in sources:
        if not isinstance(source, dict):
            continue

        text = str(source.get("text", "")).strip()
        metadata = source.get("metadata", {})

        if not isinstance(metadata, dict):
            metadata = {}

        page = (
            metadata.get("page")
            or metadata.get("page_number")
            or metadata.get("page_num")
        )

        key = (text, str(page))

        if key not in seen:
            seen.add(key)
            unique_sources.append((text, page))

    if not unique_sources:
        return

    with st.expander(
        f"📚 Retrieved Sources ({len(unique_sources)})",
        expanded=False,
    ):
        for index, (source_text, page) in enumerate(
            unique_sources,
            start=1,
        ):
            st.markdown(f"**Source {index}**")

            if page is not None:
                st.caption(f"Page: {page}")

            if source_text:
                st.write(source_text)
            else:
                st.caption("Source text is unavailable.")

            if index < len(unique_sources):
                st.divider()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown(
    '<div class="main-title"> CORE AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Upload PDF documents and ask questions about them in real time.'
    '</div>',
    unsafe_allow_html=True,
)


# ==========================================================
# MAIN TWO-COLUMN LAYOUT
# ==========================================================

left_column, right_column = st.columns(
    [0.38, 0.62],
    gap="large",
)


# ==========================================================
# LEFT SIDE: DOCUMENTS
# ==========================================================

with left_column:

    st.markdown(
        """
        <div class="section-card">
            <p class="section-heading"> Documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    upload_tab, library_tab = st.tabs(["Upload", "Library"])

    # ------------------------------------------------------
    # UPLOAD TAB
    # ------------------------------------------------------

    with upload_tab:


        st.caption(
            "Choose a PDF to add it to your workspace "
            "and start asking questions."
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF",
            type=["pdf"],
            key="pdf_uploader",
            label_visibility="collapsed",
        )

        if uploaded_file is not None:

            if st.button(
                "Process Document",
                type="primary",
                use_container_width=True,
            ):
                process_document(uploaded_file)

        if st.session_state.active_file_name:

            st.divider()

            st.markdown("**Current document**")

            st.markdown(
                f"📄 {html.escape(st.session_state.active_file_name)}"
            )

            if st.session_state.document_processed:
                st.success("Document ready for questions.")

    # ------------------------------------------------------
    # LIBRARY TAB
    # ------------------------------------------------------

    with library_tab:

        st.markdown("### Document Library")

        st.caption(
            "PDF files saved in your project's uploads folder."
        )

        pdf_files = get_uploaded_pdfs()

        if not pdf_files:

            st.info(
                "No saved PDFs found yet. Upload a PDF to get started."
            )

        else:

            for pdf_path in pdf_files:

                file_col, button_col = st.columns(
                    [0.72, 0.28],
                    vertical_alignment="center",
                )

                with file_col:
                    st.markdown(
                        f"📄 **{html.escape(pdf_path.name)}**"
                    )

                with button_col:

                    if st.button(
                        "Select",
                        key=f"select_{pdf_path.name}",
                        use_container_width=True,
                    ):

                        st.session_state.active_file_path = str(
                            pdf_path
                        )

                        st.session_state.active_file_name = (
                            pdf_path.name
                        )

                        st.session_state.document_processed = True
                        st.session_state.chat_history = []

                        st.success(
                            f"Selected {pdf_path.name}"
                        )

                        st.rerun()


# ==========================================================
# RIGHT SIDE: CHAT ASSISTANT
# ==========================================================

with right_column:

    header_col, clear_col = st.columns(
        [0.76, 0.24],
        vertical_alignment="center",
    )

    with header_col:

        st.markdown(
            """
            <div class="section-card">
                <p class="section-heading"> Chat Assistant</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with clear_col:

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):
            st.session_state.chat_history = []
            st.rerun()

    # ------------------------------------------------------
    # WELCOME MESSAGE
    # ------------------------------------------------------

    if not st.session_state.chat_history:

        if st.session_state.document_processed:

            st.info(
                f"Your document is ready: "
                f"{st.session_state.active_file_name or 'Selected PDF'}"
            )

            st.markdown("**Try asking:**")

            st.markdown(
                """
                - Summarize this document.
                - What are the main topics?
                - What are the important details?
                """
            )

        else:

            st.info(
                "Upload and process a PDF on the left "
                "before asking questions."
            )

    # ------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # ------------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":
                display_sources(message.get("sources", []))

    # ------------------------------------------------------
    # QUESTION INPUT
    # ------------------------------------------------------

    prompt = st.chat_input(
        "Ask a question about your document..."
    )

    if prompt:

        if not st.session_state.document_processed:

            st.warning(
                "Please upload and process a PDF before asking questions."
            )

        else:

            # Display and save the user's question.

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            try:

                with st.chat_message("assistant"):

                    with st.spinner("Finding the answer..."):

                        rag_pipeline = RAGPipeline()
                        response = rag_pipeline.ask(prompt)

                        if isinstance(response, dict):

                            answer = response.get(
                                "answer",
                                "I couldn't generate an answer.",
                            )

                            sources = response.get("sources", [])

                        else:

                            answer = str(response)
                            sources = []

                    # Display the answer in black.

                    st.markdown(str(answer))

                    # Display the retrieved sources.

                    display_sources(sources)

                # Save the answer for future reruns.

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": str(answer),
                        "sources": sources,
                    }
                )

            except Exception as exc:
                error_message = str(exc)
                normalized_error = error_message.upper()

                if "503" in normalized_error or "UNAVAILABLE" in normalized_error:
                    st.warning(
                        "CORE AI is temporarily busy. Please wait a moment "
                        "and try again."
                    )
                elif "429" in normalized_error or "RESOURCE_EXHAUSTED" in normalized_error:
                    st.warning(
                        "CORE AI has reached its API usage limit. "
                        "Please try again later."
                    )
                else:
                    st.error("CORE AI could not answer this question.")
                    st.error(error_message)
