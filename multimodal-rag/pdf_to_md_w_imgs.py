from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode
from pathlib import Path

data_folder = Path("data/pdfs")
output_dir = Path("data/parsed")
output_dir.mkdir(parents=True, exist_ok=True)


IMAGE_RESOLUTION_SCALE = 2.0


def parse_pdf_with_images(input_doc_path: Path, output_dir: Path):
    # Reference: https://docling-project.github.io/docling/examples/export_figures/
    md_filename = output_dir / f"{input_doc_path.name.split('.')[0]}-parsed-w-imgs.md"
    if md_filename.exists():
        print(f"Skipping {md_filename} as it already exists.")
        return

    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
    pipeline_options.generate_picture_images = True

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    conv_res = doc_converter.convert(input_doc_path)

    # Save markdown with referenced pictures
    conv_res.document.save_as_markdown(md_filename, image_mode=ImageRefMode.REFERENCED)


pdf_names = [
    f.name for f in data_folder.glob("*.pdf") if "amazon" not in f.name.lower()
]

for pdf_fname in pdf_names:
    print(f"Processing file: {pdf_fname}")

    input_doc_path = data_folder / pdf_fname

    print(f"Converting document {input_doc_path} to multimodal pages...")
    parse_pdf_with_images(input_doc_path, output_dir)
