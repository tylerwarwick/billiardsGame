# Pool Game Project

This project showcases the development of a pool game from scratch, including the creation of a physics engine in C, a server to serve both the frontend and handle game state management, and a user-friendly frontend interface. 
It was developed for the infamous CIS2750 class (known colloquially as the angel of death) at the University of Guelph in 2024. As an engineering student I took it as an elective to help bolster my software development skills!

## Table of Contents

- [Physics Engine](#physics-engine)
- [Server](#server)
- [Frontend](#frontend)
- [Installation and Usage](#installation-and-usage)

## Physics Engine

The pool game's physics engine was developed in C to accurately simulate ball movements, collisions, and interactions. Key features of the physics engine include:

- **Ball Movement:** Implementation of realistic ball movements based on factors such as velocity, friction, and basic collision dynamics.
- **Collision Detection:** Accurate detection of collisions between balls and between balls and walls.
- **Collision Resolution:** Proper handling of collisions to determine the resulting velocities and directions of balls post-collision.

## Server

The server component of the project serves multiple purposes, including serving the frontend interface to users, managing game state, and storing data in a database. Key functionalities of the server include:

- **Frontend Serving:** Serving a user-friendly frontend interface for players to interact with the pool game.
- **Game State Management:** Handling game state, including player actions, ball positions, scores, and game progression.
- **Database Integration:** Storing and retrieving game states from a database to ensure persistence and allow for resuming games.

## Frontend

The frontend interface provides an intuitive and visually appealing platform for players to engage with the pool game. Key features of the frontend include:

- **Game Interface:** Displaying the pool table, balls, cues, and other game elements in a visually appealing manner.
- **User Interaction:** Allowing players to interact with the game through mouse or touch controls for aiming and shooting.
- **Score Display:** Showing scores, player turns, and game progress in a clear and understandable format.

## Installation and Usage

To run the pool game using Docker:

1. **Clone the Repository:** Clone this repository to your local machine.
   ```bash
   git clone https://github.com/tylerwarwick/billiardsGame.git

2. **Navigate to the Repository Directory:** 
   ```bash
   cd billiardsGame

3. **Build Docker Image:** Build the Docker image using the provided Dockerfile.
   ```bash
   docker build -t billiards_game .

4. **Run Docker Container:** Run the Docker container from the built image.
   ```bash
   docker run -p 3000:3000 billiards_game

5. **Access Frontend:** Open a web browser and navigate to the following address to play some pool!
   ```plaintext
   http://localhost:3000
