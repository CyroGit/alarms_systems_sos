class AlarmaDTO:
    def __init__(self, poste, alarma, valor, origen, idposte, callid):
        self.idposte = idposte
        self.poste = poste
        self.anexo = None
        self.fullcallid = callid
        self.alarma = alarma
        self.valor = valor
        self.origen = origen