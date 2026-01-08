/****** Object:  StoredProcedure [dbo].[SP_CambiaEstadoPoste]    Script Date: 05-01-2026 10:08:45 ******/
/* Actualiza la fecha de la columna Actualizado de la tabla EstadoPostes solo cuando el estado cambia a "A" (activo). 
Con el estado en "I" (inactivo) [Actualizado] mantiene la ultima fecha de cambio a "A" (activo) */

ALTER PROCEDURE [dbo].[SP_CambiaEstadoPoste]
	-- Add the parameters for the stored procedure here
    @NumPoste varchar(50),  
	@EstadoNuevo varchar(2)
	
AS  
BEGIN  
declare @dateUpdate datetime
declare @idposte int
select top(1) @idposte = IdPoste from Postes a where a.FullCallID = @NumPoste
select @dateUpdate = [Actualizado] from EstadoPostes WHERE IdPoste = @idposte
if @EstadoNuevo= 'A' 
begin
	set @dateUpdate = getdate()
end 

UPDATE EstadoPostes
SET [EstadoActual] = @EstadoNuevo, [Actualizado]= @dateUpdate
WHERE IdPoste = @idposte

END

