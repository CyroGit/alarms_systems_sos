
from ..database import bd
import threading
from datetime import datetime, date,timedelta
import json
# Cargar configuración desde archivo JSON
with open("config.json", "r") as file:
    config = json.load(file)
umbralTiempo =config['sistema']['intervalcontrolstatus']
intervalorconsulta = config['sistema']['intervalgetstatus']
def control_postes(intervalo, stop_event):
    while not stop_event.is_set():
        postes = bd.status_poste()
        #print (postes)
        try:
            poste_indexados = {u['Actualizado']: u for u in postes}
            #fecha_hora_inicio = datetime(2023, 10, 26, 10, 0, 0)
            #fecha_hora_fin = datetime(2023, 10, 27, 12, 30, 0)
            # 2. Definir el umbral de tiempo (hace 30 segundos)
            fecha_actual = datetime.now()
            fecha_delta= fecha_actual - timedelta(seconds=umbralTiempo)
            
            print(f"--- Revisión de postes (Umbral: {fecha_delta}) ---")
            encontrado = False
            
            for poste in postes:
                # Importante: Asegúrate que poste['Actualizado'] sea un objeto datetime. 
                # Si es string, usa datetime.strptime() para convertirlo.
                fecha_poste = poste['Actualizado']
                fecha_formateada = fecha_delta.strftime("%d/%m/%Y %H:%M:%S")
                if isinstance(fecha_poste, str):
                    fecha_poste = datetime.strptime(fecha_poste, "%d/%m/%Y %H:%M:%S")


                print(f"💡 Poste: ID {poste['IdPoste']} - Última actualización: {fecha_poste}")
                

                if fecha_poste < fecha_delta:
                    print(f"⚠️ Poste desactualizado: ID {poste['IdPoste']} - Última actualización: {fecha_poste}")
                    # Aquí puedes realizar la lógica para el usuario o departamento
                    bd.ChangeEstadoPoste((poste['IdPoste'],"I"))
                    encontrado = True
            
            if not encontrado:
                print("✅ Todos los postes están actualizados.")

        except Exception as e:
            print(f"Error: {e}")
        
        stop_event.wait(intervalo)

stop_bandera = threading.Event()
def start_timer_get_poste():
    try:
        
        hilo = threading.Thread(target=control_postes, args=(intervalorconsulta, stop_bandera))
        hilo.start()
    except KeyboardInterrupt:
            print("Cerrando aplicación...")


# Para detenerlo en cualquier momento:
def stop_timer_get_poste():
    stop_bandera.set()