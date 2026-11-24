import streamlit as st
import spacy_streamlit

modelos = ["pt_core_news_sm", "pt_core_news_md", "pt_core_news_lg"]

texto_padrao = "Claro tem números abaixo da opradora Vivo"

spacy_streamlit.visualize(modelos, texto_padrao)

