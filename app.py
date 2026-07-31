import streamlit as st
from utils.api_client import check_health, run_pipeline

# --- Page config ---
st.set_page_config(
    page_title="MediSync Intelligence",
    page_icon="🏥",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Pipeline Status")

    try:
        health = check_health()
        st.success("API online")
        st.caption(f"Whisper: {health['whisper']}")
        st.caption(f"FLAN-T5: {health['flan_t5']}")
    except Exception:
        st.error("API offline — is FastAPI running?")

    st.divider()
    st.caption("Models")
    st.caption("ASR: openai/whisper-base")
    st.caption("NLP: google/flan-t5-large")

# --- Main area ---
st.title("🏥 MediSync Intelligence")
st.caption("Upload a doctor-patient audio recording to generate a structured SOAP note.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload audio file",
    type=["mp3", "wav", "m4a"],
    help="Supports .mp3, .wav, .m4a — max 25MB"
)

if uploaded_file:
    st.audio(uploaded_file)   # lets you play the audio in browser

    run = st.button("▶ Run Pipeline", type="primary", use_container_width=True)

    if run:
        with st.spinner("Running pipeline — this takes 20-40 seconds..."):
            try:
                result = run_pipeline(
                    uploaded_file.getvalue(),
                    uploaded_file.name
                )
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                st.stop()

        st.success("Done!")

        # --- Latency metrics ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Transcription", f"{result['transcription_seconds']}s")
        col2.metric("Summarization", f"{result['summarization_seconds']}s")
        col3.metric(
            "Total",
            f"{round(result['transcription_seconds'] + result['summarization_seconds'], 2)}s"
        )

        st.divider()

        # --- Results side by side ---
        left, right = st.columns(2)

        with left:
            st.subheader("📝 Transcript")
            st.text_area(
                label="",
                value=result["transcript"],
                height=300,
                disabled=True
            )

        with right:
            st.subheader("🩺 SOAP Note")
            sections = result["sections"]

            with st.expander("S — Subjective", expanded=True):
                st.write(sections["subjective"])

            with st.expander("O — Objective", expanded=True):
                st.write(sections["objective"])

            with st.expander("A — Assessment", expanded=True):
                st.write(sections["assessment"])

            with st.expander("P — Plan", expanded=True):
                st.write(sections["plan"])