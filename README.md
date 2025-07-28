# Arquitectura Conceptual de Voto Electrónico
El requerimiento funcional del proyecto radica en diseñar la arquitectura de un sistema de voto electrónico, por lo cual, todo el diagrama de la aplicación
es unicamente conceptual, y busca plantear un sistema con capas de seguridad robusta orientado a un sistema cloud, ver la trazabilidad del voto manteniendo el derecho
al sufragio anónimo, así como garantizando controles que impidan el fraude y el sistema tenga datos de auditoría sin que estos puedan enlazarse con un votante.

A nivel de bases de datos se utiliza postgres, no se eligió por ser la opción ideal, sino porque los recursos que teniamos en clase nos permitian levantar esta base de datos
en Azure con el fin de introducirnos a arquitecturas y sistemas Cloud. Pate de ello, es importante aclarar que mas allá de las bases de datos de lectura y escritura, planteadas
en postgres, tambien se diseña y se construye una base de datos analítica, para la cual, se utiliza postgres por ser el recurso a mano; sin embargo, aclaramos que 
existen bases de datos analíticas enfocadas para escenarios como este, y que en una situación real no se construiría con postgres para el analisis.

Los requerimientos del proyecto y el documento entregable para el curso están en la documentración /docs, con el fin de poder revisar y comprender porque se tomaron 
algunas decisiones de diseño.

## Arquitectura del proyecto 
```bash
electronic-vote/
├── README.md
├── LICENSE 
├── .env                                    # Variables de entorno para conexiones
│
├── docs/                                   # Documentación formal del proyecto
│   └── documento_proyecto.pdf
│
├── assets/                                 # Logos, íconos, imágenes para diagramas o README
│
├── diagrams/                               # Archivos draw.io con las arquitecturas conceptuales
│   ├── arquitectura.drawio
│   ├── arquitectura.png
│   ├── base_lectura.drawio
│   ├── base_escritura.drawio
│   ├── analitica_medalion.drawio
│   └── analitica_medalion.png
│
├── data/                                   # Archivos de datos originales
│   ├── votantes/                           # Segmentados para optimizar carga
│   │   ├── padron_chunk_1.csv
│   │   ├── padron_chunk_2.csv
│   │   └── ...
│   └── poblados/                           # Uno solo, es liviano
│       └── poblados_costa_rica.csv
│
├── scripts/
│   ├── load.py                             # Entrada principal, parsea CLI y ejecuta lo necesario
│   ├── requirements.txt
│   ├── bronze/                             # Procesos de carga inicial a la base (CSV a bronze)
│   │   ├── load_votantes.py
│   │   └── load_poblados.py
│   │   └── .....
│   ├── utils/
│   ├── db_connection.py
│   └── data_loader.py
│
├── sql/                                    # Consultas SQL para construir la base de datos analítica
│   ├── 01. Creación de Schemas.sql
│   ├── 02. Creación de Tablas Bronze.sql
│   └── 03. Triggers de Control.sql
│
└── .gitignore
```

## Configuración
### Terminal
En caso de utilziar Mac o Linux no se requiere ninguna configuración previa, por otro lado, si se utiliza Windows, como en mi caso, instalar WLS (Subsistema de Linux) e instalar Ubuntu, no utilizar terminales de PowerShell ni CMD, para mayor información de WSL visitar el siguiente enlace.
```bash
https://learn.microsoft.com/es-es/windows/wsl/install
```

*Nota: Es necesario instalar Python en el subsistema de Linux, este no viene preinstalado*

### Variables de entorno
Crear un archivo *.env* en la raiz del proyecto e ingresarle las siguientes variables. *Recordar adaptarlo con los datos propios de la base a cargar.*
```bash
DB_USER=usuario_con_permisos
DB_PASSWORD=su_contraseña
DB_HOST=host_oara_la_base_de_datos
DB_PORT=puerto_de_conexión
DB_NAME=nombre_base_de_datos
```

### Entorno Virtual
Es una buena práctica para no instalar librerias en el subsistema o bien en el sistema operativo, creamos un entorno virtual aislado donde se instalan estas dependencias para ejecutar el proyecto.
```bash
# Creamos el entorno
python3 -m venv venv

# Lo activamos
source venv/bin/activate

# Vamos al repositorio de scripts
cd scripts

# Instalamos dependencias
pip install -r requirements.txt
```

### Preparación Postgres
Antes de proceder a ejecutar nuestro código en el entorno virtual, vamos a crear las tablas necesarias para simular el ejercicio de análisis, ejecutaremos una a una las consultas en orden, están enumeradas para facilitar su ejecución, estas, si, se pueden ejecutar desde Python, pero mantendremos la ejecución manual para entender lo que estamos haciendo y evidenciar las consultas construidas.

Entre las consultas, tenemos la creación de los esquemas.
- Bronze (Raw Data).
- Silver (Transforms).
- Gold (Curated Data).

Aparte tenemos la creación de las tablas, y un pequeño trigger que nos evalua si un voto es válido, bajo la lógica que si la papeleta (Electronica) es de presidencia el candidatoa presidente no puede estar nulo, si lo está, el voto es nulo, y de diputados, el partido si está nulo, el voto es nulo, se deja la posibilidad de realizar votos nulos ya que es parte de un escenario realista. Para ello, se asignaron porcentajes de votos nulos con el fin de emular el escenario completo.

## Ejecución de Scripts
Dentro de el directorio *Scripts*, tenemos una serie de códigos que nos van a facilitar el proceso de carga de datos, vamos al path correspondiente donde se encuentra el **load.py**:
```bash
source venv/bin/activate

cd scripts
```
*Nota: No olvidar usar la consolar de Linux, abrir una nueva terminal para iniciar de cero, a este punto ya seguimos los pasos de arriba y el entorno vitual debió ser creado, recalco, si usaron otra consola para crear el entorno, va a dar error porque LINUX/UNIX son terminales distintas a CMD/PowerShell*

Luego, ejecutamso el script:
```bash
python3 load.py
```

Nos saldrá un menú, hagamos todo en orden, seleccionamos *Cargar datos* y luego uno a uno los datos en orden, primero votantes, luego, cuando termine la operación continuamos con poblados, eventualmente con candidatos y finalmente con los votos aleatorios, este tiene una particularidad, si se genera un bulk insert con la logica del escenario planteado dura muchisimo, se recomienda una maquina con buena memoria para primero generar los votos localmente en *.csv* y luego cargarlos con el mismo método de carga de los votantes.

Para esta carga primero ejecutaremos el paso 4, que genera datos aleatorios con las reglas bien estipuladas para Bitacora, Votos y Logs, cuando termine la ejecución, continuamos con el paso 5, que cargará en paralelo la información a la base de datos.