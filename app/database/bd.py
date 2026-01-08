import pyodbc
import json

# Cargar configuración desde archivo JSON
with open("config.json", "r") as file:
    config = json.load(file)

strCon = (f"DRIVER={config['sql_server']['driver']};"
                                    f"SERVER={config['sql_server']['server']};" 
                                    f"DATABASE={config['sql_server']['database']};" 
                                    f"UID={config['sql_server']['username']};"
                                    f"PWD={config['sql_server']['password']};")
# Función para ejecutar el procedimiento almacenado
def ChangeEstadoPoste(dato):
    try:
        conn = pyodbc.connect(strCon)
        cursor = conn.cursor()
        #params = (dato['axls11'], dato['origenfile'])
        sql = "EXEC dbo.SP_CambiaEstadoPoste ?, ?"
        print (dato)
        cursor.execute(sql, dato)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_postes():
    try:
        conn = pyodbc.connect(strCon)
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
        conn = pyodbc.connect(strCon)
        


        cursor = conn.cursor()
    
        cursor.execute("EXEC SP_GetEstadoPostes")
        
        # Obtener nombres de columnas y convertir a lista de diccionarios
        # cursor.description contiene los metadatos de las columnas
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        #poste_indexados = {u['IdPoste']: u for u in rows}
        #print (rows)
        return rows

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()