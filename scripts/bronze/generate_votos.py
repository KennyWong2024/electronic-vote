import os
import uuid
import random
import pandas as pd
from sqlalchemy import text
from utils.db_connection import get_engine

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
data_dir = os.path.join(project_root, "data")

BITACORA_DIR = os.path.join(data_dir, 'bitacora')
VOTOS_DIR = os.path.join(data_dir, 'votos')
LOGS_DIR = os.path.join(data_dir, 'logs')

os.makedirs(BITACORA_DIR, exist_ok=True)
os.makedirs(VOTOS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Parámetros de simulación
PARTICIPACION = 0.73
NULOS_PRESIDENTE = 0.07
NULOS_DIPUTADO = 0.10
CHUNK_SIZE = 100_000

def generate_votos():
    engine = get_engine()

    with engine.begin() as conn:
        print("Consultando votantes...")
        votantes = conn.execute(text("""
            SELECT cedula, provincia, canton, distrito, segundo_apellido
            FROM bronze.votante
        """)).fetchall()

        total_votantes = len(votantes)
        muestra = random.sample(votantes, int(total_votantes * PARTICIPACION))
        print(f"Total votantes: {total_votantes}, muestra: {len(muestra)}")

        presidentes = conn.execute(text("""
            SELECT id_candidato, partido_id FROM bronze.candidatos
            WHERE postulacion = 'PRESIDENTE'
        """)).fetchall()

        diputados = conn.execute(text("""
            SELECT id_candidato, partido_id FROM bronze.candidatos
            WHERE postulacion = 'DIPUTADO'
        """)).fetchall()

    bitacora_rows, votos_rows, logs_rows = [], [], []

    for i, persona in enumerate(muestra, 1):
        bitacora_rows.append({
            "cedula": persona.cedula,
            "voto": True
        })

        voto_presidente_nulo = random.random() < NULOS_PRESIDENTE
        candidato_pres = random.choice(presidentes) if not voto_presidente_nulo else None

        votos_rows.append({
            "uuid_voto": str(uuid.uuid4()),
            "firma_token": str(uuid.uuid4()),
            "id_candidato": candidato_pres.id_candidato if candidato_pres else None,
            "postulacion": "PRESIDENTE",
            "segundo_apellido": persona.segundo_apellido,
            "provincia": persona.provincia,
            "canton": persona.canton,
            "distrito": persona.distrito,
            "partido_id": candidato_pres.partido_id if candidato_pres else None,
            "voto_valido": not voto_presidente_nulo
        })

        logs_rows.append({
            "tipo_evento": "Voto Registrado",
            "postulacion": "PRESIDENTE"
        })

        voto_diputado_nulo = random.random() < NULOS_DIPUTADO
        candidato_dipu = random.choice(diputados) if not voto_diputado_nulo else None

        votos_rows.append({
            "uuid_voto": str(uuid.uuid4()),
            "firma_token": str(uuid.uuid4()),
            "id_candidato": candidato_dipu.id_candidato if candidato_dipu else None,
            "postulacion": "DIPUTADO",
            "segundo_apellido": persona.segundo_apellido,
            "provincia": persona.provincia,
            "canton": persona.canton,
            "distrito": persona.distrito,
            "partido_id": candidato_dipu.partido_id if candidato_dipu else None,
            "voto_valido": not voto_diputado_nulo
        })

        logs_rows.append({
            "tipo_evento": "Voto Registrado",
            "postulacion": "DIPUTADO"
        })

        if i % CHUNK_SIZE == 0 or i == len(muestra):
            chunk_idx = i // CHUNK_SIZE if i % CHUNK_SIZE == 0 else (i // CHUNK_SIZE) + 1

            pd.DataFrame(bitacora_rows).to_csv(
                os.path.join(BITACORA_DIR, f'bitacora_{chunk_idx}.csv'), index=False
            )
            pd.DataFrame(votos_rows).to_csv(
                os.path.join(VOTOS_DIR, f'votos_{chunk_idx}.csv'), index=False
            )
            pd.DataFrame(logs_rows).to_csv(
                os.path.join(LOGS_DIR, f'logs_{chunk_idx}.csv'), index=False
            )

            print(f"Chunk {chunk_idx} generado - {i} votantes procesados")

            bitacora_rows.clear()
            votos_rows.clear()
            logs_rows.clear()

if __name__ == '__main__':
    generate_votos()
