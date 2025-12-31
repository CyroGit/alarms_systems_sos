import pyodbc
import json

# Cargar configuración desde archivo JSON
with open("config.json", "r") as file:
    config = json.load(file)
# Configurar la conexión a SQL Server
conn = pyodbc.connect(
    f"DRIVER={config['sql_server']['driver']};"
    f"SERVER={config['sql_server']['server']};"
    f"DATABASE={config['sql_server']['database']};"
    f"UID={config['sql_server']['username']};"
    f"PWD={config['sql_server']['password']};"
)
cursor = conn.cursor()