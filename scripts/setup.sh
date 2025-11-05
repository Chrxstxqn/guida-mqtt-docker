#!/bin/bash

# Script di setup per MQTT con Docker
# ===================================

echo "🚀 Setup MQTT con Docker e Mosquitto"
echo "===================================="

# Verifica se Docker è installato
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non trovato! Installa Docker Desktop prima di continuare."
    exit 1
fi

echo "✅ Docker trovato"

# Verifica se Docker è in esecuzione
if ! docker info &> /dev/null; then
    echo "❌ Docker non è in esecuzione! Avvia Docker Desktop."
    exit 1
fi

echo "✅ Docker è in esecuzione"

# Crea le directory necessarie
echo "📁 Creazione directory..."
mkdir -p config data log

# Copia il file di configurazione se non esiste
if [ ! -f "config/mosquitto.conf" ]; then
    echo "📄 File mosquitto.conf non trovato nella directory config/"
    echo "📥 Scarica il file di configurazione dal repository GitHub"
    exit 1
fi

echo "✅ File di configurazione trovato"

# Pull dell'immagine Mosquitto
echo "📦 Download immagine Mosquitto..."
docker pull eclipse-mosquitto:latest

# Avvio del container con Docker Compose
if [ -f "config/docker-compose.yml" ]; then
    echo "🐳 Avvio container con Docker Compose..."
    cd config && docker-compose up -d
    echo "✅ Container avviato!"
    echo "📊 Verifica lo stato con: docker-compose ps"
else
    # Avvio manuale del container
    echo "🐳 Avvio container manuale..."
    docker run -d \\
        --name mosquitto \\
        -p 1883:1883 \\
        -p 9001:9001 \\
        -v $(pwd)/config:/mosquitto/config \\
        -v $(pwd)/data:/mosquitto/data \\
        -v $(pwd)/log:/mosquitto/log \\
        eclipse-mosquitto:latest
    
    echo "✅ Container avviato manualmente!"
fi

# Verifica che il container sia in esecuzione
sleep 5
if docker ps | grep -q mosquitto; then
    echo "🎉 Setup completato con successo!"
    echo ""
    echo "📋 Informazioni connessione:"
    echo "   Host: localhost"
    echo "   Porta MQTT: 1883"
    echo "   Porta WebSocket: 9001"
    echo ""
    echo "🔧 Comandi utili:"
    echo "   Visualizza logs: docker logs mosquitto"
    echo "   Ferma container: docker stop mosquitto"
    echo "   Riavvia container: docker start mosquitto"
    echo ""
    echo "📖 Consulta il README.md per maggiori informazioni"
else
    echo "❌ Errore nell'avvio del container"
    echo "🔍 Controlla i logs con: docker logs mosquitto"
fi