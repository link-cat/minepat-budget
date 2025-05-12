# Utilise une image Python légère
FROM python:3.11-slim

# Variables d'environnement pour Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Met à jour les paquets et installe Java + outils nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    curl \
    unzip \
    build-essential \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier uniquement le dossier du projet
COPY projet/ ./projet

# Exposer le port utilisé par l'application
EXPOSE 8000

# Définir le répertoire de travail comme celui contenant manage.py
WORKDIR /app/projet

# Commande par défaut (à adapter selon ton entrée réelle, ex: gunicorn ou python manage.py runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
