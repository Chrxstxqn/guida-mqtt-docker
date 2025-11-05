# Esempio MQTT con Node.js

Questo esempio mostra come creare un client MQTT con Node.js per pubblicare e ricevere messaggi.

## Installazione

```bash
npm init -y
npm install mqtt
```

## Codice Client MQTT

```javascript
const mqtt = require('mqtt');

// Configurazione broker
const BROKER_URL = 'mqtt://localhost:1883';
const CLIENT_ID = 'nodejs_client_' + Math.random().toString(16).substr(2, 8);

// Opzioni di connessione
const options = {
    clientId: CLIENT_ID,
    keepalive: 60,
    clean: true,
    reconnectPeriod: 1000,
};

// Topics
const TOPICS = {
    temperature: 'casa/temperatura/soggiorno',
    humidity: 'casa/umidita/soggiorno',
    movement: 'casa/sensori/movimento',
    status: 'dispositivi/stato/online'
};

console.log('🚀 Avvio client MQTT Node.js...');

// Creazione client
const client = mqtt.connect(BROKER_URL, options);

// Event: Connessione stabilita
client.on('connect', function () {
    console.log('✅ Connesso al broker MQTT!');
    console.log(`📡 Client ID: ${CLIENT_ID}`);
    
    // Sottoscrizione ai topic
    Object.values(TOPICS).forEach(topic => {
        client.subscribe(topic, function (err) {
            if (!err) {
                console.log(`🔔 Sottoscritto a: ${topic}`);
            } else {
                console.error(`❌ Errore sottoscrizione ${topic}:`, err);
            }
        });
    });
    
    // Avvia simulazione sensori
    startSensorSimulation();
});

// Event: Messaggio ricevuto
client.on('message', function (topic, message) {
    try {
        const payload = message.toString();
        const timestamp = new Date().toLocaleTimeString();
        console.log(`📨 [${timestamp}] ${topic}: ${payload}`);
        
        // Parsing JSON se possibile
        try {
            const data = JSON.parse(payload);
            console.log('   📊 Dati parsati:', data);
        } catch (e) {
            // Non è JSON, ignorare
        }
    } catch (error) {
        console.error('❌ Errore nel processare il messaggio:', error);
    }
});

// Event: Errore
client.on('error', function (error) {
    console.error('❌ Errore MQTT:', error);
});

// Event: Disconnessione
client.on('close', function () {
    console.log('🔌 Disconnesso dal broker MQTT');
});

// Event: Riconnessione
client.on('reconnect', function () {
    console.log('🔄 Tentativo di riconnessione...');
});

// Funzione per simulare dati sensori
function startSensorSimulation() {
    console.log('📊 Avvio simulazione sensori...');
    
    // Pubblica dati ogni 5 secondi
    setInterval(() => {
        publishSensorData();
    }, 5000);
    
    // Pubblica stato dispositivo ogni 30 secondi
    setInterval(() => {
        publishDeviceStatus();
    }, 30000);
}

// Funzione per pubblicare dati sensori
function publishSensorData() {
    // Dati casuali per simulazione
    const temperature = +(Math.random() * 10 + 18).toFixed(1); // 18-28°C
    const humidity = Math.floor(Math.random() * 40 + 40); // 40-80%
    const movement = Math.random() > 0.7; // 30% probabilità movimento
    
    // Pubblica temperatura
    const tempData = {
        valore: temperature,
        unita: '°C',
        timestamp: new Date().toISOString(),
        sensore: 'DHT22'
    };
    
    client.publish(TOPICS.temperature, JSON.stringify(tempData), (err) => {
        if (!err) {
            console.log(`📤 Temperatura pubblicata: ${temperature}°C`);
        }
    });
    
    // Pubblica umidità
    const humidityData = {
        valore: humidity,
        unita: '%',
        timestamp: new Date().toISOString(),
        sensore: 'DHT22'
    };
    
    client.publish(TOPICS.humidity, JSON.stringify(humidityData), (err) => {
        if (!err) {
            console.log(`📤 Umidità pubblicata: ${humidity}%`);
        }
    });
    
    // Pubblica movimento (solo se rilevato)
    if (movement) {
        const movementData = {
            movimento_rilevato: true,
            timestamp: new Date().toISOString(),
            sensore: 'PIR',
            zona: 'soggiorno'
        };
        
        client.publish(TOPICS.movement, JSON.stringify(movementData), (err) => {
            if (!err) {
                console.log('📤 Movimento rilevato!');
            }
        });
    }
}

// Funzione per pubblicare stato dispositivo
function publishDeviceStatus() {
    const statusData = {
        online: true,
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memoria: process.memoryUsage(),
        versione: process.version
    };
    
    client.publish(TOPICS.status, JSON.stringify(statusData), (err) => {
        if (!err) {
            console.log('📤 Stato dispositivo aggiornato');
        }
    });
}

// Gestione segnali di sistema
process.on('SIGINT', function() {
    console.log('\n🛑 Interruzione ricevuta. Chiusura client...');
    
    // Pubblica messaggio di shutdown
    const shutdownMsg = {
        online: false,
        timestamp: new Date().toISOString(),
        motivo: 'shutdown'
    };
    
    client.publish(TOPICS.status, JSON.stringify(shutdownMsg), () => {
        client.end();
        process.exit(0);
    });
});

console.log('🔗 Tentativo di connessione al broker...');
```

## Utilizzo

1. **Salva il codice** in un file `mqtt-client.js`
2. **Installa le dipendenze**: `npm install mqtt`
3. **Avvia il client**: `node mqtt-client.js`
4. **Osserva i messaggi** in MQTT Explorer o in altri client

## Funzionalità

- ✅ Connessione automatica al broker
- ✅ Sottoscrizione automatica ai topic
- ✅ Simulazione dati sensori (temperatura, umidità, movimento)
- ✅ Pubblicazione periodica dello stato del dispositivo
- ✅ Riconnessione automatica in caso di disconnessione
- ✅ Gestione graceful dello shutdown

## Personalizzazioni

- Modifica `BROKER_URL` per connetterti a broker remoti
- Aggiungi autenticazione modificando le `options`
- Personalizza i topic nel oggetto `TOPICS`
- Modifica la frequenza di pubblicazione negli `setInterval`