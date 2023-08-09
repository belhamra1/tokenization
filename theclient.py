import tkinter as tk
from tkinter import messagebox
import socket

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080

def send_data():
    pan_number = entry_pan.get()
    '''password = entry_password.get()'''

    if not pan_number :
        messagebox.showerror("Error", "Please enter PAN card number .")
        return
    
    if not(16 <=len(pan_number) <=19):
        messagebox.showerror("Error","PAN card number must be between 16 an 19 in it's length")
        return
    
    '''if not(len(password) ==4):
        messagebox.showerror("Error","the PASSWORD length is exactly 4 !!")
        return'''
    
    
    data_to_send = f"{pan_number}"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

        client_socket.sendall(data_to_send.encode())

        response = client_socket.recv(1024).decode()
        print("Received response from server:", response)

        client_socket.close()
        messagebox.showinfo("Response", response)
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "An error occurred while connecting to the server.")

# Create the GUI window
root = tk.Tk()
root.title("Token Generator")

# Create and place widgets in the GUI window
label_pan = tk.Label(root, text="PAN card number:")
label_pan.pack()

entry_pan = tk.Entry(root)
entry_pan.pack()

'''label_password = tk.Label(root, text="Password:")
label_password.pack()

entry_password = tk.Entry(root, show="*")
entry_password.pack() '''

button_generate_token = tk.Button(root, text="Generate Token", command=send_data)
button_generate_token.pack()

# Start the GUI event loop
root.mainloop()
