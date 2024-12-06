# Group#: G13
# Student Names: Ryan Jung and Daniel Juca

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """

    def __init__(self, window):
        self.window = window
        self.window.title("Chat Client")

        # Set up the GUI
        self.messages_frame = Frame(self.window)
        self.scrollbar = Scrollbar(self.messages_frame)  # For scrolling messages
        self.msg_list = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.messages_frame.pack()

        self.message_var = StringVar()  # For the input message
        self.message_var.set("Type your message here.")
        self.entry_field = Entry(self.window, textvariable=self.message_var, width=40)
        self.entry_field.bind("<Return>", self.send_message)  # Bind the Enter key to send messages
        self.entry_field.pack()

        self.send_button = Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        # Networking setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Prompt user for server details
        self.server_host = input("Enter server IP: ")
        self.server_port = int(input("Enter server port: "))

        try:
            self.client_socket.connect((self.server_host, self.server_port))
            self.msg_list.insert(END, "Connected to the server.")
        except Exception as e:
            self.msg_list.insert(END, f"Unable to connect to server: {e}")
            return

        # Start a thread to receive messages
        self.stop_thread = False
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        # Proper cleanup
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def send_message(self, event=None):
        """
        This method sends the message to the server.
        """
        message = self.message_var.get()
        self.message_var.set("") # Clear the input field
        try:
            self.client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            self.msg_list.insert(END, f"Error sending message: {e}")
    
    def receive_messages(self):
        """
        This method receives messages from the server.
        """
        while not self.stop_thread:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    self.msg_list.insert(END, message)
            except OSError:
                break

    def on_closing(self):
        """
        This method is called when the window is closed.
        """
        self.stop_thread = True
        self.client_socket.close()
        self.window.destroy()
    
def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()