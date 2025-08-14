import streamlit as st
from PyPDF2 import PdfMerger
import io

def unificar_pdfs(lista_arquivos_pdf):
    """
    Unifica uma lista de arquivos PDF em um único objeto de bytes.
    Args:
        lista_arquivos_pdf (list): Lista de objetos de arquivo enviados pelo Streamlit.
    Returns:
        io.BytesIO: Objeto de bytes contendo o PDF unificado.
    """
    unificador = PdfMerger()
    for arquivo in lista_arquivos_pdf:
        # A API do Streamlit fornece os arquivos como objetos, então lemos os bytes
        # diretamente do buffer de memória.
        unificador.append(io.BytesIO(arquivo.read()))
    
    # Cria um buffer de memória para o arquivo de saída
    buffer_saida = io.BytesIO()
    unificador.write(buffer_saida)
    unificador.close()
    
    # Retorna o buffer para que o Streamlit possa fazer o download
    return buffer_saida.getvalue()


# --- Configuração da interface do Streamlit ---
st.set_page_config(
    page_title="Unificador de PDFs",
    page_icon="📄"
)

st.title("Unificador de PDFs")
st.markdown("---")
st.write("Selecione os arquivos PDF que você deseja unificar. Os arquivos serão unidos na ordem em que foram enviados.")


# --- Lógica da aplicação ---
# Usamos o file_uploader com accept_multiple_files=True para permitir vários arquivos
arquivos_enviados = st.file_uploader(
    "Escolha os arquivos PDF",
    type="pdf",
    accept_multiple_files=True
)

if arquivos_enviados:
    # Mostra a lista de arquivos para o usuário
    st.markdown("### Arquivos selecionados:")
    for i, arquivo in enumerate(arquivos_enviados):
        st.write(f"- {i+1}. {arquivo.name}")
    
    # Adiciona um botão de download para o arquivo unificado
    # O Streamlit cria automaticamente o botão quando fornecemos os dados
    if st.button("Unificar e Baixar PDF"):
        with st.spinner("Unificando PDFs..."):
            pdf_unificado = unificar_pdfs(arquivos_enviados)
        
        st.download_button(
            label="Clique para Baixar o PDF",
            data=pdf_unificado,
            file_name="PDF_unificado.pdf",
            mime="application/pdf",
        )
        st.success("PDFs unificados com sucesso! Use o botão acima para baixar.")

else:
    st.info("Aguardando o envio de arquivos PDF...")
