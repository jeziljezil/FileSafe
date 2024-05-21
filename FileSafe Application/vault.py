import os
import shutil
from tkinter import messagebox 

class SecretVault:
    def __init__(self):
        self.hidden_dir = os.path.expanduser('~/.vault')

    def hide_file(self, file_path):
        if os.path.exists(file_path):
            try:
                shutil.copy(file_path, self.hidden_dir)
                messagebox.showinfo('Successful', 'File is encrypted and hidden')                
                return
            except Exception as e:
                print("Error occurred while hiding the file:", e)
        else:
            print("File does not exist.")

    def list_hidden_files(self):
        hidden_files = os.listdir(self.hidden_dir)
        if hidden_files:
            print("List of hidden files:")
            for idx, file in enumerate(hidden_files):
                print(f"{idx+1}. {file}")
        else:
            print("No files are hidden in the vault.")

    def unhide_file(self, index, path):
        hidden_files = os.listdir(self.hidden_dir)
        if 1 <= index <= len(hidden_files):
            file_to_unhide = hidden_files[index - 1]
            file_path = os.path.join(self.hidden_dir, file_to_unhide)                                    
            try:
                # shutil.move(file_path, os.getcwd())
                shutil.move(file_path, path)
                messagebox.showinfo('Successful', f"File '{file_to_unhide}' successfully restored")                
            except Exception as e:
                print("Error occurred while unhiding the file:", e)
        else:
            print("Invalid index.")

vault = SecretVault()

def vault_list():
  vault.list_hidden_files()

def vault_out():
  vault.list_hidden_files()
  index = int(input("Enter the index of the file to unhide: "))
  vault.unhide_file(index)
        
