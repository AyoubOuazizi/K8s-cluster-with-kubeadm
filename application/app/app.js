const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const kafka = require('kafka-node');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Connexion à Kafka
const kafkaClient = new kafka.KafkaClient({ kafkaHost: 'localhost:29092' });
const kafkaConsumer = new kafka.Consumer(kafkaClient, [{ topic: 'visualisation' }]);

// Route principale
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Gérer la connexion Socket.IO
io.on('connection', (socket) => {
    console.log('Client connected');

    // Écouter les messages du topic Kafka
    kafkaConsumer.on('message', (message) => {
        const data = JSON.parse(message.value);
        socket.emit('update', data);
    });

    // Gérer la déconnexion du client
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// Démarrer le serveur HTTP
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
