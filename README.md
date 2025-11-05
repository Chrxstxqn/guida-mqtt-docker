# Guida all'uso di MQTT con Docker e MQTT Explorer

![MQTT](https://img.shields.io/badge/MQTT-v5.0-blue)
![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Una guida completa e pratica per l'installazione e configurazione di **Mosquitto MQTT Broker** tramite **Docker Desktop** e l'utilizzo di **MQTT Explorer** per testare e monitorare i messaggi MQTT.

## 📋 Indice

- [Cos'è MQTT?](#cosè-mqtt)
- [Requisiti](#requisiti)
- [Installazione Docker Desktop](#installazione-docker-desktop)
- [Configurazione Mosquitto con Docker](#configurazione-mosquitto-con-docker)
- [Installazione MQTT Explorer](#installazione-mqtt-explorer)
- [Configurazione MQTT Explorer](#configurazione-mqtt-explorer)
- [Test e Utilizzo](#test-e-utilizzo)
- [Struttura del Progetto](#struttura-del-progetto)
- [Licenza](#licenza)

## 🤔 Cos'è MQTT?

**MQTT** (Message Queuing Telemetry Transport) è un protocollo di comunicazione leggero basato sul modello **publish/subscribe**. È stato progettato per essere semplice ed efficiente, anche in reti con poca banda o connessioni instabili, motivo per cui è molto utilizzato nell'**Internet of Things (IoT)**.

### Architettura MQTT

L'architettura MQTT è composta da tre elementi principali:

- **Client**: dispositivi o applicazioni che inviano o ricevono messaggi
- **Broker**: il server centrale (es. Mosquitto) che smista i messaggi
- **Topic**: i "canali" logici in cui si pubblicano i dati (es. `casa/temperatura/soggiorno`)

```
Client (Publisher) → Broker → Client (Subscriber)
```

### Vantaggi di MQTT

- ✅ **Leggerezza**: protocollo minimale e efficiente
- ✅ **Affidabilità**: diversi livelli di Quality of Service (QoS)
- ✅ **Persistenza**: messaggi persistenti e retained messages
- ✅ **Scalabilità**: supporta reti con molti dispositivi

## 📋 Requisiti

### Software Necessario

- **Docker Desktop** (Windows/macOS)
- **MQTT Explorer**

### Requisiti di Sistema

- Windows 10/11 con WSL2 attivo, oppure macOS
- Almeno 4 GB di RAM
- Accesso come amministratore

## 🐳 Installazione Docker Desktop

### Download

1. Vai al sito ufficiale: [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
2. Scarica la versione adatta al tuo sistema operativo

### Installazione su Windows

1. Avvia l'installer
2. Segui i passaggi lasciando le opzioni predefinite (incluso WSL2)
3. Completa e riavvia se richiesto
4. Al primo avvio effettua l'accesso o crea un account Docker Hub

### Installazione su macOS

1. Apri il file `.dmg`
2. Trascina l'icona di Docker in "Applicazioni"
3. Avvia Docker Desktop e accedi con il tuo profilo Docker Hub

## ⚙️ Configurazione Mosquitto con Docker

### Passo 1: Aprire Docker Desktop

Avvia Docker Desktop e vai alla sezione **Containers** dal menù laterale.

### Passo 2: Scaricare l'immagine Mosquitto

1. Vai su **Images**
2. Nel campo di ricerca inserisci `eclipse-mosquitto`
3. Sul primo risultato premi **Pull**
4. Docker scaricherà l'immagine ufficiale di Mosquitto dal Docker Hub

### Passo 3: Configurare il container

Nella schermata di configurazione imposta:

- **Container name**: `mosquitto`
- **Ports**: 
  - `1883:1883` (porta MQTT standard)
  - `9001:9001` (opzionale per WebSocket)
- **Volumes** (consigliato per persistenza):
  - `config → /mosquitto/config`
  - `data → /mosquitto/data`
  - `log → /mosquitto/log`

### Passo 4: Creare il file di configurazione

Crea una cartella `mosquitto` sul tuo PC con le sottocartelle `config`, `data`, `log`.

Nella cartella `config`, crea un file `mosquitto.conf`:

```conf
# Configurazione base Mosquitto
persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log

# Listener porta standard MQTT
listener 1883
allow_anonymous true

# Listener WebSocket (opzionale)
listener 9001
protocol websockets
```

### Passo 5: Avviare il container

1. Torna su **Containers**
2. Trova il tuo container `mosquitto`
3. Premi **Start**
4. Verifica i logs per confermare che il broker sia attivo sulla porta 1883

## 🔍 Installazione MQTT Explorer

### Download

- Visita [mqtt-explorer.com](https://mqtt-explorer.com/)
- Scarica la versione per il tuo sistema operativo

### Installazione

**Windows**: Avvia il file `.exe` e segui i passaggi guidati

**macOS**: Apri il file `.dmg` e trascina l'app in "Applicazioni"

## 🌐 Configurazione MQTT Explorer

### Passo 1: Creare una nuova connessione

1. Apri MQTT Explorer
2. Clicca su "**Add new connection**"
3. Configura i parametri:
   - **Name**: `Mosquitto Local`
   - **Host**: `localhost` (o `127.0.0.1`)
   - **Port**: `1883`
   - **Username/Password**: lascia vuoti se `allow_anonymous` è `true`

### Passo 2: Connettersi

1. Premi **Save & Connect**
2. Verifica l'indicatore "Connected" in basso a sinistra
3. L'albero dei topic apparirà sul lato sinistro (inizialmente vuoto)

## 🧪 Test e Utilizzo

### Pubblicare un messaggio di test

1. Clicca su **Publish** (icona freccia)
2. **Topic**: `test/hello`
3. **Message**: `Ciao da MQTT Explorer!`
4. Premi **Publish**

Il messaggio apparirà nell'albero dei topic a sinistra.

### Sottoscriversi a un topic

1. Seleziona il topic `test/hello` nell'albero
2. MQTT Explorer mostrerà i messaggi in tempo reale
3. Nuovi messaggi sullo stesso topic appariranno automaticamente

### Esempi di topic comuni

```
casa/temperatura/soggiorno
casa/umidita/cucina
giardino/sensori/movimento
dispositivi/stato/online
```

## 📁 Struttura del Progetto

```
guida-mqtt-docker/
├── README.md
├── LICENSE
├── docs/
│   ├── guida-completa.md
│   └── esempi/
├── config/
│   ├── mosquitto.conf
│   └── docker-compose.yml
└── scripts/
    ├── setup.sh
    └── test-connection.py
```

## 🎯 Conclusione

Seguendo questa guida hai imparato a:

- ✅ Installare e configurare Mosquitto con Docker Desktop
- ✅ Utilizzare MQTT Explorer per monitorare i messaggi
- ✅ Creare un ambiente di test MQTT isolato e sicuro
- ✅ Comprendere i concetti base del protocollo MQTT

Questa configurazione è perfetta per:
- **Apprendimento** del protocollo MQTT
- **Sviluppo** di applicazioni IoT
- **Test** di dispositivi e sensori
- **Simulazione** di scenari reali

## 🤝 Contributi

I contributi sono benvenuti! Sentiti libero di:

- Aprire issue per bug o suggerimenti
- Proporre miglioramenti alla documentazione
- Aggiungere esempi pratici
- Condividere la tua esperienza

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

---

**Autore**: Christian Schito  
**Scuola**: IISS Enrico Mattei (5°A Informatica)  
**Anno**: 2025

⭐ Se questa guida ti è stata utile, lascia una stella al repository!