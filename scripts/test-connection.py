#!/usr/bin/env python3
"""
Script di test per connessione MQTT
Testa la connessione al broker Mosquitto e pubblica messaggi di esempio
"""

import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# Configurazione broker
BROKER_HOST = "localhost"
BROKER_PORT = 1883
KEEP_ALIVE = 60

# Topics di test
TEST_TOPICS = {
    "temperatura": "casa/temperatura/soggiorno",
    "umidita": "casa/umidita/soggiorno", 
    "movimento": "casa/sensori/movimento",
    "stato": "dispositivi/stato/online"
}

def on_connect(client, userdata, flags, rc):
    """Callback chiamata quando il client si connette al broker"""
    if rc == 0:
        print("✅ Connesso al broker MQTT!")
        print(f"📡 Broker: {BROKER_HOST}:{BROKER_PORT}")
        
        # Sottoscrizione ai topic di test
        for nome, topic in TEST_TOPICS.items():
            client.subscribe(topic)
            print(f"🔔 Sottoscritto al topic: {topic}")
    else:
        print(f"❌ Connessione fallita con codice: {rc}")

def on_message(client, userdata, msg):
    """Callback chiamata quando arriva un messaggio"""
    try:
        payload = msg.payload.decode('utf-8')
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"📨 [{timestamp}] {msg.topic}: {payload}")
    except Exception as e:
        print(f"❌ Errore nel processare il messaggio: {e}")

def on_disconnect(client, userdata, rc):
    """Callback chiamata quando il client si disconnette"""
    print("🔌 Disconnesso dal broker MQTT")

def genera_dati_sensore():
    """Genera dati casuali per simulare sensori"""
    return {
        "temperatura": round(random.uniform(18.0, 28.0), 1),
        "umidita": random.randint(40, 80),
        "movimento": random.choice([True, False]),
        "timestamp": datetime.now().isoformat()
    }

def main():
    """Funzione principale"""
    print("🚀 Avvio test connessione MQTT...")
    
    # Creazione client MQTT
    client = mqtt.Client(client_id="test_client_python")
    
    # Impostazione callback
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    try:
        # Connessione al broker
        print(f"🔗 Tentativo di connessione a {BROKER_HOST}:{BROKER_PORT}...")
        client.connect(BROKER_HOST, BROKER_PORT, KEEP_ALIVE)
        
        # Avvio loop non bloccante
        client.loop_start()
        
        # Test pubblicazione messaggi
        print("\n📤 Inizio pubblicazione messaggi di test...")
        
        for i in range(10):
            dati = genera_dati_sensore()
            
            # Pubblica temperatura
            client.publish(TEST_TOPICS["temperatura"], 
                         json.dumps({"valore": dati["temperatura"], "unita": "°C"}))
            
            # Pubblica umidità
            client.publish(TEST_TOPICS["umidita"], 
                         json.dumps({"valore": dati["umidita"], "unita": "%"}))
            
            # Pubblica stato movimento
            client.publish(TEST_TOPICS["movimento"], 
                         json.dumps({"movimento_rilevato": dati["movimento"]}))
            
            # Pubblica stato dispositivo
            client.publish(TEST_TOPICS["stato"], 
                         json.dumps({"online": True, "timestamp": dati["timestamp"]}))
            
            print(f"📊 Messaggio {i+1}/10 pubblicato")
            time.sleep(2)
        
        print("\n✅ Test completato! Premi CTRL+C per uscire...")
        
        # Mantieni il client attivo per ricevere messaggi
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Interruzione da utente")
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 Test terminato")

if __name__ == "__main__":
    # Verifica dipendenze
    try:
        import paho.mqtt.client as mqtt
        main()
    except ImportError:
        print("❌ Modulo paho-mqtt non trovato!")
        print("📦 Installa con: pip install paho-mqtt")