#!/usr/bin/env python3

# This script is a standalone utility to strip solution blocks from Jupyter notebooks.
#
# Requirements:
# - nbformat: You can install it via pip:
#   pip install nbformat
#
# Usage:
# python generate_student_notebooks.py
#
# This script finds all "*-complete.ipynb" files and creates student versions by
# removing the "-complete" suffix and stripping solution blocks.

# This script will strip sections of cells between
# '# BEGIN_SOLUTION' & '# END_SOLUTION' and
# replace it with '# ADD YOUR CODE HERE'
# to produce student-friendly versions of Jupyter notebooks
import nbformat
import re
import glob
import os


def strip_solutions_from_notebook(input_path, output_path):
    """
    Removes solution blocks from a Jupyter notebook and writes the result to output_path.
    Solution blocks are marked by '# BEGIN_SOLUTION' and '# END_SOLUTION'.
    """
    with open(input_path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = re.sub(
                r"# BEGIN_SOLUTION.*?# END_SOLUTION",
                "# ADD YOUR CODE HERE",
                cell.source,
                flags=re.DOTALL,
            )

    with open(output_path, "w") as f:
        nbformat.write(nb, f)


def main():
    # Find all *-complete.ipynb files in the current directory
    complete_notebooks = glob.glob("*-complete.ipynb")

    if not complete_notebooks:
        print("No *-complete.ipynb files found in the current directory.")
        return

    print(f"Found {len(complete_notebooks)} complete notebook(s):")

    for input_path in complete_notebooks:
        # Generate output path by removing "-complete" from the filename
        output_path = input_path.replace("-complete.ipynb", ".ipynb")

        print(f"  Processing: {input_path} -> {output_path}")
        strip_solutions_from_notebook(input_path, output_path)

    print(f"\nSuccessfully created {len(complete_notebooks)} student notebook(s)!")


if __name__ == "__main__":
    main()
