# Esempio MQTT con JavaScript (Browser)

Questo esempio mostra come connettersi a un broker MQTT tramite WebSocket usando JavaScript in una pagina web.

## Requisiti

- Broker Mosquitto configurato con WebSocket sulla porta 9001
- Browser moderno con supporto WebSocket

## Codice HTML/JavaScript

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MQTT WebSocket Test</title>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            margin: 20px 0;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 4px;
            margin: 5px;
        }
        button:hover {
            background: #0056b3;
        }
        #messages {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px;
            height: 300px;
            overflow-y: scroll;
            font-family: monospace;
        }
        input, select {
            padding: 8px;
            margin: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>🚀 Test MQTT WebSocket</h1>
    
    <div class="container">
        <h3>📡 Connessione</h3>
        <input type="text" id="broker" value="ws://localhost:9001" placeholder="Broker URL">
        <button onclick="connect()">Connetti</button>
        <button onclick="disconnect()">Disconnetti</button>
        <span id="status">❌ Disconnesso</span>
    </div>
    
    <div class="container">
        <h3>📤 Pubblica Messaggio</h3>
        <input type="text" id="pubTopic" value="test/javascript" placeholder="Topic">
        <input type="text" id="pubMessage" value="Ciao da JavaScript!" placeholder="Messaggio">
        <button onclick="publishMessage()">Pubblica</button>
    </div>
    
    <div class="container">
        <h3>📥 Sottoscrivi Topic</h3>
        <input type="text" id="subTopic" value="test/+" placeholder="Topic (supporta wildcards)">
        <button onclick="subscribe()">Sottoscrivi</button>
        <button onclick="unsubscribe()">Annulla sottoscrizione</button>
    </div>
    
    <div class="container">
        <h3>💬 Messaggi Ricevuti</h3>
        <div id="messages"></div>
        <button onclick="clearMessages()">Pulisci</button>
    </div>

    <script>
        let client = null;
        let connected = false;
        
        function addMessage(message, type = 'info') {
            const messages = document.getElementById('messages');
            const timestamp = new Date().toLocaleTimeString();
            const messageDiv = document.createElement('div');
            messageDiv.innerHTML = `[${timestamp}] ${message}`;
            messageDiv.style.color = type === 'error' ? 'red' : type === 'success' ? 'green' : 'black';
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function updateStatus(status, color) {
            const statusElement = document.getElementById('status');
            statusElement.textContent = status;
            statusElement.style.color = color;
        }
        
        function connect() {
            const brokerUrl = document.getElementById('broker').value;
            
            try {
                addMessage(`🔗 Tentativo di connessione a ${brokerUrl}...`);
                
                client = mqtt.connect(brokerUrl, {
                    clientId: 'mqtt_js_' + Math.random().toString(16).substr(2, 8),
                    keepalive: 60,
                    clean: true
                });
                
                client.on('connect', function () {
                    connected = true;
                    updateStatus('✅ Connesso', 'green');
                    addMessage('✅ Connesso al broker MQTT!', 'success');
                });
                
                client.on('message', function (topic, message) {
                    const msg = message.toString();
                    addMessage(`📨 ${topic}: ${msg}`, 'info');
                });
                
                client.on('error', function (error) {
                    addMessage(`❌ Errore: ${error.message}`, 'error');
                    updateStatus('❌ Errore', 'red');
                });
                
                client.on('close', function () {
                    connected = false;
                    updateStatus('❌ Disconnesso', 'red');
                    addMessage('🔌 Disconnesso dal broker', 'info');
                });
                
            } catch (error) {
                addMessage(`❌ Errore di connessione: ${error.message}`, 'error');
            }
        }
        
        function disconnect() {
            if (client && connected) {
                client.end();
                addMessage('👋 Disconnessione richiesta', 'info');
            }
        }
        
        function publishMessage() {
            if (!connected) {
                addMessage('❌ Non connesso al broker!', 'error');
                return;
            }
            
            const topic = document.getElementById('pubTopic').value;
            const message = document.getElementById('pubMessage').value;
            
            if (!topic || !message) {
                addMessage('❌ Topic e messaggio sono obbligatori!', 'error');
                return;
            }
            
            client.publish(topic, message, function (error) {
                if (error) {
                    addMessage(`❌ Errore pubblicazione: ${error.message}`, 'error');
                } else {
                    addMessage(`📤 Pubblicato su ${topic}: ${message}`, 'success');
                }
            });
        }
        
        function subscribe() {
            if (!connected) {
                addMessage('❌ Non connesso al broker!', 'error');
                return;
            }
            
            const topic = document.getElementById('subTopic').value;
            
            if (!topic) {
                addMessage('❌ Topic è obbligatorio!', 'error');
                return;
            }
            
            client.subscribe(topic, function (error) {
                if (error) {
                    addMessage(`❌ Errore sottoscrizione: ${error.message}`, 'error');
                } else {
                    addMessage(`🔔 Sottoscritto a: ${topic}`, 'success');
                }
            });
        }
        
        function unsubscribe() {
            if (!connected) {
                addMessage('❌ Non connesso al broker!', 'error');
                return;
            }
            
            const topic = document.getElementById('subTopic').value;
            
            if (!topic) {
                addMessage('❌ Topic è obbligatorio!', 'error');
                return;
            }
            
            client.unsubscribe(topic, function (error) {
                if (error) {
                    addMessage(`❌ Errore annullamento sottoscrizione: ${error.message}`, 'error');
                } else {
                    addMessage(`🔕 Annullata sottoscrizione a: ${topic}`, 'success');
                }
            });
        }
        
        function clearMessages() {
            document.getElementById('messages').innerHTML = '';
        }
        
        // Connessione automatica al caricamento della pagina
        window.onload = function() {
            addMessage('🚀 Pagina caricata. Clicca su "Connetti" per iniziare.', 'info');
        };
        
        // Gestione input Enter
        document.getElementById('pubMessage').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                publishMessage();
            }
        });
        
        document.getElementById('subTopic').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                subscribe();
            }
        });
    </script>
</body>
</html>
```

## Come utilizzare l'esempio

1. **Avvia Mosquitto** con WebSocket abilitato (porta 9001)
2. **Salva il codice** in un file `.html`
3. **Apri il file** in un browser web
4. **Clicca su "Connetti"** per connetterti al broker
5. **Pubblica messaggi** e **sottoscrivi topic** per testare la comunicazione

## Funzionalità

- ✅ Connessione/disconnessione al broker MQTT
- ✅ Pubblicazione di messaggi su topic specifici
- ✅ Sottoscrizione a topic (supporta wildcards come `+` e `#`)
- ✅ Visualizzazione dei messaggi ricevuti in tempo reale
- ✅ Interfaccia grafica intuitiva
- ✅ Gestione degli errori

## Topic Wildcards

- `+`: sostituisce un singolo livello del topic
  - Esempio: `casa/+/temperatura` cattura `casa/soggiorno/temperatura`, `casa/cucina/temperatura`
- `#`: sostituisce tutti i livelli successivi
  - Esempio: `casa/#` cattura tutti i topic che iniziano con `casa/`

## Note

- Assicurati che il broker Mosquitto sia configurato con WebSocket sulla porta 9001
- Per test locali, usa `ws://localhost:9001`
- Per connessioni HTTPS, usa `wss://` invece di `ws://`