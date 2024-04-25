import os

def create_folder(path, name):
# Define the desired path
    desired_path = path

    # Define the folder name (optional)
    folder_name = name  # Change this if needed, otherwise omitted

    # Construct the full path (if folder name provided)
    if folder_name:
        new_folder_path = os.path.join(desired_path, folder_name)
    else:
        new_folder_path = desired_path

    # Create the folder using os.makedirs() for nested directory creation
    try:
        os.makedirs(new_folder_path)
        if folder_name:
            print(f"Folder '{folder_name}' created successfully in '{desired_path}'!")
        else:
            print(f"Folder created successfully at '{desired_path}'!")
    except FileExistsError:
        print(f"Folder '{new_folder_path}' already exists.")



def get_folder_names(directory_path):
  """
  Gets a list of folder names within a directory.

  Args:
      directory_path (str): The path to the directory containing folders.

  Returns:
      list: A list containing the names of all folders in the directory.
  """

  # Use os.listdir() to get all entries (files and folders)
  entries = os.listdir(directory_path)

  # Filter entries to keep only folders using os.path.isdir()
  folders = [entry for entry in entries if os.path.isdir(os.path.join(directory_path, entry))]

  return folders