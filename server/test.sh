curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "player1=Tyler&player2=Erin" http://localhost:50124/newGame
curl -X POST -H "Content-Type: application/json" -d "{\"gameId\":\"1\", \"xVel\":\"0.0\", \"yVel\":\"-100.00\"}" http://localhost:50124/shoot
curl -X POST -H "Content-Type: application/json" -d "{\"gameId\":\"1\", \"xVel\":\"0.0\", \"yVel\":\"-100.00\"}" http://localhost:50124/shoot