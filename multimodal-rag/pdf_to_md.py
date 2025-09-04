import time
from pathlib import Path
from docling.document_converter import DocumentConverter


def parse_pdf(input_doc_path: Path, output_dir: Path):
    filename = input_doc_path.stem
    md_filepath = output_dir / f"{filename}-parsed-text.md"
    if md_filepath.exists():
        print(f"File {md_filepath} already exists. Skipping parsing.")
        return

    doc_converter = DocumentConverter()
    conv_res = doc_converter.convert(input_doc_path)

    # Save markdown
    print(f"Saving parsed text to {md_filepath}")
    with md_filepath.open("w", encoding="utf-8") as md_file:
        md_file.write(conv_res.document.export_to_markdown())


data_folder = Path("data")
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

input_pdfs = data_folder.glob("amazon*.pdf")

for input_pdf in input_pdfs:
    print(f"Processing file: {input_pdf.name}")
    start_time = time.time()
    input_doc_path = input_pdf
    parse_pdf(input_doc_path, output_dir)
    end_time = time.time() - start_time
    print(f"Document {input_pdf.name} processed in {end_time:.2f} seconds.")

