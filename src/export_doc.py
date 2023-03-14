import csv

def export_documents(csv_file, doc_dir):
    """
    Export documents from a CSV file to a directory as text files.

    Args:
        csv_file (str): The path to the CSV file containing the documents.
        doc_dir (str): The path to the directory where the text files will be exported.

    Returns:
        None
    """

    # Set the column name for the text column
    text_column = 'Text'

    # Open the CSV file and read the rows
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get the text value from the specified column
            text = row[text_column]
            
            # Set the file name based on the row index or another identifier
            file_name = f"{doc_dir}/output_{reader.line_num}.txt"
            
            # Write the text to a new text file
            with open(file_name, 'w') as output_file:
                output_file.write(text)
