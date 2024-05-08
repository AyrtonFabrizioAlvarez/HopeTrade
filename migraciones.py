import subprocess

# Comandos de Django para ejecutar migraciones
subprocess.run(["python", "manage.py", "makemigrations", "listados"])
subprocess.run(["python", "manage.py", "makemigrations", "sesiones"])
subprocess.run(["python", "manage.py", "makemigrations", "donaciones"])
subprocess.run(["python", "manage.py", "makemigrations", "publicaciones"])
subprocess.run(["python", "manage.py", "makemigrations", "ofrecimientos"])
subprocess.run(["python", "manage.py", "makemigrations", "intercambios"])

subprocess.run(["python", "manage.py", "migrate", "listados"])
subprocess.run(["python", "manage.py", "migrate", "sesiones"])
subprocess.run(["python", "manage.py", "migrate", "donaciones"])
subprocess.run(["python", "manage.py", "migrate", "publicaciones"])
subprocess.run(["python", "manage.py", "migrate", "ofrecimientos"])
subprocess.run(["python", "manage.py", "migrate", "intercambios"])

