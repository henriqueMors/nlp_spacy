import streamlit as st
import spacy_streamlit

# Compatibilidade: o spacy-streamlit ainda usa o nome antigo do comando
if not hasattr(st, "experimental_rerun"):
    st.experimental_rerun = st.rerun

modelos = ["pt_core_news_sm", "pt_core_news_md", "pt_core_news_lg"]
texto_padrao = "Claro tem números abaixo da operadora Vivo"

spacy_streamlit.visualize(modelos, texto_padrao)