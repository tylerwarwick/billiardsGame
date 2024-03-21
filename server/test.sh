curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "player1=Tyler&player2=Erin" http://localhost:50124/newGame
curl -X POST -H "Content-Type: application/json" -d "{\"gameId\":\"2\", \"xVel\":\"0\", \"yVel\":\"-10000\"}" http://localhost:50124/shoot
