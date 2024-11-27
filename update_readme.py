import json
import os

def generate_html_table(data):
    """Generate a simplified HTML table with hierarchical structure and no redundant titles."""
    html_table = """
<table>
  <tbody>
    <tr>
      <td><b>Total PDFs</b></td>
      <td><img src="https://img.shields.io/badge/Total_PDFs-{pdf_count}-blue" alt="Total PDFs"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">PDFs in 'conf'</td>
      <td><img src="https://img.shields.io/badge/Conf_PDFs-{pdf_count_conf}-blue" alt="Conf PDFs"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">PDFs in 'jrnl'</td>
      <td><img src="https://img.shields.io/badge/Jrnl_PDFs-{pdf_count_jrnl}-blue" alt="Jrnl PDFs"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">Processed PDFs</td>
      <td><img src="https://img.shields.io/badge/Processed_PDFs-{processed_pdf_count}-green" alt="Processed PDFs"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">Unprocessed PDFs</td>
      <td><img src="https://img.shields.io/badge/Unprocessed_PDFs-{unprocessed_pdf_count}-red" alt="Unprocessed PDFs"></td>
    </tr>
    <tr>
      <td><b>Total .bib Entries</b></td>
      <td><img src="https://img.shields.io/badge/Total_Bib-{bib_total_count}-orange" alt="Total Bib"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">.bib Entries in 'conf'</td>
      <td><img src="https://img.shields.io/badge/Conf_Bib-{bib_conf_count}-orange" alt="Conf Bib"></td>
    </tr>
    <tr>
      <td style="padding-left: 20px;">.bib Entries in 'jrnl'</td>
      <td><img src="https://img.shields.io/badge/Jrnl_Bib-{bib_jrnl_count}-orange" alt="Jrnl Bib"></td>
    </tr>
  </tbody>
</table>
    """.format(**data)
    return html_table

def update_readme(reference_file, readme_file):
    """Update the README.md file with the latest counts."""
    # Ensure the reference JSON file exists
    if not os.path.exists(reference_file):
        print(f"Reference file {reference_file} not found.")
        return

    # Load data from the reference file
    with open(reference_file, 'r') as file:
        data = json.load(file)

    # Generate the HTML table
    html_table = generate_html_table(data)

    # Ensure the README.md file exists
    if not os.path.exists(readme_file):
        print(f"README file {readme_file} not found. Creating a new one.")
        with open(readme_file, 'w') as file:
            file.write(f"<!--- START COUNT TABLE --->\n{html_table}\n<!--- END COUNT TABLE --->\n")
        return

    # Read the existing README.md content
    with open(readme_file, 'r') as file:
        readme_content = file.readlines()

    # Locate the table section
    start_marker = "<!--- START COUNT TABLE --->\n"
    end_marker = "<!--- END COUNT TABLE --->\n"

    start_index = None
    end_index = None

    for i, line in enumerate(readme_content):
        if line.strip() == start_marker.strip():
            start_index = i
        if line.strip() == end_marker.strip():
            end_index = i

    # Replace the section or append if markers are not found
    if start_index is not None and end_index is not None:
        updated_content = (
            readme_content[: start_index + 1]
            + [html_table + "\n"]
            + readme_content[end_index:]
        )
    else:
        print("Markers not found in README.md. Adding table at the end.")
        updated_content = readme_content + ["\n"] + [start_marker] + [html_table + "\n"] + [end_marker]

    # Write back to README.md
    with open(readme_file, 'w') as file:
        file.writelines(updated_content)

    print("README.md updated successfully!")

def main():
    # Define paths
    reference_file = "dataset_count_reference.json"  # Adjust path if needed
    readme_file = "README.md"  # Adjust path if needed

    # Update the README with the latest data
    update_readme(reference_file, readme_file)

if __name__ == "__main__":
    main()
