import time
import threading
import json 
from app.database import bd
from app.mqtt.mqttcli import mqttcli # Asegúrate de que la clase se llame así
from app.dto.alarma import AlarmaDTO
from app.helper import decode
from app.serial.serialat import SerialReader

with open("config.json", "r") as file:
    config = json.load(file)

def onDataMqtt(Databuffer): # El callback debe recibir los argumentos que envía tu clase
    print(f"Llegó dato de poste: ")# {Databuffer}") 
    # Llamada corregida a la función del DTO
    try:
        data = decode.stringjson(Databuffer) 
        alarm = AlarmaDTO("sos1", "alarma test","1","MQTT_ORIGIN")
        print(alarm.poste)
    except Exception as e:
        print(f"Error en onDataMqtt: {e}")

def init_mqtt():
    my_mqtt = mqttcli(config) # Instancia de la clase
    my_mqtt.reg_ondata(onDataMqtt)
    my_mqtt.start()
    return my_mqtt

def onDataSerial(dataline):
    try:
        print("llego Serial: " + dataline)
        alarm = AlarmaDTO("sos1", "alarma test","1","MQTT_ORIGIN")
        print(alarm.poste)
    except Exception as e:
        print(f"Error en DTO: {e}")
   

def int_serial():
    my_serial = SerialReader("COM1",9200,callback=onDataSerial)
    my_serial.start()
    return my_serial
def main():
    bd.get_postes()
    mqtt_instance = init_mqtt()
    serial_instance = int_serial()

    taskMqtt = threading.Thread(target=mqtt_instance,daemon= True)
    taskSerial = threading.Thread(target=serial_instance,daemon= True)
    taskMqtt.start
    taskSerial.start
    print("Servicios iniciados. Presione Ctrl+C para salir.")
    
    try:
       while True: # Mantiene el programa vivo
            time.sleep(1)
    except KeyboardInterrupt:
         print("Cerrando aplicación...")
    

if __name__ == "__main__":
    main()