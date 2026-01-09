
ALTER procedure [dbo].[insertarAlertAlarmSOS]
@poste  varchar(150),
@topico varchar(150),
@idAlarma int,

@fecha datetime

as
declare @alarma varchar(150)
select  @alarma=alarma
  FROM [dbo].[AlarmaSOS]
  where ID_Alarma = @idAlarma

declare @idPoste int
select @idPoste=IdPoste
  FROM [dbo].[Postes]
  where IdPoste = @poste or fullcallid = @poste or AnexoPoste = @poste or NumeroPoste = @poste
Begin
	  INSERT INTO dbo.AlertaAlarmaSOS
				(Poste
				,Topico
				,ID_Alarma
				,AlarmaSOS
				,Fecha,
				idPoste)
		VALUES
				(@poste
				,@topico
				,@idAlarma
				,@alarma
				,@fecha
				,@idPoste)
end