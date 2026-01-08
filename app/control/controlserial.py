import json
from ..database import bd
def analizamensaje(data):
    datoarray = str(data).split(':')
    #print (f"hago algo {str(datoarray[0])}")
    match str(datoarray[0]):
        case "+CMT": # Es un sms entrante, se rescata numero de poste
            #Se debe separar la data por coma ","
            valor=str(datoarray[1]).replace('"', '').split(',')
            #print(valor)
            horatmp = str(valor[0]).split('-')
            serial_data={"numposte":valor[0],"fechasms":valor[2],"horasms":str(horatmp[0]).replace(" ","")}
            #print (serial_data)
            return serial_data
        case "OK":
            return "OK"
        case _:
            #print ("hola")
            return msgfromsos(data)



    #print (datoarray)


def msgfromsos(data):
    #ATENCION : “ALARMA”= “VALOR” ! ---> esta serial la estructura de la alarma PATsos, sin las dobles comillas 
    tmpdata = str(data).split(':')
    #print (tmpdata)
    match tmpdata[0].replace(" ",""):
        case "ATENCION":

            tmpalarma = str(tmpdata[1]).split(',')
            #print (tmpalarma)
            tmpalarma = str(tmpalarma[1]).split('=')
            alarmasms={"alarma":tmpalarma[0],"valor":tmpalarma[1].replace("!","")}
            print (alarmasms)
            return alarmasms
        case _:
            return "ok"

