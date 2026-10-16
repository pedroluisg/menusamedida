import streamlit as st

def configurar_pagina():
    st.set_page_config(
        page_title="Asistente de Cenas Familiares", 
        page_icon="🍲", 
        layout="centered"
    )
    
    # Estilos adaptativos modo claro/oscuro
    st.markdown("""
        <style>
        @media (prefers-color-scheme: dark) {
            .stMarkdown, p, li, span, h1, h2, h3 {
                color: #f3f4f6 !important;
            }
            div.stMarkdown div {
                color: #f3f4f6;
            }
        }
        @media (prefers-color-scheme: light) {
            .stMarkdown, p, li, span {
                color: #1f2937 !important;
            }
            h1, h2, h3 {
                color: #111827 !important;
            }
            div.stMarkdown div {
                color: #1f2937;
            }
        }
        </style>
    """, unsafe_allow_html=True)