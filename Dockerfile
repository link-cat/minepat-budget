# Utilisez une image Python légère
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier uniquement le dossier du projet
COPY projet/ ./projet

# Exposer le port 8000
EXPOSE 8000

# Définit le répertoire de travail comme le dossier contenant `manage.py`
WORKDIR /app/projet
