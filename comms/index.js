const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

const DUMMY_API_URL = 'http://127.0.0.1:7991/chat'; // Replace with your actual API endpoint

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('QR RECEIVED. Scan this with your WhatsApp app:');
    qrcode.generate(qr, { small: false });
});

client.on('ready', () => {
    console.log('Client is ready! Connected to WhatsApp Web');
});

client.on('authenticated', () => {
    console.log('Authentication successful');
});

client.on('auth_failure', (msg) => {
    console.error('Authentication failure:', msg);
});

client.on('message', async (message) => {
    console.log(`Message received from ${message.from}: ${message.body}`);
    
    try {
        const response = await axios.post(DUMMY_API_URL, {
            sender: message.from,
            message: message.body,
            timestamp: new Date().toISOString(),
            messageId: message.id._serialized
        });
        console.log('API response:', response.status, response.data);
    } catch (error) {
        console.error('Error calling API:', error.message);
    }
});

app.post('/send-message', async (req, res) => {
    const { to, text } = req.body;
    try {
        const formattedNumber = to.includes('@c.us') ? to : `${to}@c.us`;
        const sent = await client.sendMessage(formattedNumber, text);
        res.json({ success: true, message: `Message sent to ${to}`, data: sent });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

client.initialize();

app.listen(PORT, () => {
    console.log(`WhatsApp Web server running on port ${PORT}`);
});