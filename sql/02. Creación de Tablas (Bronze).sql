-- Padrón electoral de Costa Rica 2025
CREATE TABLE bronze.votante (
    cedula INTEGER PRIMARY KEY,
    codigo_electoral VARCHAR(20),
    fecha_caducidad DATE,
    junta VARCHAR(10),
    nombre VARCHAR(50),
    primer_apellido VARCHAR(50),
    segundo_apellido VARCHAR(50),
    provincia VARCHAR(50),
    canton VARCHAR(50),
    distrito VARCHAR(64),
    datos_biometricos TEXT,
    fotografia TEXT,
    firma_digital TEXT
);

-- Poblados de Costa Rica
CREATE TABLE bronze.distrito_electoral (
    id INTEGER PRIMARY KEY,
    codigo_postal INTEGER,
    provincia VARCHAR(50),
    canton VARCHAR(50),
    distrito VARCHAR(64),
    x VARCHAR(50),
    y VARCHAR(50)
);

-- Partidos Politicos
CREATE TABLE bronze.partido_politico (
    partido_id SERIAL PRIMARY KEY,
    nombre_partido VARCHAR(50) NOT NULL
);

-- Candidatos
CREATE TABLE bronze.candidatos (
    id_candidato SERIAL PRIMARY KEY,
    cedula INTEGER NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    provincia VARCHAR(50),
    canton VARCHAR(50),
    distrito VARCHAR(64),
    partido_id INTEGER REFERENCES bronze.partido_politico(partido_id),
    postulacion VARCHAR(50)
);

-- Bitácora de Votación
CREATE TABLE bronze.bitacora_votacion (
    id SERIAL PRIMARY KEY,
    cedula INTEGER NOT NULL UNIQUE,
    voto BOOLEAN NOT NULL
);

-- Logs
CREATE TABLE bronze.logs (
    id SERIAL PRIMARY KEY,
    tipo_evento VARCHAR(50) NOT NULL,
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    postulacion VARCHAR(50) NOT NULL
);

-- Votos
CREATE TABLE bronze.votos (
    uuid_voto VARCHAR(100) PRIMARY KEY,
    firma_token VARCHAR(200) NOT NULL,
    id_candidato INTEGER REFERENCES bronze.candidatos(id_candidato),
    postulacion VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    provincia VARCHAR(50),
    canton VARCHAR(50),
    distrito VARCHAR(64),
    partido_id INTEGER REFERENCES bronze.partido_politico(partido_id),
    voto_valido BOOLEAN
);