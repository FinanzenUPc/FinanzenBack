# Project Structure

D:\COMPLEJIDAD ALGORITMICA\Trabajo Final\BACKEND\
├───.gitignore
├───alembic.ini
├───AZURE_SETUP.md
├───Makefile
├───Procfile
├───pytest.ini
├───README.md
├───requirements.txt
├───startup.sh
├───test_azure_config.py
├───TROUBLESHOOTING.md
├───.claude\
├───.git\...
├───.github\
│   └───workflows\
│       └───main_finanzenbackend.yml
├───.venv\...
├───alembic\
│   ├───env.py
│   ├───script.py.mako
│   └───versions\
├───app\
│   ├───main.py
│   ├───__pycache__\
│   ├───core\
│   │   ├───config.py
│   │   ├───database.py
│   │   ├───security.py
│   │   └───__pycache__\
│   ├───models\
│   │   ├───transaction.py
│   │   ├───user.py
│   │   └───__pycache__\
│   ├───routers\
│   │   ├───algorithms_router.py
│   │   ├───auth.py
│   │   ├───dataset_router.py
│   │   ├───graph_router.py
│   │   ├───transactions.py
│   │   └───__pycache__\
│   ├───schemas\
│   │   ├───transaction.py
│   │   ├───user.py
│   │   └───__pycache__\
│   ├───services\
│   │   ├───algorithms_service.py
│   │   ├───dataset_service.py
│   │   ├───graph_service.py
│   │   ├───transaction_service.py
│   │   ├───user_service.py
│   │   └───__pycache__\
│   └───utils\
│       ├───bellman_ford.py
│       ├───bfs.py
│       ├───dfs.py
│       ├───dijkstra.py
│       ├───dp_mochila.py
│       ├───floyd_warshall.py
│       ├───graph_builder.py
│       ├───mst_kruskal.py
│       ├───mst_prim.py
│       ├───union_find.py
│       └───__pycache__\
├───scripts\
│   ├───clean.py
│   ├───create_db.py
│   ├───init_db.py
│   ├───setup_db.py
│   └───__pycache__\
└───tests\
    ├───conftest.py
    ├───test_auth.py
    └───test_main.py
