from pathlib import Path
import pymupdf
import math
import argparse


def convert_pdf_to_images(src_file_path: Path, img_path: Path) -> list[Path]:
    """
    Convert PDF pages to JPG images using PyMuPDF.

    Args:
        src_file_path: Path to the PDF file
        img_path: Directory to save the images

    Returns:
        List of paths to the created image files
    """
    # Ensure output directory exists
    img_path.mkdir(parents=True, exist_ok=True)

    tgt_file_path_prefix = src_file_path.stem

    # Open PDF document
    doc = pymupdf.open(str(src_file_path))
    page_count = doc.page_count

    digits = int(math.log10(page_count)) + 1
    img_paths = []

    for i in range(page_count):
        # Load page
        page = doc[i]

        # Create pixmap (image) from page
        # matrix=pymupdf.Matrix(2, 2) gives 2x zoom for better quality
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))

        # Generate filename
        img_file_path = (
            img_path / f"{tgt_file_path_prefix}_{i+1:0{digits}d}_of_{page_count}.jpg"
        )

        # Save image
        pix.save(str(img_file_path))
        img_paths.append(img_file_path)

        # Clean up
        pix = None

    # Close document
    doc.close()
    return img_paths


# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF files to images")
    parser.add_argument(
        "pattern",
        nargs="?",
        default="*.pdf",
        help="File pattern to match PDF files (default: *.pdf)"
    )
    args = parser.parse_args()

    pdf_paths = Path("data/pdfs").glob(args.pattern)
    for pdf_path in pdf_paths:
        print(f"Converting {pdf_path} to images...")
        img_dir = Path("data/imgs")
        image_paths = convert_pdf_to_images(pdf_path, img_dir)
        print(f"Converted {len(image_paths)} pages to images")
