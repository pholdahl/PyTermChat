# Importerer nødvendige moduler
import socket
import threading
import time


HOST = socket.gethostname()
PORT = 9031
FORMAT = "utf-8"


user = "login"
userID = None

def messagePrinter(message):
        userPrompt = "\r""<"+user+"> "
        if message == "§" or message == "":
            print(userPrompt, end='')
        else:
            username = message.split("~",1)[0]
            content = message.split("~",1)[1]
            print()
            print(f"[{username}] {content}")
            print(userPrompt, end='')


def listenForMessagesFromServer(client):
    global userID
    global user
    while True:
        message = client.recv(4096).decode(FORMAT)

        # Hvis melding er "disconnect" bryter vi while løkka
        if userID in message and "disconnect" in message:
            messagePrinter("SERVER~Disconnected from server")
            break
        elif userID in message and "newusername" in message:
            user = message.split(" ")[2]      # Index 2 since userID is index 0 and newusername is index 1
        else:
            messagePrinter(message)

    # Endrer user variabelen til disconnect slik at  sendMessageToServer funksjonen bryter ut av while løkka
    userID = "disconnect"
    return


def sendMessage(client, message):
    userPrompt = "\r""<"+user+"> "
    if message == "" or message.isspace():
        print(userPrompt, end='')
    else:
        client.sendall(str(message).encode())


def sendMessageToServer(client):
    while userID != "disconnect":
        sendMessage(client, input().lstrip())

        # Bruker en kort sleep her for at user variabelen skal ha tid til å endre til "disconnect" slik at vi bryter ut av while løkka før vi går inn i input
        time.sleep(0.001)
    return


def login(client):
    while True:

        # user er satt til "login" og vil i løpet av login funksjon endres til ønsket "username"
        global user
        global userID
        message = client.recv(4096).decode(FORMAT)
        messagePrinter(message)
        if "enter" in message:
            while True:
                message = input().lstrip()
                username = message                              # Her legges brukernavnet som er skrevet i input
                sendMessage(client, message)                    # Sendes til server
                message = client.recv(4096).decode(FORMAT)      # Returnerer en melding fra server
                if "Please" in message:                         # Hvis "Please" i melding vil si at en har brukt feil tegn i brukernavnet
                    messagePrinter(message)
                    continue
                elif "already" in message:                      # Hvis "already" i melding vil si at brukernavnet allerede eksisterer
                    messagePrinter(message)
                    continue
                elif username in message:                       # Hvis username finnes i meldingen
                    userID = message.split(" ")[0]              # Inneholder meldingen også socket port nummeret som identifikator
                    user = username                             # username er godkjent
                return
        else:
            message = input().lstrip()
            sendMessage(client, message)


# Starter Thread for å lytte etter meldinger fra server og sender clientObjektet til server. 
def communicateToServer(client):
    try:
        client.sendall(user.encode())
        login(client)
        sendMessage(client, user)
        threading.Thread(target=listenForMessagesFromServer, args=(client,)).start()
        sendMessageToServer(client)
    except Exception as e:
        print(e)
    print("Exiting")
    client.close()
    quit()

# main function
def main():

    # Lager et socket objekt
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Koble seg til serveren
    try:
        client.connect((HOST, PORT))
        # print(client.getpeername())
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    # Kaller kommunikasjonsfunksjon som igangsetter
    communicateToServer(client)

# Standard oppstart
if __name__ == "__main__":
    main()