import streamlit as st

from llm_playground.rust_porting.compiler import compile_and_run, run_python
from llm_playground.rust_porting.config import LANGUAGE, MODELS, PYTHON_HARD
from llm_playground.rust_porting.porter import port

st.set_page_config(page_title=f"Port Python → {LANGUAGE}", layout="wide")
st.markdown("""
<style>
    /* Purple accent for primary buttons (Port to Rust) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #753991 !important;
        border-color: #753991 !important;
        color: white !important;
        font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: #5e2d75 !important;
        border-color: #5e2d75 !important;
    }

    /* Python output - blue tint */
    .py-out textarea {
        background: linear-gradient(180deg, rgba(32,157,215,.12), rgba(32,157,215,.06)) !important;
        border: 1px solid rgba(32,157,215,.35) !important;
        color: #209dd7 !important;
        font-weight: 600;
    }

    /* Rust output - gold tint */
    .lang-out textarea {
        background: linear-gradient(180deg, rgba(236,173,10,.15), rgba(236,173,10,.08)) !important;
        border: 1px solid rgba(236,173,10,.45) !important;
        color: #ecad0a !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title(f"Port Python → {LANGUAGE}")

# --- Model selector ---
model = st.selectbox("Model", MODELS)

# --- Code editors side by side ---
col_py, col_lang = st.columns(2)

with col_py:
    python_code = st.text_area("Python (original)", value=PYTHON_HARD, height=500)
    if st.button("Run Python"):
        with st.spinner("Running Python…"):
            st.session_state["py_out"] = run_python(python_code)

with col_lang:
    if "generated_code" not in st.session_state:
        st.session_state["generated_code"] = ""

    generated = st.text_area(
        f"{LANGUAGE} (generated)",
        value=st.session_state["generated_code"],
        height=500,
        key="lang_editor",
    )

    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button(f"Port to {LANGUAGE}", type="primary"):
            with st.spinner(f"Porting with {model}…"):
                st.session_state["generated_code"] = port(model, python_code)
                st.rerun()
    with btn2:
        if st.button(f"Run {LANGUAGE}"):
            with st.spinner(f"Compiling & running {LANGUAGE}…"):
                st.session_state["lang_out"] = compile_and_run(generated)

# --- Output panels ---
out_py, out_lang = st.columns(2)
# with out_py:
#     st.text_area("Python result", value=st.session_state.get("py_out", ""), height=200)
# with out_lang:
#     st.text_area(f"{LANGUAGE} result", value=st.session_state.get("lang_out", ""), height=200)
with out_py:
    st.markdown('<div class="py-out">', unsafe_allow_html=True)
    st.text_area("Python result", value=st.session_state.get("py_out", ""), height=200, key="py_out_display")
    st.markdown('</div>', unsafe_allow_html=True)
with out_lang:
    st.markdown('<div class="lang-out">', unsafe_allow_html=True)
    st.text_area(f"{LANGUAGE} result", value=st.session_state.get("lang_out", ""), height=200, key="lang_out_display")
    st.markdown('</div>', unsafe_allow_html=True)
