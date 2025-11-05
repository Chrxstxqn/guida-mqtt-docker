# Guida Completa all'uso di MQTT con Docker e MQTT Explorer

## Introduzione

Questa guida dettagliata ti accompagna nell'installazione e nell'utilizzo del broker **Mosquitto** tramite **Docker** e nella configurazione di **MQTT Explorer** per testare e osservare i messaggi MQTT.

L'obiettivo è comprendere il funzionamento del protocollo MQTT, la logica dei topic e la trasmissione dei messaggi, in un contesto di apprendimento o sviluppo.

## Cos'è MQTT?

**MQTT** (Message Queuing Telemetry Transport) è un protocollo di comunicazione leggero basato sul modello **publish/subscribe**. È stato progettato per essere semplice ed efficiente, anche in reti con poca banda o connessioni instabili, motivo per cui è molto usato nell'**Internet of Things (IoT)**.

### Architettura MQTT

Nella sua architettura ci sono tre elementi principali:

- **Client**: dispositivi o app che inviano o ricevono messaggi
- **Broker**: il server centrale (ad esempio Mosquitto) che smista i messaggi  
- **Topic**: i "canali" logici in cui si pubblicano i dati (es. `casa/temperatura/soggiorno`)

Un sensore di temperatura può, ad esempio, pubblicare il suo valore su un topic e il broker lo consegnerà a tutti i client che si sono iscritti a quel topic.

### Vantaggi di MQTT

I vantaggi principali di MQTT sono:

- **Leggerezza**: protocollo minimale e efficiente
- **Affidabilità**: diversi livelli di qualità del servizio (QoS)
- **Persistenza**: possibilità di messaggi persistenti
- **Scalabilità**: facile scalabilità in reti con molti dispositivi

```
Client (Publisher) → BROKER → Client (Subscriber)
                    MQTT
```

## Perché usare Docker Desktop

Installare Mosquitto manualmente può richiedere configurazioni avanzate. Con Docker, invece, il broker è pronto all'uso in pochi secondi. I vantaggi principali:

- **Velocità**: il container Mosquitto è subito funzionante
- **Isolamento**: gira separato dal tuo sistema
- **Portabilità**: stesso container su diversi computer
- **Gestione semplice**: avvio/stop via interfaccia grafica Docker Desktop

Docker fornisce quindi l'ambiente ideale per eseguire Mosquitto senza complicazioni.

## Requisiti

### Installazione di Docker Desktop

**Requisiti di sistema:**
- Windows 10/11 con WSL2 attivo, oppure macOS
- Almeno 4 GB di RAM
- Accesso come amministratore

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

## Configurare Mosquitto con Docker Desktop

### Passo 1 - Aprire Docker Desktop

Avvia Docker Desktop e vai alla sezione **Containers** dal menù laterale.

### Passo 2 - Creare un nuovo container Mosquitto

1. Vai su **Images**
2. Nel campo di ricerca inserisci `eclipse-mosquitto` e sul primo risultato premi **Pull**
3. Docker scaricherà l'immagine ufficiale di Mosquitto dal Docker Hub
4. Una volta scaricata, torna sulla sezione **Images**: vedrai l'immagine `eclipse-mosquitto`
5. Clicca su **Run** per avviare la creazione del container

### Passo 3 - Configurare il container Mosquitto

Nella schermata di configurazione scegli:

- **Container name**: ad esempio `mosquitto`
- **Ports**: aggiungi il mapping:
  - `1883 → 1883` (porta MQTT standard)
  - `9001 → 9001` (opzionale per WebSocket)
- **Volumes** (consigliato per configurazioni e log persistenti):
  - Collega una cartella del tuo computer a quella del container:
    - `config → /mosquitto/config`
    - `data → /mosquitto/data`
    - `log → /mosquitto/log`

Se non hai ancora creato queste cartelle sul PC, ti conviene prima predisporle in una directory (es: `C:/mosquitto/` su Windows o `~/mosquitto/` su macOS).

### Passo 4 - Creare un file di configurazione personalizzato

Dentro alla cartella `config` sul tuo PC, crea un file chiamato `mosquitto.conf` con contenuto base:

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

Grazie al volume configurato in precedenza, Mosquitto userà automaticamente questo file.

### Passo 5 - Avviare e verificare il container

- Torna su **Containers** → troverai il tuo `mosquitto`
- Premi **Start** per avviarlo
- Puoi aprire i logs dalla GUI per verificare che il broker stia funzionando correttamente (dovresti vedere che ascolta sulla porta 1883)

## Perché usare MQTT Explorer

Ora che Mosquitto è disponibile tramite Docker, occorre uno strumento per interagire con il broker:

**MQTT Explorer** è un'app grafica che permette di:

- Collegarsi al broker
- Visualizzare i messaggi in tempo reale
- Pubblicare test su diversi topic
- Sottoscriversi ai topic e osservarne i dati
- Organizzare la struttura dei topic in una vista ad albero

In pratica, è il "microscopio" con cui osservare e capire il flusso MQTT.

## Installazione di MQTT Explorer

### Download

- Visita [mqtt-explorer.com](https://mqtt-explorer.com/)
- Scarica la versione per Windows, macOS o Linux

### Installazione su Windows

- Avvia il file `.exe`
- Segui i passaggi guidati
- Al termine, troverai MQTT Explorer nel menu Start

### Installazione su macOS

- Apri il file `.dmg`
- Trascina l'app in "Applicazioni"
- Avviala come un normale programma

A questo punto hai pronto:

1. **Docker Desktop** con Mosquitto (il broker MQTT)
2. **MQTT Explorer** per testare e osservare i messaggi

Il passo successivo sarà configurare la connessione in MQTT Explorer.

## Configurare MQTT Explorer

Dopo aver installato MQTT Explorer, è il momento di configurarlo per connettersi al broker Mosquitto che hai avviato con Docker Desktop. Questa fase ti permetterà di visualizzare in tempo reale i messaggi MQTT, creare topic e pubblicare dati di test.

### Passo 1 - Avviare MQTT Explorer

Apri MQTT Explorer dal menu Start (Windows) o dalla cartella Applicazioni (macOS).
All'avvio compare la schermata principale con la lista delle connessioni salvate (inizialmente vuota).

### Passo 2 - Creare una nuova connessione

1. Clicca su "**Add new connection**"
2. Inserisci i seguenti parametri di base:
   - **Name**: `Mosquitto Local` (puoi scegliere qualsiasi nome)
   - **Host**: `localhost` oppure `127.0.0.1`
   - **Port**: `1883`

Questi valori indicano che MQTT Explorer si collecherà al broker Mosquitto attivo sul tuo computer tramite Docker.

3. Lascia vuoti i campi **Username** e **Password** se hai configurato Mosquitto con `allow_anonymous true` (come da guida precedente)
4. Lascia disabilitata la voce **TLS**, poiché la connessione è solo locale

### Passo 3 - Salvare e connettersi

- Premi **Save & Connect**
- Dopo qualche secondo, in basso a sinistra vedrai l'indicatore "**Connected**"
- Sul lato sinistro apparirà l'albero dei topic; inizialmente sarà vuoto poiché non è stato pubblicato ancora alcun messaggio

### Passo 4 - Pubblicare un messaggio di test

1. Clicca su **Publish** (icona a forma di freccia in alto)
2. Nel campo **Topic**, inserisci qualcosa come:
   ```
   test/hello
   ```
3. Nel campo **Message**, scrivi ad esempio:
   ```
   Ciao da MQTT Explorer!
   ```
4. Premi **Publish**

Il messaggio verrà inviato al broker Mosquitto e subito comparirà nella struttura dei topic a sinistra, con il valore appena pubblicato.

### Passo 5 - Sottoscriversi a un topic

1. Seleziona il topic `test/hello` nell'albero
2. MQTT Explorer mostrerà i messaggi ricevuti in tempo reale
3. Se pubblichi nuovi messaggi sullo stesso topic, li vedrai comparire immediatamente nella parte destra dello schermo

### Passo 6 - (Opzionale) Aggiungere più connessioni

Se vuoi testare altri broker o dispositivi, clicca su "**Connections → Add new**" e ripeti la configurazione con l'IP e la porta del nuovo server MQTT.

A questo punto hai completato la configurazione di MQTT Explorer e puoi:

- Osservare i topic in tempo reale
- Pubblicare messaggi di prova
- Monitorare il corretto funzionamento del broker Mosquitto in Docker

## Esempi Pratici

### Topic comuni per IoT

```
casa/temperatura/soggiorno
casa/umidita/cucina
giardino/sensori/movimento
dispositivi/stato/online
domotica/luci/salotto
energie/consumo/totale
```

### Messaggi JSON tipici

**Sensore temperatura:**
```json
{
  "valore": 23.5,
  "unita": "°C",
  "timestamp": "2025-11-05T10:30:00Z"
}
```

**Sensore movimento:**
```json
{
  "movimento_rilevato": true,
  "sensibilita": "alta",
  "zona": "ingresso"
}
```

**Stato dispositivo:**
```json
{
  "online": true,
  "ultima_connessione": "2025-11-05T10:25:00Z",
  "batteria": 85
}
```

## Conclusione

Seguendo questa guida hai imparato come installare Mosquitto utilizzando Docker Desktop, configurare il broker per il tuo ambiente e utilizzare MQTT Explorer per connetterti, visualizzare e pubblicare messaggi in pochi passi, il tutto senza dover modificare il sistema operativo o effettuare configurazioni complesse.

Questa soluzione ti permette di sperimentare in sicurezza il protocollo MQTT, creare test, osservare i flussi dati tra client e broker e acquisire dimestichezza con i concetti chiave dell'IoT e della comunicazione "pubblica/sottoscrivi". Tutto ciò può essere facilmente replicato e adattato sia per scopi didattici che di sviluppo professionale.

Adesso sei in grado di:

- Avviare e gestire un broker MQTT isolato tramite Docker
- Utilizzare MQTT Explorer per analizzare e testare i topic e i messaggi
- Creare ambienti di simulazione per dispositivi reali o virtuali

Ti basta ripetere questi passaggi su qualsiasi computer dotato di Docker per essere subito operativo su nuovi progetti MQTT. Buona sperimentazione!

---

**Autore**: Christian Schito  
**Scuola**: IISS Enrico Mattei (5°A Informatica)  
**Anno**: 2025