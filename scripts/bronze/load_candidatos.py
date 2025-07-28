import logging
from sqlalchemy import text
import random
from utils.db_connection import get_engine

PARTIDOS = [
    "PUSC", "PLN", "PLP",
    "PNR", "PUP", "PPS", "PFA"
]

def main():
    engine = get_engine()

    with engine.begin() as conn:
        logging.info("Insertando partidos políticos...")
        conn.execute(text("TRUNCATE bronze.partido_politico RESTART IDENTITY CASCADE"))
        for nombre in PARTIDOS:
            conn.execute(
                text("INSERT INTO bronze.partido_politico (nombre_partido) VALUES (:nombre)"),
                {"nombre": nombre}
            )
        logging.info("Partidos insertados correctamente.")

        partidos = conn.execute(
            text("SELECT partido_id FROM bronze.partido_politico")
        ).fetchall()

        logging.info("Seleccionando candidatos a presidente...")
        presidentes = conn.execute(text("""
            SELECT cedula, nombre, primer_apellido, segundo_apellido, provincia, canton, distrito
            FROM bronze.votante
            WHERE cedula IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 7
        """)).fetchall()

        logging.info("Seleccionando candidatos a diputado...")
        diputados = conn.execute(text("""
            SELECT cedula, nombre, primer_apellido, segundo_apellido, provincia, canton, distrito
            FROM bronze.votante
            WHERE cedula IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 60
        """)).fetchall()

        if len(presidentes) < 7 or len(diputados) < 60:
            logging.error("No hay suficientes votantes en la base de datos.")
            return

        conn.execute(text("TRUNCATE bronze.candidatos RESTART IDENTITY"))

        for row in presidentes:
            partido_id = random.choice(partidos).partido_id
            conn.execute(text("""
                INSERT INTO bronze.candidatos (
                    cedula, nombre, primer_apellido, segundo_apellido,
                    provincia, canton, distrito, partido_id, postulacion
                ) VALUES (
                    :cedula, :nombre, :primer_apellido, :segundo_apellido,
                    :provincia, :canton, :distrito, :partido_id, 'PRESIDENTE'
                )
            """), {
                "cedula": row.cedula,
                "nombre": row.nombre,
                "primer_apellido": row.primer_apellido,
                "segundo_apellido": row.segundo_apellido,
                "provincia": row.provincia,
                "canton": row.canton,
                "distrito": row.distrito,
                "partido_id": partido_id
            })

        for row in diputados:
            partido_id = random.choice(partidos).partido_id
            conn.execute(text("""
                INSERT INTO bronze.candidatos (
                    cedula, nombre, primer_apellido, segundo_apellido,
                    provincia, canton, distrito, partido_id, postulacion
                ) VALUES (
                    :cedula, :nombre, :primer_apellido, :segundo_apellido,
                    :provincia, :canton, :distrito, :partido_id, 'DIPUTADO'
                )
            """), {
                "cedula": row.cedula,
                "nombre": row.nombre,
                "primer_apellido": row.primer_apellido,
                "segundo_apellido": row.segundo_apellido,
                "provincia": row.provincia,
                "canton": row.canton,
                "distrito": row.distrito,
                "partido_id": partido_id
            })

        logging.info("Candidatos cargados exitosamente desde padrón electoral.")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    main()