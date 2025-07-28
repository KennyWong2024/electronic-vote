import sys
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import text

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'bronze'))
sys.path.append(os.path.join(script_dir, 'utils'))

from load_votantes import main as cargar_votantes
from load_poblados import main as cargar_poblados
from load_candidatos import main as cargar_candidatos
from load_votos import main as cargar_votos
from generate_votos import generate_votos
from db_connection import get_engine

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def cargar_entorno():
    load_dotenv(dotenv_path=os.path.join(script_dir, '..', '.env'))
    required = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        logging.error(f"Faltan variables de entorno: {', '.join(missing)}")
        sys.exit(1)
    logging.info('Variables de entorno cargadas correctamente.')

def verificar_conexion():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logging.info("Conexión a la base de datos establecida correctamente.")
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        sys.exit(1)

def mostrar_menu_principal():
    print("=== Menú Principal ===")
    print("1) Cargar datos")
    print("2) Salir")

def mostrar_menu_carga():
    print("\n--- Cargar Datos ---")
    print("1) Cargar votantes")
    print("2) Cargar poblados")
    print("3) Cargar candidatos y partidos") 
    print("4) Generar votos aleatorios (CSV)")
    print("5) Cargar votos generados")
    print("6) Volver")

def main():
    setup_logging()
    cargar_entorno()
    verificar_conexion()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione opción: ").strip()

        if opcion == '1':
            while True:
                mostrar_menu_carga()
                sub = input("Seleccione opción de carga: ").strip()
                if sub == '1':
                    logging.info("Iniciando carga de datos de votantes...")
                    cargar_votantes()
                elif sub == '2':
                    logging.info("Iniciando carga de datos de poblados...")
                    cargar_poblados()
                elif sub == '3':
                    logging.info("Iniciando carga de partidos y candidatos...")
                    cargar_candidatos()
                elif sub == '4':
                    logging.info("Generando votos aleatorios localmente (CSV)...")
                    generate_votos()
                elif sub == '5':
                    logging.info("Cargando votos desde CSV a la base de datos...")
                    cargar_votos()
                elif sub == '6':
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")

        elif opcion == '2':
            logging.info("Saliendo del programa.")
            sys.exit(0)

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == '__main__':
    main()
