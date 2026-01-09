import paho.mqtt.client as mqtt
import threading
import json
import time

# Cargar configuración desde archivo JSON
with open("config.json", "r") as file:
    config = json.load(file)

class mqttcli:
    def __init__(self,configJson ):
            self.broker = configJson["mqtt"].get("broker", "localhost")
            self.port = configJson["mqtt"].get("port", 1883) 
            self.topic = configJson["mqtt"].get("topic","test/#")
            self.running = False
            self.running_event = threading.Event()
            self.started = False
            self.thread = None

    
    def reg_ondata(self, handles):
        self.mqtt_ondata = handles 
    
    def reg_oninfo(self, handles):
        self.mqtt_oninfo=handles
    def reg_onerror(self, handles):
        self.mqtt_onerror=handles
    
        
    # Callback cuando se recibe un mensaje MQTT
    countpasada =0 
    def on_message(self,client, userdata, message):
        #global  countpasada 
        #countpasada += 1
    
        topic_parts = message.topic.split('/')
        #print (topic_parts)
        #lane = topic_parts[-1]  # Get the last part of the topic, which is the lane number
        self.mqtt_ondata(message.payload.decode('utf-8'),topic_parts)
        ## Check if the lane is numeric (representing a valid lane number)
        #if not lane.isdigit():
        #    print("\n" + "_"*80 + "\n")
        #    raw_data = message.payload.decode('utf-8')
        #    print(raw_data)
        #    print("\n" + "_"*80 + "\n")
        #    return

        # raw_data = message.payload.decode('utf-8')
        #data = raw_data.split(',')
        ##print("Received MQTT message:", raw_data)  # Print the received message
        
        #if len(data) < 6:
        #    print("Invalid data received:", data)
        #    return


    # Configurar el cliente MQTT usando datos del archivo JSON
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Conectado al broker")
            topic = self.topic
            if topic:
                client.subscribe(topic)
            else:
                print("No se encontró un tópico DAW200 para suscribirse.")
        else:
            print(f"Error de conexión: {rc}")

    
    def reconnect(self,client):
        delay = 1  # Tiempo inicial de espera
        while True:
            try:
                print(f"Intentando reconectar en {delay} segundos...")
                time.sleep(delay)
                client.reconnect()
                print("Reconexión exitosa")
                break
            except Exception as e:
                print(f"Error al reconectar: {e}")
                delay = min(delay * 2, 60)  # Incrementa el tiempo de espera hasta un máximo de 60s

    def on_disconnect(self,client, userdata, rc):
        print("Desconectado. Intentando reconectar...")
        self.reconnect(client)


    
    def conecta(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        try:
            #broker = config["mqtt"].get("broker", "localhost")  # Valor por defecto
            #port = config["mqtt"].get("port", 1883)  # Puerto estándar MQTT
            client.connect(self.broker, self.port)
            client.loop_start()
        except Exception as e:
            print(f"Error al conectar con el broker MQTT: {e}")
        #client.connect(config["mqtt"]["broker"])

        #client.loop_forever()
        while self.running:
            time.sleep(1)

    def start(self):
        """Inicia el hilo lector."""
        print("Start MQTT.")
        self.running = True
        self.thread = threading.Thread(target=self.conecta, daemon=True)
        self.thread.start()
        print("MQTT thread started.")

    def stop(self):
        """Detiene."""
        self.running = False
        if self.thread is not None:
            self.thread.join()
        print("Stop MQTT. thread stopped.")
       
