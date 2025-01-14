#!/bin/bash

# Variables
BACKUP_DIR="./db_backups"
DB_NAME="projet"
DB_USER="postgres"
DB_PASSWORD="link2024"
DB_HOST="localhost"
DB_PORT="5442"

# Création du répertoire de backup si nécessaire
mkdir -p "$BACKUP_DIR"

# Suppression du dump de la veille
find "$BACKUP_DIR" -type f -mtime +0 -name "*.sql" -exec rm {} \;

# Génération d'un nouveau dump
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y-%m-%d).sql"

export PGPASSWORD=$DB_PASSWORD
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup réussi : $BACKUP_FILE"
else
    echo "Échec du backup"
    exit 1
fi
