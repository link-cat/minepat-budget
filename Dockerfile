# Utilise une image Python légère basée sur Debian Bookworm (stable)
FROM python:3.11-slim-bookworm

# Variables d'environnement
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV DEBIAN_FRONTEND=noninteractive
ENV ACCEPT_EULA=Y

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système + OpenJDK 17 + polices (alternative à Arial)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    build-essential \
    libpq-dev \
    fontconfig \
    wget \
    gnupg \
    ca-certificates \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Alternative à ttf-mscorefonts-installer (Arial, etc.)
# Télécharge les polices Microsoft Core Fonts depuis un miroir tiers
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && wget -qO- https://github.com/velitasali/ttf-mscorefonts-installer/raw/master/ttf-mscorefonts-installer_3.8_all.deb -O /tmp/mscorefonts.deb \
    && dpkg -i /tmp/mscorefonts.deb || apt-get install -f -y \
    && rm /tmp/mscorefonts.deb \
    && fc-cache -f -v

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY projet/ ./projet

# Exposer le port
EXPOSE 8000

# Changer de répertoire
WORKDIR /app/projet

# Commande par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]