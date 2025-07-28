import os
import logging
from utils.db_connection import get_engine
from utils.data_loader import cargar_csvs_en_lote

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    engine = get_engine()

    logging.info("Cargando votos desde CSV a la base de datos...")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(project_root, 'data')

    bitacora_dir = os.path.join(data_dir, 'bitacora')
    votos_dir = os.path.join(data_dir, 'votos')
    logs_dir = os.path.join(data_dir, 'logs')

    cargar_csvs_en_lote(
        carpeta=bitacora_dir,
        engine=engine,
        tabla="bitacora_votacion",
        schema="bronze",
        mapping_columnas={"cedula": "cedula", "voto": "voto"}
    )

    cargar_csvs_en_lote(
        carpeta=votos_dir,
        engine=engine,
        tabla="votos",
        schema="bronze",
        mapping_columnas={
            "uuid_voto": "uuid_voto",
            "firma_token": "firma_token",
            "id_candidato": "id_candidato",
            "postulacion": "postulacion",
            "segundo_apellido": "segundo_apellido",
            "provincia": "provincia",
            "canton": "canton",
            "distrito": "distrito",
            "partido_id": "partido_id",
            "voto_valido": "voto_valido"
        }
    )

    cargar_csvs_en_lote(
        carpeta=logs_dir,
        engine=engine,
        tabla="logs",
        schema="bronze",
        mapping_columnas={"tipo_evento": "tipo_evento", "postulacion": "postulacion"}
    )

    logging.info("Carga completa de votos, bitácora y logs.")

if __name__ == "__main__":
    main()
