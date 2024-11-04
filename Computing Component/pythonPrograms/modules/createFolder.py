import os

def create_folder_if_not_exists(folder_name):
    """
    Create a folder with the specified name if it does not already exist.

    Parameters:
    - folder_name: The name of the folder to create.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")