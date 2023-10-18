import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 1234
MESSAGE_LENGTH = 2048
DECODE = 'utf-8'

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = '#fff'
FONT = ('Helvetica', 17)
SMALL_FONT = ('Helvetica', 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = tk.Tk()

root.geometry("800x600")
root.title("Message Client")
root.resizable(False, True)

root.grid_rowconfigure(0, minsize=40)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, minsize=50)



def add_message(message:str):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)



def listen_for_messages(client:socket.socket):
    while 1:
        message = client.recv(MESSAGE_LENGTH).decode(DECODE)
        if message != '':
            message_detail = message.split('~')
            username = message_detail[0]
            content = message_detail[1]
            # print(f"[{username}]: {content}")
            add_message(f"[{username}]: {content}")
        else:
            messagebox.showerror("Invalid message","The message from server is empty!")
            exit(0)


def comminucate_with_server(client:socket.socket):
    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username","Username cannot be empty!")
        exit(0)
    
    threading.Thread(target=listen_for_messages, args=(client,)).start()

def connect():
    try:
        client.connect((HOST, PORT))
        notification = f"Successfully connected to server {HOST}:{PORT}"
        print(notification)
        add_message(notification)

    except Exception as e:
        print(e)
        messagebox.showerror("Unable to connect server", f"Unable to connect server {HOST} {PORT}")
        exit(0)

    comminucate_with_server(client)

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = input_textbox.get()
    if message != '':
        client.sendall(message.encode())
        input_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Invalid message","Message cannot be empty!")
        exit(0)


def ux_config(root:tk.Tk):
    root.geometry("800x600")
    root.title("Message Client")
    root.resizable(False, True)

    root.grid_rowconfigure(0, minsize=40)
    root.grid_rowconfigure(1, weight=4)
    root.grid_rowconfigure(2, minsize=50)


    top_frame = tk.Frame(root, width=800, bg=DARK_GREY)
    top_frame.grid(row=0, column=0, sticky=tk.NSEW)
    
    username_label = tk.Label(top_frame, text="Enter username: ", font=FONT, bg=DARK_GREY, fg=WHITE)
    username_label.pack(side=tk.LEFT, padx=10)

    username_textbox = tk.Entry(top_frame, font=FONT, background=MEDIUM_GREY, fg=WHITE, width=25)
    username_textbox.pack(side=tk.LEFT)

    username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
    username_button.pack(side=tk.LEFT, padx=10)

    middle_frame = tk.Frame(root, width=800, height=400, bg=MEDIUM_GREY)
    middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=88)
    message_box.pack(side=tk.TOP, padx=5)
    message_box.config(state=tk.DISABLED)

    bottom_frame = tk.Frame(root, width=800, bg=DARK_GREY)
    bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

    input_textbox = tk.Entry(bottom_frame, font=FONT, background=MEDIUM_GREY, fg=WHITE, width=55)
    input_textbox.pack(side=tk.LEFT, padx=10)

    input_button = tk.Button(bottom_frame, text="Send", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
    input_button.pack(side=tk.LEFT)


top_frame = tk.Frame(root, width=800, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)
    
username_label = tk.Label(top_frame, text="Enter username: ", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, background=MEDIUM_GREY, fg=WHITE, width=25)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=10)

middle_frame = tk.Frame(root, width=800, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=88)
message_box.pack(side=tk.TOP, padx=5)
message_box.config(state=tk.DISABLED)

bottom_frame = tk.Frame(root, width=800, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

input_textbox = tk.Entry(bottom_frame, font=FONT, background=MEDIUM_GREY, fg=WHITE, width=55)
input_textbox.pack(side=tk.LEFT, padx=10)

input_button = tk.Button(bottom_frame, text="Send", font=SMALL_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
input_button.pack(side=tk.LEFT)


def main():
    root.mainloop()
    client.close()
    exit(0)

if __name__ == '__main__':
    main()