# Utilise une image Python légère
FROM python:3.11-slim

# Variables d'environnement pour Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Installer Java, outils de compilation, PostgreSQL, et polices Arial (via ttf-mscorefonts-installer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    curl \
    unzip \
    build-essential \
    libpq-dev \
    fontconfig \
    wget \
    gnupg \
    ca-certificates \
    && echo "deb http://ftp.debian.org/debian buster main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://security.debian.org buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    ttf-mscorefonts-installer \
    && fc-cache -f -v \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Accepter la licence Microsoft (évite les erreurs non-interactives)
ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND=noninteractive

# Répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier du projet
COPY projet/ ./projet

# Exposer le port utilisé par l'application
EXPOSE 8000

# Définir le répertoire de travail comme celui contenant manage.py
WORKDIR /app/projet

# Commande par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
