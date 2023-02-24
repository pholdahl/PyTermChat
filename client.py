import socket                   # Importing the socket module
import threading                # Importing the threading module for multithreading
import time                     # Importing the time module for thread timing

HOST = socket.gethostname()     # Set the host to the current machine name
PORT = 9031                     # Set the port number to 9031
FORMAT = "utf-8"                # Set the character encoding format to UTF-8

user = "login"                  # Set the default username
userID = None                   # Set the userID variable to None by default

# Function to print the message received from server
def messagePrinter(message):
    userPrompt = "\r""<"+user+"> "                  # Set the user prompt
    if message == "§" or message == "":             # If the message is empty or has a special character for triggering the user prompt
        print(userPrompt, end='')                   # Print the user prompt
    else:
        username = message.split("~",1)[0]          # Extract the username from the message
        content = message.split("~",1)[1]           # Extract the message content
        print()                                     # Print a new line
        print(f"[{username}] {content}")            # Print the username and message content
        print(userPrompt, end='')                   # Print the user prompt

# Function to listen for messages from server
def listenForMessagesFromServer(client):
    global userID                                               # Use the global variabel to be able to change its value
    global user                                                 # Use the global variable to be able to change username locally
    while True:                                                 # While loop to continuously receive messages
        message = client.recv(4096).decode(FORMAT)              # Receive message from server
        if userID in message and "disconnect" in message:       # If user ID and "disconnect" is in the message
            messagePrinter("SERVER~Disconnected from server")   # Print disconnection message
            break                                               # Break out of the while loop
        elif userID in message and "newusername" in message:    # If user ID and "newusername" is in the message
            user = message.split(" ")[2]                        # Extract new username from message
        else:                                                   # Else
            messagePrinter(message)                             # Send the message to the messagePrinter function
    userID = "disconnect"                                       # If while loop breaks, set the user ID to "disconnect" so the sendMessageToServer function returns
    return

# Function to send message to server
def sendMessage(client, message):
    userPrompt = "\r""<"+user+"> "                              # Set the user prompt
    if message == "" or message.isspace():                      # If the message is empty or only contains whitespace
        print(userPrompt, end='')                               # Print only the user prompt
    else:
        client.sendall(str(message).encode())                   # Else send the message to the server
       
# Function to send message to the server continuously
def sendMessageToServer(client):
    while userID != "disconnect":                               # While the user is connected to the server
        sendMessage(client, input().lstrip())                   # Send the user's input to the server, stripping whitespace from the left
        time.sleep(0.001)                                       # Sleep for a short period to avoid message oveflows which may confuse the messagPrinter function
    return

# Function to handle user login
def login(client):
    while True:                                                 # While loop to continuously receive messages from the server
        global user                                             # Use the global variabel to be able to change its value
        global userID                                           # Use the global variable to be able to change username locally
        message = client.recv(4096).decode(FORMAT)              # Receive message from server
        messagePrinter(message)                                 # Print the message received from server
        if "enter" in message:                                  # If the message prompts the user to enter a username
            while True:                                         # While loop to continuously prompt user for username to check if username is valid
                message = input().lstrip()                      # Remove leading whitespace from user input
                username = message                              # Storing message in variable username                        
                sendMessage(client, message)                    # Sending the message to the servare
                message = client.recv(4096).decode(FORMAT)      # Recieving returnmessage from the server
                if "Please" in message:                         # If "Please" in message username contains not allowed characters or spaces
                    messagePrinter(message)                     # Print the message
                    continue                                    # Go back to the start of the "enter" username while loop
                elif "already" in message:                      # If "already" in the message, the username already exists
                    messagePrinter(message)                     # Print the message               
                    continue                                    # Go back to the start of the "enter" username while loop
                elif username in message:                       # If the message from the server is equal to the username variable           
                    userID = message.split(" ")[0]              # The message will also contain the userID which is the port nr. assigned from the server
                    user = username                             # Change the global user variable to the username
                return                          
        else:                                                   # Else (This part will never happen, but put it here in case of changes)
            message = input().lstrip()                          # Remove leading whitespace from user input
            sendMessage(client, message)                        # SendMessage

# Function to communicate with the server
def communicateToServer(client):
    try:                                                        # Try to handle exceptions
        client.sendall(user.encode())                           # Starts the communcation by sending the global user variable "login"
        login(client)                                           # Starts the login function, with the clientobject as parameter
        sendMessage(client, user)                               # Sends the client object with the global user variable containing the username
        # Starts the listeForMessagesFromServer function as thread
        threading.Thread(target=listenForMessagesFromServer, args=(client,)).start()
        sendMessageToServer(client)                             # Starts the sendMessageToServer function with client as paremeter which has a while loop
    except Exception as e:                                      # Catching exceptions
        print(e)                                                # Printing the exception
    print("Exiting")                                            # Printing "Exiting" if disconnected from server or because of Exeption
    client.close()                                              # Closing client
    quit()                                                      # Quiting the script

# Main function to define client object and start the chat program
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Defining client object
    try:                                                        # Try to handle exceptions
        client.connect((HOST, PORT))                            # Connecting to server
    except Exception as e:                                      # Catching exceptions
        print(e)                                                # Printing the exception
        print(f"Unable to connect to server {HOST} {PORT}")     # Printing a more readable line
    communicateToServer(client)                                 # Starting communicateToServer function with client object as paremeter.

# Standard python start command
if __name__ == "__main__":
    main()