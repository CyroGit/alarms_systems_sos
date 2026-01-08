import time
import threading
import json 
import queue
from cachetools import TTLCache


from app.database import bd
from app.mqtt.mqttcli import mqttcli # Asegúrate de que la clase se llame así
from app.dto.alarma import AlarmaDTO
from app.helper import decode
from app.serial.serialat import SerialReader
from app.control import statuspostes
from app.control import controlserial

with open("config.json", "r") as file:
    config = json.load(file)


# ======================= Bloque MQTT ============================================
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

# ======================= Bloque Serial ============================================
posteSMS_cache = TTLCache(maxsize=100, ttl=5)
def onDataSerial(dataline):
    try:
        print(f"Llegó Serial: {dataline}")
        data = controlserial.analizamensaje(dataline)

        # Procesar alarma
        alarma_val = data.get("alarma")
        if alarma_val is not None:
            # Recuperar poste si existe y no ha expirado
            tmpposte = posteSMS_cache.get("poste")
            if tmpposte:
                #print(tmpposte)
                alarm = AlarmaDTO(tmpposte, data['alarma'], data['valor'], "SMS")
                print(f"Procesé una alarma {alarm.poste} con alarma {alarm.alarma} valor {alarm.valor}")
            else:
                print("No hay poste válido disponible (expirado o nunca insertado)")

        # Procesar numposte
        poste_val = data.get("numposte")
        if poste_val is not None:
            # Guardar poste con TTL automático
            posteSMS_cache["poste"] = poste_val
            print(f"Poste {poste_val} agregado al cache (expira en 2s)")

    except Exception as e:
        print(f"Error en onDataSerial: {e}")


def int_serial():
    my_serial = SerialReader("COM1",9200,callback=onDataSerial)
    my_serial.start()
    return my_serial

def main():
    #bd.get_postes()
    statuspostes.stop_timer_get_poste()
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
        statuspostes.stop_timer_get_poste()
        serial_instance.stop()
        mqtt_instance.stop()
        print("Cerrando aplicación...")
    

if __name__ == "__main__":
    #texto = '"+56995999621,"","25/10/02, 12:53:49-12"'
    #valor = texto.replace('"', '').split(',')
    #print (valor)
    main()