# Utilisez une image de base avec Python
FROM python:3.8-slim

# Créez le répertoire de travail
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt ./
COPY stats-app.py ./
COPY .env ./

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exécutez le script Python
CMD ["python", "stats-app.py"]