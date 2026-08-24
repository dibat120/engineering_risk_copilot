import os

import requests
import streamlit as st


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Local development default.
# Later, when deployed, this can be replaced by an environment
# variable pointing to the public FastAPI backend on Render.
API_BASE_URL = os.getenv(
    "ENGINEERING_RISK_API_URL",
    "https://engineering-risk-copilot.onrender.com",
)

ASK_ENDPOINT = f"{API_BASE_URL}/ask"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Engineering Risk Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main page spacing */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero title */
    .hero-title {
        font-size: 2.7rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-bottom: 1.4rem;
    }

    /* Small status badge */
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.70rem;
        border-radius: 999px;
        background-color: rgba(34, 197, 94, 0.14);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: #4ade80;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Product information cards */
    .info-card {
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background-color: rgba(30, 41, 59, 0.30);
        height: 100%;
    }

    .info-card-title {
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .info-card-text {
        color: #aab3c2;
        font-size: 0.92rem;
    }

    /* Source cards */
    .source-card {
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.7rem;
        background-color: rgba(30, 41, 59, 0.35);
    }

    .source-name {
        font-weight: 700;
    }

    .source-meta {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #808897;
        font-size: 0.82rem;
        padding-top: 1.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("🛡️ Risk Copilot")

    st.caption(
        "Applied AI prototype for grounded engineering "
        "knowledge retrieval."
    )

    st.divider()

    st.subheader("Architecture")

    st.markdown(
        """
        **Streamlit UI**  
        ↓  
        **FastAPI REST API**  
        ↓  
        **RAG Pipeline**  
        ↓  
        **Semantic Retrieval**  
        ↓  
        **OpenAI LLM**
        """
    )

    st.divider()

    st.subheader("Current Capabilities")

    st.markdown(
        """
        - Document chunking
        - Embedding generation
        - Semantic retrieval
        - Context augmentation
        - Grounded generation
        - Source attribution
        - Guardrail / abstention
        """
    )

    st.divider()

    st.caption("Engineering Risk Copilot v0.2")


# ---------------------------------------------------------
# BACKEND HEALTH CHECK
# ---------------------------------------------------------

backend_online = False

try:

    health_response = requests.get(
        HEALTH_ENDPOINT,
        timeout=5,
    )

    if health_response.ok:
        backend_online = True

except requests.exceptions.RequestException:
    backend_online = False


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="hero-title">Engineering Risk Copilot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-subtitle">
        Grounded engineering knowledge retrieval using
        Retrieval-Augmented Generation (RAG).
    </div>
    """,
    unsafe_allow_html=True,
)


if backend_online:

    st.markdown(
        '<div class="status-badge">● AI Backend Online</div>',
        unsafe_allow_html=True,
    )

else:

    st.error(
        "FastAPI backend is offline. "
        "Start the API before submitting a question."
    )


# ---------------------------------------------------------
# PRODUCT VALUE CARDS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Grounded Answers</div>
            <div class="info-card-text">
                Responses are generated from retrieved engineering
                context rather than unrestricted model knowledge.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Traceable Sources</div>
            <div class="info-card-text">
                Retrieved document, chunk identifier and semantic
                similarity are preserved with every response.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">Grounding Guardrail</div>
            <div class="info-card-text">
                The Copilot can abstain when the available engineering
                evidence is insufficient.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# ---------------------------------------------------------
# QUESTION FORM
# ---------------------------------------------------------

st.subheader("Ask an Engineering Risk Question")

st.caption(
    "The Copilot searches the current engineering knowledge base "
    "before generating an answer."
)

with st.form("question_form"):

    question = st.text_area(
        "Engineering question",
        placeholder=(
            "Example: How can engineering risk be reduced?"
        ),
        height=130,
    )

    submitted = st.form_submit_button(
        "Ask Engineering Risk Copilot",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# CALL FASTAPI / RAG
# ---------------------------------------------------------

if submitted:

    if not question.strip():

        st.warning(
            "Please enter an engineering risk question."
        )

    elif not backend_online:

        st.error(
            "The FastAPI backend is currently unavailable."
        )

    else:

        with st.spinner(
            "Retrieving engineering evidence and generating a grounded response..."
        ):

            try:

                response = requests.post(
                    ASK_ENDPOINT,
                    json={
                        "question": question
                    },
                    timeout=60,
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No answer was returned by the API.",
                )

                sources = data.get(
                    "sources",
                    [],
                )


                # -------------------------------------------------
                # DETECT GUARDRAIL / ABSTENTION RESPONSE
                # -------------------------------------------------

                guardrail_message = (
                    "The available context does not contain enough "
                    "information to answer this question."
                )

                is_guardrail_response = (
                    guardrail_message.lower()
                    in answer.lower()
                )


                # -------------------------------------------------
                # DISPLAY ANSWER
                # -------------------------------------------------

                st.divider()

                if is_guardrail_response:

                    st.warning(
                        "Insufficient evidence — the Copilot "
                        "declined to generate an unsupported answer."
                    )

                else:

                    st.success(
                        "Grounded response generated from retrieved evidence."
                    )


                st.subheader("Answer")

                st.markdown(answer)


                # -------------------------------------------------
                # DISPLAY RETRIEVED SOURCES
                # -------------------------------------------------

                if sources:

                    st.subheader("Retrieved Evidence")

                    st.caption(
                        "Semantic similarity indicates how closely each "
                        "retrieved chunk matches the question."
                    )

                    for source in sources:

                        source_name = source.get(
                            "source",
                            "unknown",
                        )

                        chunk_id = source.get(
                            "chunk_id",
                            "unknown",
                        )

                        similarity = source.get(
                            "similarity",
                            0.0,
                        )

                        st.markdown(
                            f"""
                            <div class="source-card">
                                <div class="source-name">
                                    📄 {source_name}
                                </div>
                                <div class="source-meta">
                                    Chunk {chunk_id}
                                    &nbsp; • &nbsp;
                                    Similarity: {similarity:.4f}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the FastAPI backend."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )


            except requests.exceptions.RequestException as error:

                st.error(
                    f"API request failed: {error}"
                )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="footer">
        Engineering Risk Copilot • Applied AI Portfolio Prototype<br>
        RAG • FastAPI • Streamlit • OpenAI • Semantic Retrieval<br>
        August 2026
    </div>
    """,
    unsafe_allow_html=True,
)