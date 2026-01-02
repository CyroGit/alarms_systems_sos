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


# Función para ejecutar el procedimiento almacenado
def insertar_con_sp(dato):
    cursor = conn.cursor()
    params = (
        dato['vehicle_count'], dato['idequipo'], dato['timestamp'],
        dato['boardtemp'], dato['lane'], dato['class'], dato['speed_kph'], dato['gvw_kg'],
        dato['total_length_cm'], dato['axle_count'],
        dato['axlw1'], dato['axls1'],
        dato['axlw2'], dato['axls2'],
        dato['axlw3'], dato['axls3'],
        dato['axlw4'], dato['axls4'],
        dato['axlw5'], dato['axls5'],
        dato['axlw6'], dato['axls6'],
        dato['axlw7'], dato['axls7'],
        dato['axlw8'], dato['axls8'],
        dato['axlw9'], dato['axls9'],
        dato['axlw10'], dato['axls10'],
        dato['axlw11'], dato['axls11'],
        dato['origenfile']
    )
    sql = "EXEC SP_AddPesajeDAW200 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()
def get_postes():
    try:
        cursor = conn.cursor()
        sql ="EXEC dbo.SP_GetInfoPostes"
        cursor.execute(sql)
        rows = cursor.fetchall()
        #for row in rows:
            #print(row)
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def status_poste():
    try:
        conn = pyodbc.connect(f"DRIVER={config['sql_server']['driver']};"
        f"SERVER={config['sql_server']['server']};"
        f"DATABASE={config['sql_server']['database']};"
        f"UID={config['sql_server']['username']};"
        f"PWD={config['sql_server']['password']};")
        cursor = conn.cursor()
        
        # 2. Ejecutar la consulta
        cursor.execute("EXEC SP_GetEstadoPostes")
        
        # 3. Obtener nombres de columnas y convertir a lista de diccionarios
        # cursor.description contiene los metadatos de las columnas
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # 4. Crear un ÍNDICE en memoria para búsquedas rápidas por ID
        # Esto transforma la lista en: { 101: {'nombre': 'Ana', ...}, 102: {...} }
        usuarios_indexados = {u['IdPoste']: u for u in rows}
        print (rows)
        # --- EJEMPLO DE BÚSQUEDA ---
        #id_a_buscar = 101
        
        #if id_a_buscar in usuarios_indexados:
        #    usuario = usuarios_indexados[id_a_buscar]
        #    print(f"✅ Usuario encontrado: {usuario['nombre']} ({usuario['departamento']})")
        #else:
        #    print("❌ El ID no existe en los registros descargados.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()