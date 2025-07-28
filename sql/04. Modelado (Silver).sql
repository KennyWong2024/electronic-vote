-- Verificador de abtencionismo pro provincia, cantón y distrito
CREATE OR REPLACE VIEW silver.tasa_votacion AS
WITH total_padron AS (
    SELECT 
        cedula,
        codigo_electoral,
        fecha_caducidad,
        junta,
        nombre,
        primer_apellido,
        segundo_apellido,
        provincia,
        canton,
        distrito,
        datos_biometricos,
        fotografia,
        firma_digital
    FROM bronze.votante
),
votantes AS (
    SELECT
        id,
        cedula,
        voto
    FROM bronze.bitacora_votacion
)
SELECT 
    A.provincia,
    A.canton,
    A.distrito,
    B.voto AS voto_emitido
FROM total_padron AS A
LEFT JOIN votantes AS B
  ON A.cedula = B.cedula


-- Votaciones
CREATE OR REPLACE VIEW silver.elecciones AS
WITH votos AS (
    SELECT
        id_candidato,
        postulacion,
        provincia,
        canton,
        distrito,
        partido_id
    FROM bronze.votos
),
partidos AS (
    SELECT
        partido_id,
        nombre_partido
    FROM bronze.partido_politico
),
candidatos AS (
    SELECT
        id_candidato,
        nombre,
        primer_apellido,
        segundo_apellido
    FROM bronze.candidatos
)
SELECT
    C.nombre AS nombre_candidato,
    C.primer_apellido AS primer_apellido_candidato,
    C.segundo_apellido AS segundo_apellido_candidato,
    A.postulacion,
    A.provincia AS voto_provincia,
    A.canton AS voto_canton,
    A.distrito AS voto_distrito,
    B.nombre_partido
FROM votos AS A
LEFT JOIN partidos AS B
  ON A.partido_id = B.partido_id
LEFT JOIN candidatos AS C
  ON A.id_candidato = C.id_candidato