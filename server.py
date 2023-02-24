import socket                               # Importing the socket module
import threading                            # Importing the threading module for multithreading
import time                                 # Importing the time module

HOST = socket.gethostname()                 # Set the host to the current machine name
PORT = 9031                                 # Set the port number to 9031
FORMAT = "utf-8"                            # Set the character encoding format to UTF-8
MAXCLIENTS = 10

# Initiating ALLOT of constants used by the server to inform the clients
BADNAME = "SERVER~Please enter a username thats not empty, containing spaces or [/,§,~]"
USERNAMEEXISTS = "SERVER~Username already exists"
ERRORUSERNAME = "SERVER~Username doesn't exist in clientlist"
ERRORGROUPNAME = "SERVER~Group doesn't exist"
ERRORGENERAL = "SERVER~Something went wrong"
NOCOMMAND = "SERVER~Command does not exist"
MAINAREA = "The Ether"
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
| /newusername [username] -> to change your username                  |
| /whereami -> returns your position, the main area or in chatgroups  |
| /bye -> disconnects you from the server                             |
| /instructions -> returns this instruction overview                  |
 ---------------------------------------------------------------------
'''
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

# Initiating a GROUP constant dictionary contianing chatgroups for the clients to join
GROUP = {
    "chatgroup1":[],"chatgroup2":[],"chatgroup3":[],"chatgroup4":[], "chatgroup5": [],
    "chatgroup6": [], "chatgroup7": [], "chatgroup8": [], "chatgroup9": []}

clients = ["Pholdahl"]              # Existing usernames are stored in the clients list
activeClients = dict()              # activeClients stores usernames and client port number in a dictionary where the port number is the key
chatGroups = GROUP                  # chatGroups is a dictionary containing 9 different chatgroups with chatgroup[1-9] being the keys
inGroupChat = []                    # A list containing users in groupchat for easy access to search through for the broadcast function
inLobby = []                        # A short-time list for containing the pair of users just before the RPS game starts
inGame = []                         # A list for holding the users who are playing RPS


# Function that listens for messages and redirects them to the correct function in the server
def listenForMessages(client):
    while True:                                                                         # While loop
        try:                                                                            # Try to handle exceptions
            message = client.recv(4096).decode(FORMAT)                                  # Message receiver
            message = message.lstrip()                                                  # Stripping left part of message if containing empty space
            if message == "/bye":                                                       # If the message is "/bye"
                break                                                                   # We break the loop

            # Lobby message?
            elif any(client.getpeername()[1] in item for item in inLobby):              # If the client is in the inLobby list, the message will be a response for a RPS invite
                lobbyroom(client, message)                                              # Redirects the message to lobbyroom function


            # Game message?
            elif any(client.getpeername()[1] in item for item in inGame):               # If the client is in the inGame list, the message will be a gaming move message
                game(client, message)                                                   # Redirects the message to the game function


            # Groupchat message?                        
            elif client.getpeername()[1] in inGroupChat:                                # If the client is in the inGroupChat list, the message will only display for that group
                chatrooms(client, message)                                              # Redirects the message to the chatrooms function
            

            # Command message?
            elif message.startswith("/"):                                               # If the message starts with "/" it is a command message
                commandMessage(client, message)                                         # Redirects the message to the commandMessage function


            # Normal message?
            else:                                                                       # Otherwise
                message = activeClients[client.getpeername()[1]][1] + "~" + message     # Format the message to contain the username
                broadcast(client, message)                                              # Redirects the formatted message to the broacast function
                
        except Exception as e:                                                          # Catching exceptions
            print("Exception was:", e)                                                  # Printing exceptions
            break                                                                       # breaking the loop
    disconnect(client)                                                                  # Starting the disconnect function with the client object as paremeter
    

# Chatroom/Chatgroup function
def chatrooms(client, message):

    # Command message?
    if message.startswith("/"):                                                         # Also inside chatgroups, you can use the command messages
        commandMessage(client, message)                                                 # Redirects to the commandMessage function
    
    # Groupchat message
    else:                                                                               # Otherwise
        groupMemberNr = client.getpeername()[1]                                         # Getting the key/id (port number) of the client sending the message
        groupNr = None                                                                  # Initating a groupNr variable
        for key, value in GROUP.items():                                                # Searching through the GROUP dictionary to find the right group to send
            if groupMemberNr in value:                                                  # If clients key/id is in the group
                groupNr = key                                                           # GroupNr is equal to that key
        sendList = GROUP[groupNr]                                                       # The sendList will be equal to that list in the GROUP dictionary
        for m in sendList:                                                              # For member in sendList
            for clients in activeClients.values():                                      # For clients in activeClients dictionary
                # If that member equals the client sending the message
                if m == clients[0].getpeername()[1] and clients[0].getpeername()[1] == client.getpeername()[1]:
                    returnEmpty(client)                                                 # Return an empty message
                elif m == clients[0].getpeername()[1]:                                  # If that member is equal to a client in the activeClientList
                    # Send the message to that client, formatted correctly
                    sendMessageToClient(clients[0], activeClients[client.getpeername()[1]][1] + '~' + message)


"""
-----------------------------THE ROCK PAPER SCISSORS GAME FUNCTIONS-----------------------
"""
# Function to count down for the user who got invited to play RPS
def countDown(client, start):
    if start == True:                                           # If boolean start == True (which is an input paremeter in the countDown function)
        startTime = time.time()                                 # Initiate a startTime variable
        while start:                                            # As long as start == True
            if time.time() - startTime > 10:                    # If the start time subtracted from current time is larger than 10 (seconds)
                removeUsersFromGameLobby(client)                # Start the removeUsersFromGameLobby with the client as a paremeter
                break                                           # Break the loop
            elif start == False:                                # Or if start equals False
                return                                          # return from countDown function

# Function to remove clients from the inLobby list
def removeUsersFromGameLobby(client):
    userFound = False                                           # Initating a variable userFound as False
    index = 0                                                   # Initiating a index counter variable
    for game in inLobby:                                        # A for loop going through game lists in the inLobby list
        if client.getpeername()[1] in game:                     # If this clients port number is found in the game list in the inLobby list
            userFound = True                                    # The userFound variable will change to True
            break                                               # Breaking the for loop
        index += 1                                              # Adding to the index variable
    if userFound:                                               # If userFound is True
        gamePair = inLobby.pop(index)                           # Initiating a gamePair variable and poping the gamelist in the inLobby list containing the clients
        for clients in activeClients.values():                  # For loop to search through active clients
            if clients[0].getpeername()[1] == gamePair[0]:      # If the clients port number is equal to the gemPair lists index 0 (client to initate the game)
                # Send a decline message to that client
                sendMessageToClient(clients[0], f"SERVER~{activeClients[client.getpeername()[1]][1]} declined, or took too long to respond")
                returnEmpty(client)                             # Return empty to the client declining the game
                break                                           # Break
    else:                                                       # Otherwise
        return                                                  # Return


# Function to move the gamePair lists containing the client from the inLobby list to the inGame list
def moveUsersToGame(client):
    index = 0                                                   # Initiating a index counter variable
    for game in inLobby:                                        # A for loop going through game lists in the inLobby list
        if client.getpeername()[1] in game:                     # If this clients port number is found in the game list in the inLobby list
            break                                               # Breaking the for loop
        index += 1                                              # Adding to the index variable
    inGame.append(inLobby.pop(index))                           # Appending and popping the gamePair list from the inLobby to the inGame list

# Function to remove the clients from the game
def removeUsersFromGame(client):
    index = 0                                                   # Initiating a index counter variable
    for game in inGame:                                         # A for loop going through game lists in the inGame list
        if client.getpeername()[1] in game:                     # If this clients port number is found in the game list in the inGame list
            break                                               # Breaking the for loop
        index += 1                                              # Adding to the index variable
    inGame.remove(index)                                        # Removing that game list from the inGame list


# Function lobbyroom which is a short time area for the invited client to respond to playing or not playig a game of RPS
def lobbyroom(client, message):
    if message == "n":                                                          # If the message is "n" (no)
        removeUsersFromGameLobby(client)                                        # Starting removeUsersFromGameLobby function
    elif message == "y":                                                        # If the message is "y" (yes)
        returnEmpty(client)                                                     # Starts returnEmpty function to initate the prompt
        moveUsersToGame(client)                                                 # Statrs the moveUsersToGame function to move them into the inGame lis
        time.sleep(2)                                                           # Short sleep to not overflow the users with information
        gameRoom = findGameRoom(client)                                         # finding the gameList in the inGame list
        # Sending the gameinstructions to both players
        sendMessageToClient(activeClients[gameRoom[0]][0], GAMEINSTRUCTIONS)
        sendMessageToClient(activeClients[gameRoom[1]][0], GAMEINSTRUCTIONS)
        time.sleep(2)                                                           # Short sleep to not overflow the users with information
        gameRoom[2] += 1                                                        # Adding 1 to index 2 (round counter of the game = round 1)
        # Sending the gameinstructions to both players
        sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round{gameRoom[2]}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
        sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round{gameRoom[2]}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
    else:                                                                       # Otherwise
        # Prompt the client to respond correctly
        sendMessageToClient(client, "SERVER~You have to respond yes [y] or no [n]")


# Function that finds the gameList within the inGame list
def findGameRoom(client):
    index = 0                                                   # Initiating a index counter variable
    for game in inGame:                                         # A for loop going through game lists in the inGame list
        if client.getpeername()[1] in game:                     # If the clients port number is withing the gameList
            break                                               # Breaking the for loop                     
        index += 1                                              # Adding to the index variable
    return inGame[index]                                        # Returning the particular gameList from inGame list


# Explanation of the indexes in the gameList/gameRoom: [0,1] = clients, [2] = round, [3,4] = moves for a round, [5,6,7]  =  result from each rounds
# A value of -1 means that the game has not been played, the results are not in, no moves from the players have been taken
# activeClients[gameRoom[0]][0] gets the corresponding player as a client object from the activeClients list
# Function that controls the game
def game(client, message):
    gameRoom = findGameRoom(client)                                     # finding the gameList in the inGame list
    while gameRoom[3] == -1 or gameRoom[4] == -1:                       # Game loop as long as no moves have been initated
        endRound = False                                                # A boolean variable to confirm if a round has ended
        if message == "r" or message == "p" or message == "s":          # If message contains correct character
            moveToValue(client, message, gameRoom)                      # Use the function moveToValue to enter value into indexes in the gameList
            while gameRoom[3] != -1 and gameRoom [4] != -1:             # If both index 3 and 4 is not equal -1, then the round has ended
                rpsLogic(gameRoom)                                      # Start the rpsLogic function to figure out who won the round
                endRound = True                                         # Change booelan value endRound to True
                break                                                   # Break the while loop
            continue                                                    # If not in the second while loop, continue(move up to first while loop)
        elif message != "r" or message != "p" or message != "s":        # If message does not contain correct move characters
            # If check for which client and send a instruction message
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Wrong command, must choose between Rock[r], Paper[p] or Scissors[s]")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Wrong command, must choose between Rock[r], Paper[p] or Scissors[s]")
            break
    if endRound == True:                                                # If endRound is True, we end the round
        if gameRoom[int(gameRoom[2])+4] == 0:                           # If the roundpoint stored on index calculated by int(gameRoom[2])+4 == 0
            # The client who initated the game won that round
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~You won {int(gameRoom[2])} round")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Player1 won {int(gameRoom[2])} round")
        elif gameRoom[int(gameRoom[2])+4] == 1:                         # If the roundpoint stored on index calculated by int(gameRoom[2])+4 == 1
            # The client got invited to the game won that round
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Player2 won {int(gameRoom[2])} round")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~You won {int(gameRoom[2])} round")
        elif gameRoom[int(gameRoom[2])+4] == 2:                         # If the roundpoint stored on index calculated by int(gameRoom[2])+4 == 2
            # The round was a draw
            if client.getpeername()[1] == activeClients[gameRoom[0]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round {int(gameRoom[2])} was a draw")
            elif client.getpeername()[1] == activeClients[gameRoom[1]][0].getpeername()[1]:
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round {int(gameRoom[2])} was a draw")
        time.sleep(5)                                                   # Sleep 5 seconds to not overburden clients with information
        gameRoom[2] += 0.5                                              # Add 0.5 per user per round, when 2 players have used their move, round + 1.0 = next round
        gameRoom[3] = -1                                                # Setting move index 3 to -1, so we can repeat with the same game while loop
        gameRoom[4] = -1                                                # Setting move index 4 to -1, so we can repeat with the same game while loop
        if gameRoom[2] == 4.0:                                          # If the round index = 4, we are passed round 3, and we need to calulate which player is the winner
            player1Points = 0                                           # Variable for points for player1
            player2Points = 0                                           # Variable for points for player2
            for i in range(5,8):                                        # For loop checking index 5 to 7 of the gameList
                if gameRoom[i] == 0:                                    # If index i == 0
                    player1Points += 1                                  # Player 1 gets a point
                elif gameRoom[i] == 1:                                  # If index i == 1
                    player2Points += 1                                  # PLayer 2 gets a point
                elif gameRoom[i] == 2:                                  # If index i == 2
                    continue                                            # Its s draw, so continue
            if player1Points > player2Points:                           # If player1Points are more then player2Points
                # Send messages to the players who won, and who lost
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Congratulations, you won the game!")
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Buuhuu, you lost, get over it!")
            elif player2Points > player1Points:                         # If player2points are more the player1Points
                # Send messages to the playes who won, and who lost
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Congratulations, you won the game!")
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Buuhuu, you lost, get over it!")
            else:                                                       # Otherwise its a draw
                sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~The game was a draw")
                sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~The game was a draw")
            inGame.remove(gameRoom)                                     # The game is over, we remove the gameList from the inGame list
            time.sleep(3)                                               # Sleep for 3 seconds
            # Let infrom both users where they are on the server
            whereami(activeClients[gameRoom[0]][0])                   
            whereami(activeClients[gameRoom[1]][0])
            return                                                      # Return
        # If we are not passed the 3 round
        elif gameRoom[2].is_integer():
            # Send instruction messages to both clients
            sendMessageToClient(activeClients[gameRoom[0]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")
            sendMessageToClient(activeClients[gameRoom[1]][0], f"RPS~Round{int(gameRoom[2])}: What will you choose, Rock[r], Paper[p] or Scissors[s]?")


# Function that changes "r" "p" "s" to number values
def moveToValue(client, message, gameRoom):
    move = -1                                               # Initate the move as -1 to start with
    if message == "r":                                      # If message == "r"
        move = 0                                            # The move variable = 0
    elif message == "p":                                    # If message == "p"
        move = 1                                            # The move variable = 1
    elif message == "s":                                    # If message == "s"
        move = 2                                            # The move variable = 2
    if client.getpeername()[1] == gameRoom[0]:              # If the client with the message is equal to player1
        gameRoom[3] = move                                  # Place the move value inside index 3
    elif client.getpeername()[1] == gameRoom[1]:            # If the client with the message is equal to player2
        gameRoom[4] = move                                  # Place the move value inside index 4
    return


# Function that contains the logic to calculate points in the game
def rpsLogic(gameRoom):                             
    if (gameRoom[3] + 1) % 3 == gameRoom[4]:                # If the value on index 3 + 1 modulus 3 is equal to the value on index 4
        gameRoom[int(gameRoom[2])+4] = 1                    # Player 2 won the round
    elif (gameRoom[3] == gameRoom[4]):                      # If the value on index 3 is equal to the value on index 4
        gameRoom[int(gameRoom[2])+4] = 2                    # It is a draw
    else:                                                   # Otherwise
        gameRoom[int(gameRoom[2])+4] = 0                    # PLayer 1 won the round
    return      

"""
-----------------------END OF THE ROCK PAPER SCISSORS GAME FUNCTIONS---------------------
"""


# Function that returns the clientKey from activeUsers based on a username
def getClientKeyFromUsername(username):
    for key, value in activeClients.items():                # For loop to search through the activeClients dictionary
        if username == value[1]:                            # If username is equal to index 1 in value (username)
            return key                                      # Return that key
        

# Function that redirects command messages
def commandMessage(client, message):
    # List command
    if message == "/list":                                                          # If the message == "/list"
        clientKeyList = activeClients.keys()                                        # Get alle the keys in the dictionary
        count = len(clientKeyList)                                                  # Get the length of the list
        listOfClients = f"SERVER~There are currently {count} user(s) online:\n"       # Create the start of the message
        for clientKey in clientKeyList:                                             # Use a for loop to continue creating the message
            listOfClients += "[" + activeClients[clientKey][1] + "]\n"              # Adding usernames of active users to the message
        sendMessageToClient(client, listOfClients)                                  # Sending the message to the user
    
    # Whisper command
    elif message.startswith("/whisper"):                                            # If the message starts with "/whisper"                                
        message = message.replace("/whisper ","")                                   # Replace the start of the message with nothing
        try:                                                                        # Try to handle exceptions
            # Finding the client to send the message to
            userToWhisper = activeClients[getClientKeyFromUsername(message.split(" ",1)[0])][0]
            # Formatting the final message
            finalMessage = activeClients[client.getpeername()[1]][1] + "~Whispered: " + message.split(" ",1)[1]
            # Sending the final message
            sendMessageToClient(userToWhisper, finalMessage)
            returnEmpty(client)
        except:
            sendMessageToClient(client, ERRORUSERNAME)                              # Returning a standard errormessage to the client
            returnEmpty(client)

    # Chatgroup command
    elif message.startswith("/chat"):                                               # If the message starts with "/chat"
        message = message.replace("/chat ","")                                      # Replace the start of the message with nothing
        groupToGo = "chatgroup"+message.split(" ", 1)[0]                            # Format to find which chatgroup to go to
        if groupToGo in GROUP.keys():                                               # Figure out if this chatgroup exists as key in the GROUP dictionary    
            try:                                                                    # Try to handle exceptions
                exitGroup = exit(client)                                            # The exit function will return which group client exited if it was in a group
                GROUP[groupToGo] += [client.getpeername()[1]]                       # Adding the portnumber/clientKey to the chatgroup
                inGroupChat.append(client.getpeername()[1])                         # Also appendint to the inGroupChat list
                if(exitGroup is not None):                                          # If exitGroup is not None
                    # Return this message
                    sendMessageToClient(client, f"SERVER~You just exited {exitGroup} and entered {groupToGo}")
                else:                                                               # Otherwise
                    # Return this message
                    sendMessageToClient(client, f"SERVER~You just entered {groupToGo}")
            except Exception as e:                                                  # If there is an expetion
                print(e)                                                            # Print the exception
                sendMessageToClient(client, ERRORGENERAL)                           # Return a standard errormessage to the client
        else:                                                                       # Otherwise
            sendMessageToClient(client, ERRORGROUPNAME)                             # Return a standard errormessage to the client

    
    # rps command
    elif message.startswith("/rps"):                                                 # If the message startswith "/rps"
        message = message.replace("/rps ","")                                       # Replace the start of the message with nothing
        whoToGame = message.split(" ",1)[0]                                         # Store the username of the intited player in whoToGame
        clientToGameWith = activeClients[getClientKeyFromUsername(whoToGame)][0]    # Find the client by useing getClientKeyFromUserName function
        # Create and append a list with the current client on index 0, and the invited client on index 1, and also game logic values on the other indexes
        inLobby.append([client.getpeername()[1], clientToGameWith.getpeername()[1], 0, -1, -1, -1, -1, -1])
        # Send a message waiting to the current client
        sendMessageToClient(client, f"SERVER~Waiting for response from {whoToGame}")
        # Send a inviting message to the client intvited to play
        sendMessageToClient(clientToGameWith, f"{activeClients[client.getpeername()[1]][1]}~Wants to play Rock Paper Scissors with you! Respond yes or no [y] or [n]")
        countDown(clientToGameWith, True)                                           # Start the countdown function


    
    # Exit command                  
    elif message == "/exit":                                                        # If the message is equal "/exit"
        exitGroup = exit(client)                                                    # Store the returnvalue of exit fuction in exitGroup variable
        if(exitGroup is not None):                                                  # If the exitGroup variable contains a value
            sendMessageToClient(client, f"SERVER~You just exited {exitGroup}")      # Return a message of which group the client exited
        else:                                                                       # Otherwise
            returnEmpty(client)                                                     # Return empty
        
    
    # Shout command                     
    elif message.startswith("/shout"):                                              # If the message starts with "/shout"
        broadcast(client, message)                                                  # Redirect the message to the broadcast function


    # Bye command
    elif message == "/bye":                                                         # If the message is equal "/bye"
        disconnect(client)                                                          # Redirect the message to the disconnect function


    # Instructions command
    elif message == "/instructions":                                                # If the message is equal "/instructions"
        message = "SERVER~" + INSTRUCTIONS                                          # Format the message with the INSTRUCTIONS constant
        sendMessageToClient(client, message)                                        # Return the message to the client

    # Whereami command
    elif message == "/whereami":                                                    # If the message is equal "/wherami"
        whereami(client)                                                            # Redirect the message to the whereami function

    # Newusername command
    elif message.startswith("/newusername"):                                        # If the message startswith "/newusername"
        newusername(client, message)                                                # Redirect the message to the newusername function

    # Otherwise
    else:
        sendMessageToClient(client, NOCOMMAND)                                      # Return a standard NOCOMMAND message


# Function that lets the client change their username
def newusername(client, message):                                                   # Parameters are the current client and the message
    message = message.replace("/newusername","")                                    # Replacing the "/newusername" string with nothing
    newUsername = message.split(" ", 1)[1]                                          # Finding the new username in the message
    usernameTest = usernameCheck(newUsername)                                       # Running a usernameCheck and storing the result in variable usernameTest
    if usernameTest == True and newUsername not in clients:                         # If usernameTest is True and the newUsername is not in the clients list
        oldUsername = activeClients[client.getpeername()[1]][1]                     # Getting the old username
        activeClients[client.getpeername()[1]][1] = newUsername                     # Changing to the new username
        clients.remove(oldUsername)                                                 # Removing the old username from the clients list
        clients.append(newUsername)                                                 # Adding the new username to the cleints list
        # Return a message to the current client with both the client key (port number), and the new username keyword and the new username
        sendMessageToClient(client, str(client.getpeername()[1]) + " newusername " + newUsername)
        time.sleep(0.001)                                                           # Short sleep here to not overflow the messagePrinter of the client
        returnEmpty(client)                                                         # returnEmpty message to the client to trigger the prompt
    else:                                                                           # Otherwise
        sendMessageToClient(client, ERRORGENERAL)                                   # Return a general errormessage
    

# Function that lets the client disconnect from the server
def disconnect(client):                                                             # Takes in the client as parameter
    # Broadcasting the disconnect, the username is stored on index 1 of the list stored in the activeCliets dictionary {activeClients[client.getpeername()[1]][1]}
    broadcast(client, f"SERVER~{activeClients[client.getpeername()[1]][1]} disconnected from server")
    exit(client)                                                                    # Starting the exit function to remove the client from any chatgroups
    sendMessageToClient(client, str(client.getpeername()[1]) + " disconnect")       # Commando message that starts the disconnect prosess from the clientside
    activeClients.pop(client.getpeername()[1])                                      # Popping the client from the active clients dictionary
    client.close()                                                                  # Closing the client object


# Function that returns the position on the server, be it in the main area, or in a groupchat
def whereami(client):                                                               # Takes in the client as paremeter
    area = MAINAREA                                                                 # As a standard the MAINAREA constant is the area
    for group, clients in GROUP.items():                                            # A for loop searching through the GROUP dictionary
        if client.getpeername()[1] in clients:                                      # If client portnumber(key) is found
            area = group                                                            # Area variable is equal to that group
            break                                                                   # Break the loop
    # Message of where the user is
    whereYouAre = f'''                                                               
 ---------------------------------------------------------------------
| You are now in "{area}"                                         
 ---------------------------------------------------------------------
    '''
    message = f"SERVER~{whereYouAre}"                                               # Final message
    sendMessageToClient(client, message)                                            # Sending message to client


# Function that let you exit chatgroups
def exit(client):                                                                   # Takes in the client as paremeter                                          
    for group, clients in GROUP.items():                                            # For loop to serach through to find matching client port number
        if client.getpeername()[1] in clients:                                      # If matching port number (key)
            clients.remove(client.getpeername()[1])                                 # Remove from the listvalue clients of that key in the dictionary
            inGroupChat.remove(client.getpeername()[1])                             # Also remove from the inGroupChat list
            return group                                                            # Return the groupchat key
    return None                                                                     # Otherwise return None


# Function that sends a message to client containing a key character
def returnEmpty(client):                                                # Takes in the paremeter Client 
    sendMessageToClient(client, "§")                                    # Sends message to that client with the key character "§"


# Function that sends messages to a client
def sendMessageToClient(client, message):                               # Takes in the paremeter Client and a message
    client.sendall(message.encode())                                    # Uses the client objects sendall method and encodes the message


# Function that broadcasts messages to other clients
def broadcast(client, message):                                         # Takes in the client and message as paremeter
    if message.startswith("/shout") or message.startswith("SERVER"):    # If the message starts with "/shout" or "SERVER"
        if message.startswith("/shout"):                                # If the message starts with "/shout"
            message = message.replace("/shout ","")                     # replace that part with nothing
            # Format the message so that it corresponds to the "/shout" command
            message = activeClients[client.getpeername()[1]][1] + "~Cried out to everyone: " + message
        for user in activeClients.values():                             # For loop going through all the active clients
            if user[0] == client:                                       # If the client object in activeClients dictionary is equal to the current client
                returnEmpty(client)                                     # Use the returnEmpty function
            else:                                                       # Otherwise
                sendMessageToClient(user[0], message)                   # Send the message
    else:                                                               # Otherwise
        for user in activeClients.values():                             # For loop going through all the active clients
            # If any of the clients is also in a game
            if any(user[0].getpeername()[1] in sublist for sublist in inGame):
                continue                                                # Do not send message
            elif user[0].getpeername()[1] in inGroupChat:               # If they are in a grouChat
                continue                                                # Do not send message
            elif user[0].getpeername()[1] == client.getpeername()[1]:   # If it is the current client
                returnEmpty(client)                                     # Use the returnEmpty function
            else:                                                       # Otherwise
                sendMessageToClient(user[0], message)                   # Send the message


# Function that prompts the user for a login
def login(client):                                                                      # Takes client as input paremeter
    while True:                                                                         # While loop
        sendMessageToClient(client, LOGIN)                                              # Sends a message to the client with the standard LOGIN constant
        message = client.recv(4096).decode(FORMAT)                                      # Receives the message from the client
        if(message.lower() == "n"):                                                     # If message is equal to "n"                         
            sendMessageToClient(client, "SERVER~Please enter a unique username")        # Send message to client
            while True:                                                                 # While loop
                message = client.recv(4096).decode(FORMAT)                              # Receives the message from the client
                goodname = usernameCheck(message)                                       # Check the username store result in goodname variable
                if not goodname:                                                        # If not goodname
                    sendMessageToClient(client, BADNAME)                                # Send message to client with BADNAME instructions
                    continue                                                            # Continue to go back to the start of the while loop
                elif message in clients:                                                # If message exists in clients list
                    sendMessageToClient(client, USERNAMEEXISTS)                         # Send message to client with USERNAMEEXISTS instructions
                    continue                                                            # Continue to go back to the start of the while loop
                else:                                                                   # Otherwise
                    clients.append(message)                                             # Message containing the username is approved, append it to the clients list
                    activeClients.update({client.getpeername()[1] : [client, message]}) # Update the activeClients dictionary using the portnumber as key
                    message = str(client.getpeername()[1]) + " " + message              # Formatting a message containing also the portnumber
                    sendMessageToClient(client, message)                                # Returning the message with the portnumber as a userID and the username to confirm
                break                                                                   # Breaking the loop
            break
        elif(message.lower() == "r"):                                                   # If message is equal to "r"    
            sendMessageToClient(client, "SERVER~Please enter your username")            # Sends message to client
            while True:                                                                 # While loop
                message = client.recv(4096).decode(FORMAT)                              # Receiving incomming message from the client
                if message in clients:                                                  # Cheching if the username in the message exists in the clients list
                    activeClients.update({client.getpeername()[1] : [client, message]}) # If so add the client and the username to the activeClients dictionary
                    returnUsername = str(client.getpeername()[1]) + " " + message       # Create a returnmessage to the client with the port number and the username
                    sendMessageToClient(client, returnUsername)                         # Sending the reutrnmessage to the client
                    break                                                               # Break the loop
                else:                                                                   # Otherwise
                    sendMessageToClient(client, ERRORUSERNAME)                          # Send a standards ERRORUSERNAME message
                    continue                                                            # Continue to get back to the start of the while loop
            break                                                                       # Break
        else:                                                                           # Otherwise
            continue                                                                    # Continue to get back to the start of the while loop

# Function to check that the username doent contain illegal characters or spaces
def usernameCheck(username):                                                            # Takes a message string which should be a username as input parameter
    if username.find(" ") == -1 and username.find("/") == -1 and username.find("§") == -1 and username.find("~") == -1 and username != "":
        return True
    else:
        return False


# clienthandler handles all incomming connections
def clientHandler(client):                                                              # Takes a client as input parameter
    while True:                                                                         # While loop
        username = client.recv(4096).decode(FORMAT)                                     # First message from client connecting should allways be "login"
        if(username == "login"):                                                        # Check if the username is "login"
            login(client)                                                               # If so, start login function
        username = client.recv(4096).decode(FORMAT)                                     # The client sends automaticly the correct username after login
        if username != "":                                                              # As long as username not empty 
            promptMessage = "SERVER~" + f"{username} added to the chat"                 # A promptmessage is created
            welcomeMessage = WELCOME + INSTRUCTIONS                                     # A welcome message is also created
            sendMessageToClient(client, welcomeMessage)                                 # Sends the welcome message to the client
            time.sleep(0.1)                                                             # A little sleeptime to not overflow the sendMessageToClient function
            broadcast(client, promptMessage)                                            # Broadcast to everyone on the server about the client joining the chat
            break                                                                       # Break
        else:                                                                           # Otherwise
            print("User tried to connect with empty username")                          # Print a message about empty username
    threading.Thread(target=listenForMessages, args=(client,)).start()                  # Start a listenForMessages function thread


# Main function to define the server object and start the clientHandler
def main():
    # Create a socket class object
    # AF_INET: Is for using IPv4
    # SOCK_STREAM: Is for using the TCP protocol betyr at vi bruker TCP protocollen
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  # AF_INET = ipv4, SOCK_STREAM = socketen should list for and send streams of data
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                # Set option for the socket such that the same address can be used at restart

    try:
        server.bind((HOST, PORT))                                               # Binds the server with the tuple containing constants HOST and PORT
        print(f"The server is up and running and ready at {HOST} {PORT}")       # Printing confirming message in the terminal
    except Exception as e:                                                      # Collect exception
        print(e)                                                                # Print the exception
        print(f"Klarte ikke å binde til host {HOST} og port {PORT}")            # Print a standard message

    server.listen(MAXCLIENTS)                                                   # Make the server listen for clients and sets a max limit

    while True:                                                                 # While loop
        client, address = server.accept()                                       # Accepting incomming connections
        print(f"Successfully connected to client {address[0]} {address[1]}")    # Print confirming client connection in terminal
        clientHandler(client)                                                   # Sends the client object to the clientHandler function
    

# Standard python start command
if __name__ == "__main__":
    main()