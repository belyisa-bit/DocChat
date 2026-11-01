import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="DocChat - Consulta de Documentos",
    page_icon="📚",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("📚 DocChat - Assistente RAG")
st.caption("Faça upload dos seus documentos e faça perguntas contextualizadas.")

# Sidebar para upload de ficheiros
with st.sidebar:
    st.header("⚙️ Ingestão de Documentos")
    uploaded_file = st.file_uploader(
        "Selecione um ficheiro (PDF, TXT, MD)",
        type=["pdf", "txt", "md"]
    )
    
    if st.button("Processar Documento", type="primary"):
        if uploaded_file is not None:
            with st.spinner("A indexar documento no ChromaDB..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{API_URL}/documents", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ {data['message']} ({data['chunks_created']} chunks criados)")
                    else:
                        st.error(f"❌ Erro ({response.status_code}): {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"❌ Falha de ligação com a API: {str(e)}")
        else:
            st.warning("Por favor, selecione um ficheiro primeiro.")

# Histórico de Chat na Sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("📌 Fontes Consultadas"):
                for cite in msg["citations"]:
                    st.markdown(f"- **Doc:** `{cite['document_id']}` | **Pág:** `{cite['page_number']}`")
                    st.caption(f"_{cite['snippet']}_")

# Input de pergunta do utilizador
if prompt := st.chat_input("Faça uma pergunta sobre os documentos..."):
    # Exibe a pergunta do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Requisita a resposta à API FastAPI
    with st.chat_message("assistant"):
        with st.spinner("A consultar contexto e a gerar resposta..."):
            try:
                payload = {"question": prompt, "top_k": 3}
                response = requests.post(f"{API_URL}/ask", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    citations = data.get("citations", [])
                    
                    st.write(answer)
                    if citations:
                        with st.expander("📌 Fontes Consultadas"):
                            for cite in citations:
                                st.markdown(f"- **Doc:** `{cite['document_id']}` | **Pág:** `{cite['page_number']}`")
                                st.caption(f"_{cite['snippet']}_")
                    
                    # Guarda no histórico
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "citations": citations
                    })
                else:
                    st.error(f"Erro na API: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Falha ao comunicar com a API: {str(e)}")