import os
import json

def count_pdfs(folder_path):
    pdf_count = 0
    for root, dirs, files in os.walk(folder_path):  # Walk through all subfolders
        pdf_count += sum(1 for file in files if file.lower().endswith('.pdf'))  # Count PDFs
    return pdf_count

# Replace this with the path to your dataset
folder_path = "D:\\IR Anthology Dataset"  # Folder to scan for PDFs
pdf_count = count_pdfs(folder_path)

# Create the JSON data for Shields.io
pdf_status = {
    "schemaVersion": 1,
    "label": "PDFs",
    "message": str(pdf_count),
    "color": "blue"
}

# Save the JSON file in the repository folder
output_path = os.path.join(os.getcwd(), "pdf_status.json")  # Save in the repo's root directory
with open(output_path, "w") as f:
    json.dump(pdf_status, f)

print(f"PDF count saved to {output_path}")
