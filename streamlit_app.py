
import streamlit as st
import fitz
import tempfile
from PIL import Image
import io

st.set_page_config(page_title="CheatSheet Generator", layout="centered")

st.title("📚 AI CheatSheet Generator")
st.write("Upload a lecture script PDF, and this app will generate a summarized cheat sheet.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

def extract_full_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)

    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc[page_index].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append((page_index + 1, img_index + 1, image))

    return images

if uploaded_file is not None:
    with st.spinner("🔍 Extracting and summarizing... please wait"):
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Run ETL process
        #summaries = generate_cheatsheet_from_pdf(tmp_path)
        text = extract_full_text(tmp_path)
        images = extract_images_from_pdf(tmp_path)

        if images:
            st.subheader("🖼️ Extracted Images")
            for page_num, img_num, img in images:
                st.markdown(f"**Page {page_num} – Image {img_num}**")
                st.image(img, use_column_width=True)
        else:
            st.info("No images found in the PDF.")
        st.success("✅ PDF Loaded!")
        st.subheader("📃 Full Content")
        st.text_area("PDF Text", text, height=600)

else:
    st.info("Please upload a PDF file to begin.")
