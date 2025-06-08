import streamlit as st
import tempfile
import os
from converters import pdf_to_text, pdf_to_docx, pdf_to_html, pdf_to_images

st.set_page_config(page_title="PDF Converter", layout="centered")

# Load custom styles
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1>📄 PDF Converter</h1>", unsafe_allow_html=True)
st.markdown("<p>Convert PDF files to DOCX, TXT, HTML, or Images</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name

    output_format = st.selectbox("Select Output Format", ["DOCX", "TXT", "HTML", "PNG Images"])

    if st.button("Convert"):
        with st.spinner("Converting..."):
            if output_format == "TXT":
                text = pdf_to_text(pdf_path)
                st.download_button("Download TXT", text, file_name="output.txt")

            elif output_format == "DOCX":
                output_path = pdf_path.replace(".pdf", ".docx")
                pdf_to_docx(pdf_path, output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Download DOCX", f, file_name="output.docx")

            elif output_format == "HTML":
                output_path = pdf_path.replace(".pdf", ".html")
                pdf_to_html(pdf_path, output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Download HTML", f, file_name="output.html")

            elif output_format == "PNG Images":
                with tempfile.TemporaryDirectory() as tmp_dir:
                    images = pdf_to_images(pdf_path, tmp_dir)
                    for img_path in images:
                        st.image(img_path, use_column_width=True)
                        with open(img_path, "rb") as f:
                            st.download_button("Download Page", f, file_name=os.path.basename(img_path))

        os.unlink(pdf_path)
