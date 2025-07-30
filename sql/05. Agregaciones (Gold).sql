/*
    Nota, estos cálculos es con el fin de realizar agregaciones al Gold Layer, sin embargo con visualizadores como Looker seria mas optimo realizar
    estos cálculos con métricas evaluando las dimenciones y tablas calculadas para definir porcentajes
*/

-- Aquí respondemos preguntas como tasa de abtencionismo
-- Todas rondan el 73 por la ingesta que hicimos preprogramada, si cambian en porcentaje en generate votos esto cambiará
-- Hay nulos de las fuentes de datos

CREATE TABLE gold.tasa_votacion AS
SELECT
	provincia,
    canton,
    distrito,
    voto_emitido,
    COUNT(*) OVER (PARTITION BY provincia) AS total_votantes_provincia,
    COUNT(*) OVER (PARTITION BY canton) AS total_votantes_canton,
    COUNT(*) OVER (PARTITION BY distrito) AS total_votantes_distrito,
    COUNT(*) FILTER (WHERE voto_emitido) OVER () AS total_votos_emitidos,
    ROUND(
        (COUNT(*) FILTER (WHERE voto_emitido) OVER (PARTITION BY provincia) * 100.0 / COUNT(*) OVER (PARTITION BY provincia)), 2
    ) AS porcentaje_participacion_provincia,
    ROUND(
        (COUNT(*) FILTER (WHERE voto_emitido) OVER (PARTITION BY canton) * 100.0 / COUNT(*) OVER (PARTITION BY canton)), 2
    ) AS porcentaje_participacion_canton,
    ROUND(
        (COUNT(*) FILTER (WHERE voto_emitido) OVER (PARTITION BY distrito) * 100.0 / COUNT(*) OVER (PARTITION BY distrito)), 2
    ) AS porcentaje_participacion_distrito
FROM silver.tasa_votacion;

-- Aquí respondemos preguntas de ganador
-- Trtabajemos una una CTE porque tenemos el doble de votos que votantes, ya que teniamos la papeleta para el presidente y la otra para diputados

CREATE TABLE gold.resultado_elecciones AS
WITH base AS (
  SELECT
    postulacion,
    CASE
      WHEN postulacion = 'PRESIDENTE'
      THEN COALESCE(nombre_candidato, 'VOTO NULO')
      ELSE NULL
    END AS nombre_candidato,
    CASE
      WHEN postulacion = 'PRESIDENTE'
      THEN COALESCE(primer_apellido_candidato, '')
      ELSE NULL
    END AS primer_apellido_candidato,
    CASE
      WHEN postulacion = 'PRESIDENTE'
      THEN COALESCE(segundo_apellido_candidato, '')
      ELSE NULL
    END AS segundo_apellido_candidato,
    CASE
      WHEN postulacion = 'PRESIDENTE'
      THEN CONCAT(
             COALESCE(nombre_candidato, 'VOTO NULO'),
             ' ',
             COALESCE(primer_apellido_candidato, ''),
             ' ',
             COALESCE(segundo_apellido_candidato, '')
           )
      ELSE NULL
    END AS nombre_completo,
    CASE
      WHEN postulacion = 'DIPUTADO'
      THEN COALESCE(nombre_partido, 'VOTO NULO')
      ELSE NULL
    END AS nombre_partido,
    voto_provincia,
    voto_canton,
    voto_distrito
  FROM silver.elecciones
)
SELECT
  postulacion,
  nombre_candidato,
  primer_apellido_candidato,
  segundo_apellido_candidato,
  nombre_completo,
  nombre_partido,
  voto_provincia,
  voto_canton,
  voto_distrito,
  COUNT(*) AS total_votos_recibidos,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY postulacion, voto_provincia) * 100, 2) AS porcentaje_votos_provincia,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY postulacion, voto_canton) * 100, 2) AS porcentaje_votos_canton,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY postulacion, voto_distrito) * 100, 2) AS porcentaje_votos_distrito,
  RANK() OVER (PARTITION BY postulacion ORDER BY COUNT(*) DESC) AS posicion_candidato
FROM base
GROUP BY
  postulacion,
  nombre_candidato,
  primer_apellido_candidato,
  segundo_apellido_candidato,
  nombre_completo,
  nombre_partido,
  voto_provincia,
  voto_canton,
  voto_distrito;

