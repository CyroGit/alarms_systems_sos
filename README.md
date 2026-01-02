# Sistema Alarma PATsos MQTT y SMS

> Proyecto alarmas PATsos MQTT y SMS serial Command AT

## Built
 - Python
 - SQL 
### Requisitos
 - pyodbc

### Config File 
> config.json
```json
{
    "sql_server": {
        "driver": "SQL SERVER",
        "server": "localhost,1433",
        "database": "ECB",
        "username": "xxxx",
        "password": "xxxx"
    },
    "mqtt": {
        "broker": "localhost",
        "port": 1883,
        "topic": "test",
        "user":"test",
        "pass":"test"
    },
    "serial":{
        "com":"COM1",
        "baudrate":9200
    },
    "sistema":{
        "intervalgetstatus": 30,
        "intervalcontrolstatus":86400
    }

}
```
> - sistema.intervalgetstatus : intervalo de tiempo en segundos para obtener el status del poste.
> - sistema.intervalcontrolstatus: intervalo de tiempo en segundos para determinar cambio de estado del poste (86400 -> 24 hrs).