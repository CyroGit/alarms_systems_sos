
from ..database import bd
import threading
import datetime

def control_postes(intervalo, stop_event):
    while not stop_event.is_set():
        bd.status_poste()
        # wait() funciona como sleep pero se interrumpe si el evento se activa
        stop_event.wait(intervalo)
try:
    stop_bandera = threading.Event()
    hilo = threading.Thread(target=control_postes, args=(5, stop_bandera))
    hilo.start()
except KeyboardInterrupt:
         print("Cerrando aplicación...")


# Para detenerlo en cualquier momento:
def stop_timer_get_poste():
    stop_bandera.set()