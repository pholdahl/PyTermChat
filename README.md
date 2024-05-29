## PyTermChat

![Project Logo](/images/PyTermChat_0001.png)</br>

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Current State and Future Development](#current-state-and-future-development)
- [Technology Used](#technology-used)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## About the Project

PyTermChat is a Python-based chat application that allows multiple clients to connect to a server
and communicate with each other in real-time. Designed to operate in the terminal or console,
PyTermChat provides a straightforward interface for users to chat, play games, and manage their
presence in different chat groups. This project was originally based on a mandatory assignment
in [Networking and Cloud computing](https://student.oslomet.no/studier/-/studieinfo/emne/DATA2410/2022/H%C3%98ST), but it has been significantly extended to include additional
features like a Rock-Paper-Scissors game.

### Extensive Commenting

The code contains extensive comments, with almost every line commented.
This level of detail was required by our lecturer for a course assignment to
ensure clarity and thorough documentation of the code's functionality.

## Features

- **Multi-threaded Server:** Handles multiple clients simultaneously.
- **Broadcast Messaging:** Clients can send messages to all connected users.
- **Private Messaging:** Send private messages to specific users using the whisper command.
- **Chat Groups:** Join and communicate within specific chat groups.
- **Rock-Paper-Scissors Game:** Play a game of Rock-Paper-Scissors with other users.
- **User Management:** Change usernames, view online users, and track user locations.
- **Command-based Interface:** Intuitive commands for various actions (e.g., /shout, /list, /whisper, /rps).
- **Robust Error Handling:** Ensures smooth operation and provides meaningful error messages.

## Current State and Future Development

Currently, PyTermChat is fully functional with the features mentioned above. Future development may include:

- **Enhanced Game Options:** Adding more games and improving game mechanics.
- **User Authentication:** Implementing login systems with passwords.
- **Improved UI:** Enhancing the terminal interface for better user experience.
- **Logging and Monitoring:** Adding logging for server activity and user actions.
- **Security Enhancements:** Incorporating security features like encryption for messages.

## Technology Used

- **Python:** The main programming language used for both the server and client.
- **Socket Programming:** For handling network communication.
- **Multi-threading:** To manage multiple clients concurrently.
- **Terminal/Console Interface:** For user interaction.

## Dependencies

- Python 3.x
- Standard Python libraries: `socket`, `threading`, `time`

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your machine. You can download Python from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/PyTermChat.git

   ```

2. Navigate to the project directory:
   ```sh
   cd PyTermChat
   ```

### Running the Server

Start the server by running the following command:

```sh
python3 server.py
```

### Running the Client

Open a new terminal window and navigate to the project directory. Start the client by running:

```sh
python3 client.py
```

## Usage

### Commands

Once connected to the server, you can use the following commands:

- **/shout [message]:** Sends a message to everyone including chat groups.
- **/list:** Lists all online users.
- **/whisper [username] [message]:** Sends a private message to a specific user.
- **/chat [1-9]:** Joins a chat group (1-9).
- **/exit:** Leaves the current chat group.
- **/rps [username]:** Starts a game of Rock-Paper-Scissors with a user.
- **/newusername [username]:** Changes your username.
- **/whereami:** Displays your current location (main area or chat group).
- **/bye:** Disconnects from the server.
- **/instructions:** Displays the list of available commands.

### Playing Rock-Paper-Scissors

To start a game of Rock-Paper-Scissors with another user, use the /rps [username] command. The invited user must respond with **y** to accept or **n** to decline. Once the game starts, follow the prompts to choose Rock, Paper, or Scissors.

## Contributors

- This project was developed solely by me [Pholdahl](https://github.com/pholdahl).

## License

This project is licensed under the MIT License.
