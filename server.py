# Importerer nødvendige biblioteker
import socket
import threading
import time
import sys


HOST = socket.gethostname()
PORT = 9031 # En kan bruke en port mellom 0 og 65535
FORMAT = "utf-8"


MAXCLIENTS = 10
BADNAME = "SERVER~Please enter a username thats not empty, containing spaces or [/,§,~]"
USERNAMEEXISTS = "SERVER~Username already exists"
ERRORUSERNAME = "SERVER~Username doesn't exist in clientlist"
ERRORGROUPNAME = "SERVER~Group doesn't exist"
ERRORGENERAL = "SERVER~Something went wrong"
NOCOMMAND = "SERVER~Command does not exist"
MAINAREA = "The Ether"

GROUP = {
    "chatgroup1":[],"chatgroup2":[],"chatgroup3":[],"chatgroup4":[], "chatgroup5": [],
    "chatgroup6": [], "chatgroup7": [], "chatgroup8": [], "chatgroup9": []}

WELCOME = "SERVER~Welcome to the server!"
LOGIN = "SERVER~New or returning user? Respond with [n] or [r]"
INSTRUCTIONS = '''
 ---------------------------------------------------------------------
| Commands to use:                                                    |
|---------------------------------------------------------------------| 
| /shout -> sends messages to everyone including chatgroups           |
| /list -> returns a list of online users                             |
| /whisper [username] -> sends a message to a specific user           |
| /chat [1-9] -> enter at chatgroup numbers 1-9                       |
| /exit -> makes you leave a chatrgroup                               |
| /rps [username] -> start a game of rock paper sissors with a user   |
| /whereami -> returns your position, the main area or in chatgroups  |
| /bye -> disconnects you from the server                             |
| /instructions -> returns this instruction overview                  |
 ---------------------------------------------------------------------
'''
LOGIN = "SERVER~New or returning user? Respond with [n] or [r]"

GAMEINSTRUCTIONS = '''RPS~
 ---------------------------------------------------------------------
| Welcome to Rock, Paper Scissors!                                    |
|---------------------------------------------------------------------| 
|    ⠀⠀⠀⠀⠀⣠⡴⠖⠒⠲⠶⢤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠖⠒⢶⣄⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠀⢀⡾⠁⠀⣀⠔⠁⠀⠀⠈⠙⠷⣤⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠋⠀⠀⠀⢀⡿⠀⠀⠀⠀⠀⠀⠀                  |
|    ⣠⠞⠛⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⠈⢿⡀⢠⡶⠒⠳⠶⣄⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⣰⠏⠀⢀⣤⣤⣄⡀⠀⠀                  |
|    ⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠛⠛⠃⠸⡇⠈⣇⠸⡇⠀⠀⠀⠘⣇⠀⠀⣠⡾⠁⠀⠀⠀⢀⣾⣣⡴⠚⠉⠀⠀⠈⠹⡆⠀                  |
|    ⣹⡷⠤⠤⠤⠄⠀⠀⠀⠀⢠⣤⡤⠶⠖⠛⠀⣿⠀⣿⠀⢻⡄⠀⠀⠀⢻⣠⡾⠋⠀⠀⠀⠀⣠⡾⠋⠁⠀⠀⠀⠀⢀⣠⡾⠃⠀                  |
|    ⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡤⠖⠋⢀⣿⣠⠏⠀⠀⣿⠀⠀⠀⠘⠉⠀⠀⠀⠀⠀⡰⠋⠀⠀⠀⠀⠀⣠⠶⠋⠁⠀⠀⠀                  |
|    ⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠁⠀⠀⠠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠁⠀⠀⠀⢀⣴⡿⠥⠶⠖⠛⠛⢶⡄                  |
|    ⠀⠉⢿⡋⠉⠉⠁⠀⠀⠀⠀⠀⢀⣠⠾⠋⠀⠀⠀⠀⢀⣰⡇⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⢀⣠⠼⠃                  |
|    ⠀⠀⠈⠛⠶⠦⠤⠤⠤⠶⠶⠛⠋⠁⠀⠀⠀⠀⠀⠀⣿⠉⣇⠀⡴⠟⠁⣠⡾⠃⠀⠀⠀⠀⠀⠈⠀⠀⠀⣀⣤⠶⠛⠉⠀⠀⠀                  |
|    ⠀⠀⠀⠀⢀⣠⣤⣀⣠⣤⠶⠶⠒⠶⠶⣤⣀⠀⠀⠀⢻⡄⠹⣦⠀⠶⠛⢁⣠⡴⠀⠀⠀⠀⠀⠀⣠⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⢀⡴⠋⣠⠞⠋⠁⠀⠀⠀⠀⠙⣄⠀⠙⢷⡀⠀⠀⠻⣄⠈⢷⣄⠈⠉⠁⠀⠀⠀⢀⣠⡴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⢀⡾⠁⣴⠋⠰⣤⣄⡀⠀⠀⠀⠀⠈⠳⢤⣼⣇⣀⣀⠀⠉⠳⢤⣭⡿⠒⠶⠶⠒⠚⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⢸⠃⢰⠇⠰⢦⣄⡈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠛⠛⠓⠲⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠸⣧⣿⠀⠻⣤⡈⠛⠳⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠈⠹⣆⠀⠈⠛⠂⠀⠀⠀⠀⠀⠀⠈⠐⠒⠒⠶⣶⣶⠶⠤⠤⣤⣠⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠀⠀⠹⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠀⠀⠀⠈⠻⣦⣀⠀⠀⠀⠀⠐⠲⠤⣤⣀⡀⠀⠀⠀⠀⠀⠉⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠶⠤⠤⠤⠶⠞⠋⠉⠙⠳⢦⣄⡀⠀⠀⠀⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⠦⠾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  |
|---------------------------------------------------------------------|
| [r] -> Choose rock                                                  |
| [p] -> Choose paper                                                 |
| [s] -> Choose scissors                                              |
| - May the best combatant win!                                       |
 ---------------------------------------------------------------------
'''


# Existing usernames are stored in the clients list
clients = ["Pholdahl"]
# activeClients stores usernames and client port number in a dictionary where the port number is the key
activeClients = dict()
# chaGroups is a dictionary containing 9 different chatgroups with chatgroup[1-9] being the keys
chatGroups = GROUP
# a list containing users in groupchat for easy access to search through for broadcast function
inGroupChat = []
# inLobby is a list of g
inLobby = []
inGame = []


# listenForMessages listens for and redirects all incomming messages
def listenForMessages(client):
    
    while True:

        try:
            message = client.recv(4096).decode(FORMAT)
            message = message.lstrip()

            if message == "/bye":
                break
            

            # Lobby message?
            if any(client.getpeername()[1] in item for item in inLobby):
                print(message)
                print(client.getpeername()[1])
                lobbyroom(client, message)


            # Game message?
            elif any(client.getpeername()[1] in item for item in inGame):
                game(client, message)


            # Groupchat message?
            elif client.getpeername()[1] in inGroupChat:
                chatrooms(client, message)
            

            # Command message?
            elif message.startswith("/"):
                commandMessage(client, message)


            # Normal message?
            else:
                message = activeClients[client.getpeername()[1]][1] + "~" + message
                broadcast(client, message)
                
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception was:", e)
            print(exception_traceback.tb_lineno)
            break
    disconnect(client)
    


# Chatroom/Chatgroup function
def chatrooms(client, message):

    # Command message?
    if message.startswith("/"):
        commandMessage(client, message)
    
    # Groupchat message
    else:
        groupMemberNr = client.getpeername()[1]
        groupNr = None
        for key, value in chatGroups.items():
            if groupMemberNr in value:
                groupNr = key
        sendList = chatGroups[groupNr]
        for m in sendList:
            for clients in activeClients.values():
                if m == clients[0].getpeername()[1] and clients[0].getpeername()[1] == client.getpeername()[1]:
                    returnEmpty(client)
                elif m == clients[0].getpeername()[1]:
                    sendMessageToClient(clients[0], activeClients[client.getpeername()[1]][1] + '~' + message)  # Henter ut username til avsender fra activeClients


def countDown(client, start):
    if start == True:
        startTime = time.time()
        while start:
            if time.time() - startTime > 10:
                removeUsersFromGameLobby(client)
                break
            elif start == False:
                return


def removeUsersFromGameLobby(client):
    print("in removeuserFromGameLobby")
    userFound = False
    index = 0
    for game in inLobby:
        if client.getpeername()[1] in game:
            userFound = True
            break
        index += 1
    print("after for loop1")
    if userFound:
        gamePair = inLobby.pop(index)
        for clients in activeClients.values():
            if clients[0].getpeername()[1] == gamePair[0]:
                sendMessageToClient(clients[0], f"SERVER~{activeClients[client.getpeername()[1]][1]} declined, or took too long to respond")
                returnEmpty(client)
                break
    else:
        return


def moveUsersToGame(client):
    index = 0
    for game in inLobby:
        if client.getpeername()[1] in game:
            break
        index += 1
    inGame.append(inLobby.pop(index))

def removeUsersFromGame(client):
    index = 0
    for game in inGame:
        if client.getpeername()[1] in game:
            break
        index += 1
    inGame.remove(index)


def lobbyroom(client, message):
    print("in lobbyroom")
    if message == "n":
        removeUsersFromGameLobby(client)
    elif message == "y":
        returnEmpty(client)
        moveUsersToGame(client)
        time.sleep(2)
        gameRoom = findGameRoom(client)
        sendMessageToClient(activeClients[gameRoom[0]][0], GAMEINSTRUCTIONS)
        sendMessageToClient(activeClients[gameRoom[1]][0], GAMEINSTRUCTIONS)
        time.sleep(2)
        gameRoom[2] += 1
        sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round{gameRoom[2]}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
        sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round{gameRoom[2]}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
    else:
        sendMessageToClient(client, "SERVER~You have to respond yes [y] or no [n]")


def findGameRoom(client):
    index = 0
    for u in inGame:
        if client.getpeername()[1] in u:
            break
        index += 1
    return inGame[index]

def findPlayer2(client, gameRoom):
    player2 = None
    for u in gameRoom:
        if u != client.getpeername()[1]:
            player2 = u
            break
    return player2


# appending a game as a list: index 2 = round, index 3, 4 = moves for a round, index 5, 6, 7  =  result from each rounds.
# a value of: -1 = not played, 0 = player1 wins, 1 = player2 winns, 2 = tie
def game(client, message):
    # Få inn en rundeteller, counter, som også kan brukes i sendMessageToClient()
    # Nullstille movsene i gameRoom, hold rede på poengene i en tabell
    print("Inne i game")
    gameRoom = findGameRoom(client)
    player1Key = gameRoom[0] # player1 is at index 0 of the gameroom, the user who invited to play RPS
    player2Key = gameRoom[1] # player2 is at index 1 of the gamroom
    print("player1", player1Key)
    print("player2", player2Key)
    endgame = False
    # Game loop 
    while gameRoom[3] == -1 or gameRoom[4] == -1:   # index 3 and index 4 = -1, means that the round is not finished (index 3 and index 4 will contain the moves of the players)
        endRound = False
        if message == "r" or message == "p" or message == "s":
            print(str(client.getpeername()[1]) + " is in 1 gameloop")
            moveToValue(client, message, gameRoom)
            print("Inne i while loop")
            while(gameRoom[3] != -1 and gameRoom [4] != -1): # index 3 and index 4 = -1, means that the round is not finished
                print("inne i if sjekk gameRoom")
                addPointsToRound(gameRoom)
                print("Points for round " + str(gameRoom[2]) + ": " +  str(gameRoom[gameRoom[2+4]]))
                endRound = True
                break
            continue
        elif message != "r" or message != "p" or message != "s":
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Wrong command, must choose between Rock[r], Paper[p] or Scissors[s]")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Wrong command, must choose between Rock[r], Paper[p] or Scissors[s]")
            break
    if endRound == True:
        print(gameRoom[int(gameRoom[2])+4])
        if gameRoom[int(gameRoom[2])+4] == 0:
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~You won {int(gameRoom[2])} round")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Player1 won {int(gameRoom[2])} round")
        elif gameRoom[int(gameRoom[2])+4] == 1:
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Player2 won {int(gameRoom[2])} round")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~You won {int(gameRoom[2])} round")
        elif gameRoom[int(gameRoom[2])+4] == 2:
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round {int(gameRoom[2])} was a draw")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round {int(gameRoom[2])} was a draw")
        time.sleep(5) 
        gameRoom[2] += 0.5              # Add 0.5 per user per round, when 2 players have used there move, round + 1.0 = next round
        gameRoom[3] = -1                # Setting move index 3 to -1, so we can repeat with the same game while loop
        gameRoom[4] = -1                # Setting move index 4 to -1, so we can repeat with the same game while loop

        # if round index = 4, we are passed round 3, and we need to calulate which player is the winner
        if gameRoom[2] == 4.0:
            player1Points = 0
            player2Points = 0
            for i in range(5,8):
                if gameRoom[i] == 0:
                    player1Points += 1
                elif gameRoom[i] == 1:
                    player2Points += 1
                elif gameRoom[i] == 2:
                    continue
            if player1Points > player2Points:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Congratulations, you won the game!")
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Buuhuu, you lost, get over it!")
                print("Player1 wins")
            elif player2Points > player1Points:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Congratulations, you won the game!")
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Buuhuu, you lost, get over it!")
                print("Player2 wins")
            else:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~The game was a draw")
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~The game was a draw")
                print("It is a draw")
            inGame.remove(gameRoom)
            time.sleep(1)
            whereami(activeClients[gameRoom[0]][0])
            whereami(activeClients[gameRoom[1]][0])
            return
        elif gameRoom[2].is_integer():
            print("Value of gameRoom[2) = " + str(gameRoom[2]) + "isInteger: " + str(gameRoom[2].is_integer()))
            sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
            sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
            # if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
            #     sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
            # elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
            #     sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")

    
def moveToValue(client, message, gameRoom):
    move = -1
    if message == "r":
        move = 0
    elif message == "p":
        move = 1
    elif message == "s":
        move = 2
    if client.getpeername()[1] == gameRoom[0]:
        gameRoom[3] = move
    elif client.getpeername()[1] == gameRoom[1]:
        gameRoom[4] = move
    return

def addPointsToRound(gameRoom):
    if (gameRoom[3] + 1) % 3 == gameRoom[4]:
        print("Player2 won because their move is one greater than player 1")
        gameRoom[int(gameRoom[2])+4] = 1
    elif (gameRoom[3] == gameRoom[4]):
        gameRoom[int(gameRoom[2])+4] = 2
        print("Its a draw")
    else:
        print("Player1 wins")
        gameRoom[int(gameRoom[2])+4] = 0
    return

    # print(inGame)
    # sendMessageToClient(player2, "player"+ "~" + message)
    # returnEmpty(client)

def rpsLogic(gameRoom):
    while(gameRoom[2] == -2 or gameRoom[3] == -2):
        while(gameRoom[2] != -2 and gameRoom [3] != -2):
            print("inne i if sjekk gameRoom")
            if (gameRoom[2] + 1) % 3 == gameRoom[3]:
                print("Player2 won because their move is one greater than player 1")
                return True
            elif (gameRoom[2] == gameRoom[3]):
                print("Its a draw")
                return True
            else:
                print("Player1 wins")
                return True
        continue
    # while(gameRoom[2] != -2 and gameRoom[3] != -2):

def getClientKeyFromUsername(username):
    for key, value in activeClients.items():
        if username == value[1]:
            return key
    
    
    
        

def commandMessage(client, message):
    # List command
    if message.startswith("/list"):
        listOfClients = "SERVER~List of users online:\n"
        clientKeyList = activeClients.keys()
        # for c in activeClients:
        #     listOfClients += "[" + c[0] + "]\n"
        for clientKey in clientKeyList:
            listOfClients += "[" + activeClients[clientKey][1] + "]\n"
        sendMessageToClient(client, listOfClients)
    
    # Whisper command
    elif message.startswith("/whisper"):
        message = message.replace("/whisper ","")
        try:
            userToWhisper = activeClients[getClientKeyFromUsername(message.split(" ",1)[0])][0] 
            finalMessage = activeClients[client.getpeername()[1]][1] + "~Whispered: " + message.split(" ",1)[1]
            sendMessageToClient(userToWhisper, finalMessage)
            returnEmpty(client)
        except:
            sendMessageToClient(client, ERRORUSERNAME)

    # Chatgroup command
    elif message.startswith("/chat"):
        message = message.replace("/chat ","")
        groupToGo = "chatgroup"+message.split(" ", 1)[0]
        if groupToGo in chatGroups.keys():
            clientNumber = client.getpeername()[1]
            try:
                exitGroup = exit(client)
                chatGroups[groupToGo] += [clientNumber]
                inGroupChat.append(clientNumber)
                if(exitGroup is not None):
                    sendMessageToClient(client, f"SERVER~You just exited {exitGroup} and entered {groupToGo}")
                else:
                    sendMessageToClient(client, f"SERVER~You just entered {groupToGo}")
            except Exception as e:
                print(e)
                sendMessageToClient(client, ERRORGENERAL)
        else:
            sendMessageToClient(client, ERRORGROUPNAME)

    
    # rps command
    elif message.startswith("/rps"):
        message = message.replace("/rps ","")
        whoToGame = message.split(" ",1)[0]
        clientToGameWith = activeClients[getClientKeyFromUsername(whoToGame)][0]
        # appending a game as a list: index 2 = round, index 3, 4 = moves for a round, index 5, 6, 7  =  result from each rounds.
        # a value of: -1 = not played, 0 = player1 wins, 1 = player2 wins, 2 = tie
        inLobby.append([client.getpeername()[1], clientToGameWith.getpeername()[1], 0, -1, -1, -1, -1, -1])
        print(inLobby)
        sendMessageToClient(client, f"SERVER~Waiting for response from {whoToGame}")
        sendMessageToClient(clientToGameWith, f"{activeClients[client.getpeername()[1]][1]}~Wants to play Rock Paper Scissors with you! Respond yes or no [y] or [n]")
        countDown(clientToGameWith, True)


    
    # Exit command
    elif message.startswith("/exit"):
        exitGroup = exit(client)
        if(exitGroup is not None):
            sendMessageToClient(client, f"SERVER~You just exited {exitGroup}")
        else:
            returnEmpty(client)
        
    
    # Shout command
    elif message.startswith("/shout"):
        broadcast(client, message)


    # bye command disconnect user from server
    elif message.startswith("/bye"):
        print("redirected to disconnect")
        disconnect(client)


    # Instructions command
    elif message.startswith("/instructions"):
        message = "SERVER~" + INSTRUCTIONS
        sendMessageToClient(client, message)


    elif message.startswith("/whereami"):
        whereami(client)


    elif message.startswith("/newusername"):
        newusername(client, message)

    else:
        sendMessageToClient(client, NOCOMMAND)



def newusername(client, message):
    message = message.replace("/newusername","")
    newUsername = message.split(" ", 1)[1]
    usernameTest = usernameCheck(newUsername)
    print(usernameTest)
    if usernameTest == True and newusername not in clients:
        oldUsername = activeClients[client.getpeername()[1]][1]
        activeClients[client.getpeername()[1]][1] = newUsername
        clients.remove(oldUsername)
        clients.append(newUsername)
        print(activeClients[client.getpeername()[1]][1])
        sendMessageToClient(client, str(client.getpeername()[1]) + " newusername " + newUsername)
        time.sleep(0.001)
        returnEmpty(client)
    else:
        sendMessageToClient(client, ERRORGENERAL)
    

def disconnect(client):
    print(activeClients[client.getpeername()[1]][1] + " disconnected from server")
    broadcast(client, f"SERVER~{activeClients[client.getpeername()[1]][1]} disconnected from server") # brukernavnet ligger i {activeClients[client.getpeername()[1]][1]}
    exit(client)
    sendMessageToClient(client, str(client.getpeername()[1]) + " disconnect") # kommandoen som igangsetter disconnect fra klientsiden
    print(client.getpeername()[1])
    activeClients.pop(client.getpeername()[1])
    client.close()

def whereami(client):
    area = MAINAREA
    for group, clients in chatGroups.items():
        if client.getpeername()[1] in clients:
            area = group
    whereYouAre = f'''
 ---------------------------------------------------------------------
| You are now in "{area}"                                             |
 ---------------------------------------------------------------------
    '''
    message = f"SERVER~{whereYouAre}"
    sendMessageToClient(client, message)


# exit lets you exit chatgroups
def exit(client):
    clientNumber = client.getpeername()[1]
    for group, clients in chatGroups.items():
        if clientNumber in clients:
            clients.remove(clientNumber)
            inGroupChat.remove(clientNumber)
            return group
    return None


# returnEmpty sendsmessage to 
def returnEmpty(client):
    sendMessageToClient(client, "§")


# sendMessageToClient sends message to clients
def sendMessageToClient(client, message):
    client.sendall(message.encode())


# broadcast sends messages between users and checks if users are in groupchat or in rps game before sending
def broadcast(client, message):
    if message.startswith("/shout") or message.startswith("SERVER"):
        if message.startswith("/shout"):
            message = message.replace("/shout ","")
            message = activeClients[client.getpeername()[1]][1] + "~Cried out to everyone: " + message
        for user in activeClients.values():
            if user[0] == client:
                returnEmpty(client)
            else:
                sendMessageToClient(user[0], message)
    else:
        for user in activeClients.values():
            if any(user[0].getpeername()[1] in sublist for sublist in inGame):
                continue
            elif user[0].getpeername()[1] in inGroupChat:
                continue
            elif user[0].getpeername()[1] == client.getpeername()[1]:
                returnEmpty(client)
            else:
                sendMessageToClient(user[0], message)


# login asks incomming connections if they are new users or returning users, and checks username
def login(client):
    while True:
        sendMessageToClient(client, LOGIN)
        message = client.recv(4096).decode(FORMAT)
        if(message.lower() == "n"):
            print("New user")
            sendMessageToClient(client, "SERVER~Please enter a unique username")
            while True:
                message = client.recv(4096).decode(FORMAT)
                goodname = usernameCheck(message)
                if not goodname:
                    sendMessageToClient(client, BADNAME)
                    continue
                elif message in clients:
                    sendMessageToClient(client, USERNAMEEXISTS)
                    continue
                else:
                    clients.append(message)
                    activeClients.update({client.getpeername()[1] : [client, message]})  # Bruker getpeername, altså porten som nøkkel.
                    message = str(client.getpeername()[1]) + " " + message
                    sendMessageToClient(client, message)
                break
            break
        elif(message.lower() == "r"):
            print("Returning user")
            sendMessageToClient(client, "SERVER~Please enter your username")
            while True:
                message = client.recv(4096).decode(FORMAT)
                if message in clients:
                    activeClients.update({client.getpeername()[1] : [client, message]})
                    returnUsername = str(client.getpeername()[1]) + " " + message
                    # returnUsername = "SERVER" + f"~{message}"
                    sendMessageToClient(client, returnUsername)
                    break
                else:
                    sendMessageToClient(client, ERRORUSERNAME)
                    continue
            break
        else:
            continue

# usernameCheck checks that the username doesnt contain illegal charcters or empty space
def usernameCheck(username):
    if username.find(" ") == -1 and username.find("/") == -1 and username.find("§") == -1 and username.find("~") == -1 and username != "":
        return True
    else:
        return False


# clienthandler handles all incomming connections
def clientHandler(client):
    
    # Server lytter etter client melding som inneholder brukernavn
    while True:
        username = client.recv(4096).decode(FORMAT)
        if(username == "login"):
            login(client)
        username = client.recv(4096).decode(FORMAT)
        if username != "":
            promptMessage = "SERVER~" + f"{username} added to the chat"
            welcomeMessage = WELCOME + INSTRUCTIONS
            sendMessageToClient(client, welcomeMessage)
            time.sleep(0.1)
            broadcast(client, promptMessage)
            break
        else:
            print("Client username is empty")
    threading.Thread(target=listenForMessages, args=(client,)).start()


# Main function
def main():
    # Lager socket klasse objektet
    # AF_INET: betyr at vi bruker IPv4
    # SOCK_STREAM: betyr at vi bruker TCP protocollen
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = ipv4, SOCK_STREAM = socketen skal ta i mot og sende strømmer
    # Setter options på socketten slik at adressen øyeblikkelig kan brukes på nytt ved restart, uten å vente på TIMEOUT
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # lager en try catch block
    try:
        # Gir serveren en adresse på formen host-IP og portnr
        server.bind((HOST, PORT))
        print(f"Serveren er oppe og kjører på {HOST} {PORT}")
    except:
        print(f"Klarte ikke å binde til host {HOST} og port {PORT}")

    # Setter en server grense
    server.listen(MAXCLIENTS)

    # Denne while loopen vil fortsette å lytte til clients som vil koble seg til
    while True:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        clientHandler(client)

        # # Lager en tråd som starter 
        # threading.Thread(target=clientHandler, args=(client, )).start()
    

if __name__ == "__main__":
    main()