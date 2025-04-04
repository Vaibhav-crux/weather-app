import os

def parse_files_and_folders_to_txt(output_file='directory_structure.txt'):
    # Get the current working directory
    directory = os.getcwd()

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        return

    # Open the file to write output (creates the file if it doesn't exist)
    with open(output_file, 'w') as file:
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            # Exclude .venv and __pycache__ from the directories list
            if '.venv' in dirs:
                dirs.remove('.venv')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            
            # Calculate the depth and indent based on the folder structure
            depth = root[len(directory):].count(os.sep)
            indent = '  ' * depth  # Indentation based on depth

            # Write current directory
            file.write(f"{indent}- {os.path.basename(root)}/\n")

            # Write files in the current directory
            for file_name in files:
                file.write(f"{indent}  - {file_name}\n")

    print(f"Directory structure saved to {output_file}")

# Call the function to parse the current directory and save to 'directory_structure.txt'
parse_files_and_folders_to_txt()
