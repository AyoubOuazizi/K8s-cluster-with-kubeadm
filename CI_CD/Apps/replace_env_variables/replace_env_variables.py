import os
import re
from dotenv import load_dotenv
import sys

def replace_env_variables(folder_path):
    # Construire les chemins complets des fichiers .env et docker-compose.yml
    env_file_path = os.path.join(folder_path, '.env')
    docker_compose_path = os.path.join(folder_path, 'docker-compose.yaml')

    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv(dotenv_path=env_file_path)

    # Lire le contenu du fichier docker-compose.yml
    with open(docker_compose_path, 'r') as f:
        content = f.read()

    # Recherche des variables d'environnement dans le format ${VAR_NAME}
    env_pattern = re.compile(r'\$\{(.+?)\}')

    def replace_env(match):
        env_var = match.group(1)
        # Récupérer la valeur de la variable d'environnement
        env_value = os.environ.get(env_var, f'${{{env_var}}}')
        return env_value

    # Remplacer les variables d'environnement dans le contenu
    updated_content = env_pattern.sub(replace_env, content)

    # Écrire le contenu mis à jour dans un nouveau fichier docker-compose-env.yml
    modified_docker_compose_path = os.path.join(folder_path, 'docker-compose-env.yaml')
    with open(modified_docker_compose_path, 'w') as f:
        f.write(updated_content)

    print(f"Les variables d'environnement ont été mises à jour dans {modified_docker_compose_path}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /chemin/vers/dossier")
        sys.exit(1)

    folder_path = sys.argv[1]

    replace_env_variables(folder_path)