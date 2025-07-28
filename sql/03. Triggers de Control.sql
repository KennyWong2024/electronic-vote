-- Verificador de votos nulos

CREATE OR REPLACE FUNCTION validar_voto_valido()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.postulacion = 'PRESIDENTE' AND NEW.id_candidato IS NULL THEN
        NEW.voto_valido := FALSE;
    ELSIF NEW.postulacion = 'DIPUTADO' AND NEW.partido_id IS NULL THEN
        NEW.voto_valido := FALSE;
    ELSE
        NEW.voto_valido := TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_voto_valido
BEFORE INSERT ON bronze.votos
FOR EACH ROW EXECUTE FUNCTION validar_voto_valido();
