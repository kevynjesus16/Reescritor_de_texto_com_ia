# app.py - VERSÃO 2.1 MODERNA (com Google Gemini)
import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA E CSS ---
st.set_page_config(page_title="Reescrevedor IA Moderno", page_icon="✨", layout="wide")

# CSS para o design moderno (o mesmo que aprovamos)
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' );
header, footer { visibility: hidden; }
body { font-family: 'Inter', sans-serif; }
.main-card { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 16px; padding: 2.5rem; max-width: 1100px; margin: 2rem auto; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
.main-card h1 { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
.main-card .subtitle { font-size: 1.1rem; color: #6c757d; text-align: center; margin-bottom: 3rem; }
.main-card h3 { font-size: 1rem; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1rem; }
div.stButton > button { background: linear-gradient(45deg, #6a11cb, #2575fc); color: white; border: none; padding: 14px 24px; border-radius: 8px; font-weight: 600; font-size: 1.1rem; width: fit-content; display: block; margin: 2rem auto 0 auto; }
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# --- CONEXÃO COM A API DO GOOGLE GEMINI ---
try:
    # Pega a chave dos "Secrets" do Streamlit
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Chave da API do Google não configurada. Por favor, adicione sua GOOGLE_API_KEY nos 'Secrets' do seu app no Streamlit Cloud.")
    st.stop()

# --- LAYOUT DA APLICAÇÃO ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h1>Reescrevedor de Texto IA</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transforme suas ideias em textos claros e impactantes.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h3>ORIGINAL</h3>", unsafe_allow_html=True)
        texto_original = st.text_area("Cole o texto aqui:", height=280, key="original_text", label_visibility="collapsed")
        estilo = st.selectbox("Escolha o estilo:", ("Padrão", "Formal", "Simples", "Criativo"), key="estilo_select", label_visibility="collapsed")
    with col2:
        st.markdown("<h3>REESCRITO</h3>", unsafe_allow_html=True)
        if 'texto_final' not in st.session_state:
            st.session_state.texto_final = "Aguardando..."
        st.text_area("Resultado:", value=st.session_state.texto_final, height=280, key="rewritten_text", label_visibility="collapsed")

    if st.button("✨ Reescrever Agora", key="rewrite_button"):
        if texto_original:
            prompt_completo = f"Reescreva o texto a seguir em um tom '{estilo}', mantendo a ideia central. Texto original: '{texto_original}'"
            
            with st.spinner("O Gemini está pensando... 🧠"):
                try:
                    response = model.generate_content(prompt_completo)
                    st.session_state.texto_final = response.text
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao chamar a API do Gemini: {e}")
        else:
            st.warning("Por favor, insira um texto para reescrever.")
    st.markdown('</div>', unsafe_allow_html=True)
