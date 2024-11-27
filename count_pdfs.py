import os
import bibtexparser
import json

def count_pdfs_and_jsons(directory):
    """Counts PDFs and JSON files, matches them, and identifies unmatched PDFs."""
    pdf_files = []
    json_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(file)
            elif file.endswith(".json"):
                json_files.append(file)

    pdf_base_names = {os.path.splitext(file)[0] for file in pdf_files}
    json_base_names = {os.path.splitext(file)[0] for file in json_files}
    unmatched_pdfs = pdf_base_names - json_base_names

    total_pdfs = len(pdf_files)
    total_processed = len(pdf_base_names - unmatched_pdfs)
    total_unprocessed = len(unmatched_pdfs)

    return total_pdfs, total_processed, total_unprocessed

def count_pdfs_in_subfolders(directories):
    """Counts PDFs in specified subfolders."""
    pdf_counts = {}
    for directory in directories:
        pdf_count = 0
        for root, _, files in os.walk(directory):
            pdf_count += sum(1 for file in files if file.endswith(".pdf"))
        pdf_counts[directory] = pdf_count
    return pdf_counts

def count_bib_entries_with_mod_times(directory, previous_mod_times):
    """Counts entries in .bib files and tracks their modification times."""
    total_entries = 0
    current_file_data = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".bib"):
                bib_file_path = os.path.join(root, file)
                try:
                    mod_time = os.path.getmtime(bib_file_path)

                    if (
                        bib_file_path not in previous_mod_times
                        or mod_time > previous_mod_times.get(bib_file_path, {}).get("mod_time", 0)
                    ):
                        with open(bib_file_path, 'r') as bibtex_file:
                            bib_database = bibtexparser.load(bibtex_file)
                            entry_count = len(bib_database.entries)
                        current_file_data[bib_file_path] = {
                            "mod_time": mod_time,
                            "entry_count": entry_count,
                        }
                        total_entries += entry_count
                    else:
                        total_entries += previous_mod_times[bib_file_path]["entry_count"]
                        current_file_data[bib_file_path] = previous_mod_times[bib_file_path]
                except Exception as e:
                    print(f"Error reading {bib_file_path}: {e}")

    return total_entries, current_file_data

def clean_cache(previous_data, current_file_data):
    """Removes entries for deleted files from the cache."""
    return {
        file_path: details
        for file_path, details in previous_data.items()
        if file_path in current_file_data
    }

def check_and_update_counts(main_directory, reference_file):
    """Combines PDF and .bib entry counts with caching."""
    conf_directory = os.path.join(main_directory, 'conf')
    jrnl_directory = os.path.join(main_directory, 'jrnl')

    # Load cached data
    if os.path.exists(reference_file):
        with open(reference_file, 'r') as file:
            reference_data = json.load(file)
    else:
        reference_data = {
            "pdf_count": 0,
            "pdf_count_conf": 0,
            "pdf_count_jrnl": 0,
            "processed_pdf_count": 0,
            "unprocessed_pdf_count": 0,
            "bib_total_count": 0,
            "bib_conf_count": 0,
            "bib_jrnl_count": 0,
            "bib_file_mod_times": {}
        }

    previous_mod_times = reference_data.get("bib_file_mod_times", {})

    # Count PDFs in the main directory
    total_pdfs, total_processed, total_unprocessed = count_pdfs_and_jsons(main_directory)

    # Count PDFs in `conf` and `jrnl` subfolders
    pdf_counts = count_pdfs_in_subfolders([conf_directory, jrnl_directory])
    pdf_count_conf = pdf_counts.get(conf_directory, 0)
    pdf_count_jrnl = pdf_counts.get(jrnl_directory, 0)

    # Count `.bib` entries
    conf_entries, conf_file_data = count_bib_entries_with_mod_times(conf_directory, previous_mod_times)
    jrnl_entries, jrnl_file_data = count_bib_entries_with_mod_times(jrnl_directory, previous_mod_times)
    total_bib_entries = conf_entries + jrnl_entries

    # Combine `.bib` file data for caching
    current_file_data = {**conf_file_data, **jrnl_file_data}

    # Clean cache to remove deleted files
    cleaned_file_data = clean_cache(previous_mod_times, current_file_data)

    # Detect changes in `.bib` files or PDFs
    if cleaned_file_data != previous_mod_times or total_pdfs != reference_data["pdf_count"]:
        reference_data.update({
            "pdf_count": total_pdfs,
            "pdf_count_conf": pdf_count_conf,
            "pdf_count_jrnl": pdf_count_jrnl,
            "processed_pdf_count": total_processed,
            "unprocessed_pdf_count": total_unprocessed,
            "bib_total_count": total_bib_entries,
            "bib_conf_count": conf_entries,
            "bib_jrnl_count": jrnl_entries,
            "bib_file_mod_times": current_file_data  # Ensure cache is updated
        })

        # Save updated data to the reference file
        with open(reference_file, 'w') as file:
            json.dump(reference_data, file, indent=4)

        print("Counts updated:")
    else:
        print("No updates detected. Using cached counts:")

    # Print the final results
    print(f"Total number of PDFs: {reference_data['pdf_count']}")
    print(f"  Number of PDFs in 'conf': {reference_data['pdf_count_conf']}")
    print(f"  Number of PDFs in 'jrnl': {reference_data['pdf_count_jrnl']}")
    print(f"  Processed PDFs: {reference_data['processed_pdf_count']}")
    print(f"  Unprocessed PDFs: {reference_data['unprocessed_pdf_count']}")
    print(f"Total number of .bib entries: {reference_data['bib_total_count']}")
    print(f"  Number of entries in 'conf': {reference_data['bib_conf_count']}")
    print(f"  Number of entries in 'jrnl': {reference_data['bib_jrnl_count']}")

def main():
    # Define main dataset directory and reference file path
    main_directory = r'F:\Digital Engineering\5th Sem\IR Anthology\Preprocessing\_processed data'
    reference_file = 'dataset_count_reference.json'

    # Check and update counts if needed
    check_and_update_counts(main_directory, reference_file)

if __name__ == "__main__":
    main()
