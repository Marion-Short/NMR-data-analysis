#!/usr/bin/env python
# coding: utf-8
# Take data from TopSpin text document and store integrals in dataframe

def TopSpin_to_dataframe(code):
    directory = r'C:\Users\mims3\OneDrive - University of Cambridge\Experiments\Bacteria'

    from pathlib import Path
    path = Path(directory)

    # List all subdirectories
    folders = [item.name for item in path.iterdir() if item.is_dir()]

    # find the folder in the directory which matches experiment code
    import re
    for folder in folders:
        exp = re.match(code, folder)
        if exp:
            experiment = exp.string

    # create a list of all the files in this folder
    exp_folder = f'{directory}'+'\\'+f'{experiment}'
    doc_path = Path(exp_folder)
    documents = [item.name for item in doc_path.iterdir() if item.is_file()]

    # Remove the files which do not contain NMR data e.g. excel and word documents
    # Regular expression pattern to match strings ending with a period followed by alphabetical characters
    pattern = re.compile(r'\.[a-zA-Z]+$')

    # Filter the list using a list comprehension
    filtered_documents = [element for element in documents if not pattern.search(element)]
    
    import pandas as pd

    # create a function that when given the file name takes the file and saves the data to a dataframe

    def doc_to_df(file_name):

        # Open document and save all the lines in a list
        doc = f'{exp_folder}'+'\\'+file_name
        with open(doc, 'r') as text:
            lines = text.read()
        line_list = lines.splitlines()

        # drop the elements from the list that start with '#' and '' (i.e. empty)
        integrals = [l for l in line_list if not l.startswith('#') and l != '']

        # create a list of lists from the integrals
        list_of_lists = [s.split(';') for s in integrals]

        df = pd.DataFrame(list_of_lists)
        df = df.iloc[:, 1:-2]

        return df
    
    # Dictionary to store the data frames
    data_frames = {}

    # Iterate over the documents and create data frames
    for i, document in enumerate(filtered_documents):
        df = doc_to_df(document)  # Extract data from the document
        label = f'df{i}'                             # Create a label for the data frame
        data_frames[label] = df                      # Store the data frame in the dictionary
        
    return data_frames