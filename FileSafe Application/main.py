import os
import hashlib
from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog
from db import Database
from cryptography.fernet import Fernet
from vault import SecretVault


db = Database('file.db')
vault = SecretVault()

# Function to save hashed password
def save_password():
    password = password_text.get()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open("password.txt", "w") as file:
        file.write(hashed_password)
    create_password_window.destroy()

# Function to check password
def check_password():     
    user_input = password_entry.get()
    hashed_input = hashlib.sha256(user_input.encode()).hexdigest()
    with open("password.txt", "r") as file:
        stored_password = file.read()
    if hashed_input == stored_password:
        messagebox.showinfo("Success", "Password Correct! Access Granted.")            
        start_app()        
        password_window.destroy()            
    else:
        messagebox.showerror("Error", "Incorrect Password!")

# Function to create password window
def create_password_window():
    global password_text, password_entry, create_password_window
    create_password_window = Tk()
    create_password_window.title("Create Password")
    create_password_window.geometry("400x180")


    password_text = StringVar()
    Label(create_password_window, text="Create Password:").pack(pady=10)
    password_entry = Entry(create_password_window, width=40, textvariable=password_text, show="*")
    password_entry.pack(pady=10)
    Button(create_password_window, text="Save Password", width=12, command=save_password).pack(pady=10)

# Function to prompt for password
def password_prompt():
    
    global password_entry, password_window
    password_window = Tk()
    password_window.title("Password Required")
    password_window.geometry("400x180")

    Label(password_window, text="Enter Password:").pack(pady=10)
    password_entry = Entry(password_window, width=40, show="*")
    password_entry.pack(pady=10)
    Button(password_window, text="Enter", width=12, command=check_password).pack(pady=10)

# Prints all encrypted files in the listbox
def populate_list():
  file_list.delete(0, END)
  for row in db.fetch():
    file_list.insert(END, row)

# Lets user browse through their directories
def select_file():
  file_path = filedialog.askopenfilename()
  if file_path:
    file_entry.delete(0, END)
    file_entry.insert(END, file_path)

# Encrypts the file, saves a copy in the vault
def encrypt():
  
  for row in db.fetch():
    if file_entry.get() == row[1]:
      messagebox.showerror('Error', 'This file is already encrypted')
      return
  
  if file_entry.get() == '':
    messagebox.showerror('Required Fields', 'Please select a file')
    return
  
  # key 
  key = 'm6eWhr2ruRQBJjvTnNKRdzl3It949hHvRpZMVKFDXA8='

  # using the generated key
  fernet = Fernet(key)
  
  file_addr = file_entry.get()
  
  # opening the original file to encrypt
  with open(file_addr, 'rb') as file:
    original = file.read()
    
  # encrypting the file
  encrypted = fernet.encrypt(original)

  # opening the file in write mode and writing the encrypted data
  with open(file_addr, 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

  # saves file copy in vault      
  vault.hide_file(file_addr)

  # file path saved to database
  db.insert(file_addr)
  file_list.insert(END, (file_addr))
  clear_text()
  populate_list()

  # Deletes the file 
  os.remove(file_addr)

# Decrypts the file, releases a copy at original location
def decrypt():
  key = 'm6eWhr2ruRQBJjvTnNKRdzl3It949hHvRpZMVKFDXA8='

  destin = '/'.join(selected_item[1].split('/')[:-1])  
  vault.unhide_file(selected_item[0], destin)

  # using the key
  fernet = Fernet(key)

  file_addr = selected_item[1]

  # opening the encrypted file
  with open(file_addr, 'rb') as enc_file:
    encrypted = enc_file.read()

  # decrypting the file
  decrypted = fernet.decrypt(encrypted)

  # opening the file in write mode and writing the decrypted data
  with open(file_addr, 'wb') as dec_file:
    dec_file.write(decrypted)

  db.remove(selected_item[0])
  clear_text()
  populate_list()


# Deletes selection
def delete():
  db.remove(selected_item[0])
  clear_text()
  populate_list()

# Clears the 'file_entry' textfield
def clear_text():
  file_entry.delete(0, END)  

# Retrieves the data of selection
def select_item(event):
  try:
    global selected_item
    index = file_list.curselection()[0]
    if (not file_list):
      index = 0
    selected_item = file_list.get(index)
    
    file_entry.delete(0, END)
    file_entry.insert(END, selected_item[1])      
  except IndexError:
    pass

def start_app():
  # Create window object
  app = Tk()    

  # App brief
  define_app = 'Encrypt or Decrypt your files'
  file_label = Label(app, text=define_app, font=('bold', 20), pady=20)
  file_label.pack(fill=X)

  # App body
  file_frame = Frame(app)
  file_frame.pack(pady=(5, 0), padx=10, fill=X)

  # File selection
  file_label = Label(file_frame, text='Select File', font=('bold', 14))
  file_label.pack(side=LEFT)

  global file_path, file_entry
  file_path = StringVar()
  file_entry = Entry(file_frame, width=50, textvariable=file_path)
  file_entry.pack(side=LEFT, padx=(10, 0))

  file_btn = Button(file_frame, text="Browse..", width=12, command=select_file)
  file_btn.pack(side=LEFT, padx=(10, 0))

  # Encryption and Decryption buttons
  button_frame = Frame(app)
  button_frame.pack(pady=20)

  encr_btn = Button(button_frame, text='Encrypt File', width=12, command=encrypt)
  encr_btn.pack(side=LEFT, padx=(10, 5))

  decr_btn = Button(button_frame, text='Decrypt File', width=12, command=decrypt)
  decr_btn.pack(side=LEFT, padx=(5, 10))

  # Delete file from db
  del_btn = Button(button_frame, text='Delete', width=12, command=delete)
  del_btn.pack(side=LEFT, padx=(60, 0))

  # Listbox label
  list_label = Label(app, text='List of encrypted and hidden files:', font=('bold', 12))
  list_label.pack(fill=BOTH)
  # Files List
  global file_list
  file_list = Listbox(app, height=8, width=50, border=0)
  file_list.pack(side=LEFT, fill=BOTH, expand=True, pady=(0, 20), padx=20)
  # create scrollbar
  scrollbar = Scrollbar(app)
  scrollbar.pack(side=RIGHT, fill=Y)
  # Set scroll to listbox
  file_list.configure(yscrollcommand=scrollbar.set)
  scrollbar.configure(command=file_list.yview)
  # Bind select
  file_list.bind('<<ListboxSelect>>', select_item)

  app.title('FileSafe')
  app.geometry('700x400')

  #Populate data
  populate_list()

# Check if password file exists
try:
    with open("password.txt", "r") as file:
        stored_password = file.read()
    if stored_password:
        password_prompt()        
except FileNotFoundError:
    create_password_window()


mainloop()

