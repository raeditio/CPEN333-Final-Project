# Group#: G13
# Student Names: Ryan Jung and Daniel Juca

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    def __init__(self, window):
        self.window = window
        self.window.title("Chat Server")
        
        # GUI setup
        self.messages_frame = Frame(self.window)
        self.scrollbar = Scrollbar(self.messages_frame) # To navigate through past messages
        # Basic layout
        self.msg_list = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.messages_frame.pack()

        self.start_button = Button(self.window, text="Start Server", command=self.start_server)
        self.start_button.pack()

        self.stop_button = Button(self.window, text="Stop Server", command=self.stop_server, state=DISABLED)
        self.stop_button.pack()

        self.server_socket = None
        self.clients = []  # List to keep track of connected clients
        self.server_running = False

    def start_server(self):
        """
        This method starts the server.
        It creates a server socket and listens for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 12345  # Default port

        try:
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            self.msg_list.insert(END, f"Server started on {host}:{port}")
            self.server_running = True
            self.start_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)

            # Start the thread to accept connections
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            self.msg_list.insert(END, f"Error starting server: {e}")
    
    def accept_connections(self):
        """
        Accepts incoming connections and assigns client IDs.
        """
        while self.server_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_id = f"client{len(self.clients) + 1}"  # Assign unique ID
                self.clients.append(client_socket)
                self.msg_list.insert(END, f"{client_id} connected from {client_address}.")
                # Notify the client of its ID
                client_socket.sendall(client_id.encode("utf-8"))

                # Start a thread to handle this client
                threading.Thread(target=self.handle_client, args=(client_socket, client_id), daemon=True).start()
            except OSError:
                break

    
    def handle_client(self, client_socket):
        """
        This method handles a client connection.
        It receives messages from the client and sends them to all other clients.
        """
        client_address = client_socket.getpeername()  # Get client address
        client_id = f"client{self.clients.index(client_socket) + 1}"  # Assign a unique ID
        while self.server_running:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message:
                    formatted_message = f"{client_id}: {message}"
                    self.msg_list.insert(END, formatted_message)  # Display in the server GUI
                    self.broadcast(formatted_message, client_socket)
            except ConnectionResetError:
                break
        client_socket.close()
        
    def broadcast(self, message, client_socket):
        """
        This method sends the message to all clients except the sender.
        """
        for client in self.clients:
            if client != client_socket:
                try:
                    client.sendall(message.encode("utf-8"))
                except:
                    self.clients.remove(client)

                    
    def stop_server(self):
        """
        This method stops the server.
        Stop the chat server and disconnect all clients.
        """
        self.server_running = False
        for client in self.clients:
            client.close()
        self.clients.clear()

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

        self.msg_list.insert(END, "Server stopped.")
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
    
    def on_closing(self):
        """
        This method is called when the window is closed.
        """
        self.server_running = False
        self.window.destroy()

def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    server = ChatServer(window)
    window.protocol("WM_DELETE_WINDOW", server.on_closing)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()