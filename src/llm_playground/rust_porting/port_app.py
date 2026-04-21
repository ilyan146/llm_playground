import streamlit as st

from llm_playground.rust_porting.compiler import compile_and_run, run_python
from llm_playground.rust_porting.config import LANGUAGE, MODELS, PYTHON_HARD
from llm_playground.rust_porting.porter import port
from pathlib import Path

ICONS = Path(__file__).parent / "icons"

st.set_page_config(page_title=f"Port Python → {LANGUAGE}", layout="wide")
# st.title(f"Port Python → {LANGUAGE}")
header_col, _ = st.columns([2, 10])
with header_col:
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        st.image(str(ICONS / "python.png"), width=60)
    with c2:
        st.image(str(ICONS / "arrow2.png"), width=60)
    with c3:
        st.image(str(ICONS / "rust_icon2.png"), width=60)

# --- Model selector ---
model = st.selectbox("Model", MODELS)

# --- Code editors side by side ---
col_py, col_lang = st.columns(2)

with col_py:
    st.subheader("Python (original)")
    with st.container(height=500):
        st.code(PYTHON_HARD, language="python")
    python_code = PYTHON_HARD
    if st.button("Run Python"):
        with st.spinner("Running Python…"):
            st.session_state["py_out"] = run_python(python_code)

with col_lang:
    st.subheader(f"{LANGUAGE} (generated)")
    with st.container(height=500):
        generated = st.session_state.get("lang_editor", "")
        if generated:
            st.code(generated, language="rust")
        else:
            st.code("", language="rust")

    btn1, _, btn2 = st.columns([2, 6, 2])
    with btn1:
        if st.button(f"Port to {LANGUAGE}", type="primary", use_container_width=True):
            st.session_state["lang_out"] = ""
            st.session_state["lang_editor"] = ""
            st.session_state["do_port"] = True
            st.rerun()
    with btn2:
        if st.button(f"Run {LANGUAGE}", type="secondary", use_container_width=True):
            with st.spinner(f"Compiling & running {LANGUAGE}…"):
                st.session_state["lang_out"] = compile_and_run(generated)

# --- Output panels ---
out_py, out_lang = st.columns(2)
with out_py:
    py_result = st.session_state.get("py_out", "")
    if py_result:
        st.info("Python result")
        st.code(py_result, language=None)
    else:
        st.text_area("Python result", value="", height=200, disabled=True)

with out_lang:
    lang_result = st.session_state.get("lang_out", "")
    if lang_result:
        st.warning(f"{LANGUAGE} result")
        st.code(lang_result, language=None)
    else:
        st.text_area(f"{LANGUAGE} result", value="", height=200, disabled=True)

# --- Deferred porting (phase 2: runs after UI renders with cleared state) ---
if st.session_state.get("do_port"):
    st.session_state["do_port"] = False
    with col_lang:
        with st.spinner(f"Porting with {model}…"):
            st.session_state["lang_editor"] = port(model, python_code)
            st.rerun()