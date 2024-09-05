
# Projet Django

Ceci est une application Django utilisant PostgreSQL pour la base de données. Le projet inclut une documentation Swagger accessible à l'URL `/swagger`.

## Prérequis

- **Python** : Assurez-vous d'avoir installé **Python 3.10** ou une version supérieure.
- **PostgreSQL** : Une base de données PostgreSQL doit être configurée.

## Installation

### 1. Cloner le dépôt

Clonez le dépôt sur votre machine locale :

```bash
git https://github.com/link-cat/minepat-budget.git
cd minepat-budget
```

### 2. Créer et activer un environnement virtuel

Créez un environnement virtuel pour isoler les dépendances du projet :

```bash
python3.10 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

### 3. Installer les dépendances

Installez les dépendances à partir du fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Créez une base de données PostgreSQL avec le nom **`projet`** :

```sql
CREATE DATABASE projet;
```

### 5. Configurer le fichier `.env`

Renommez le fichier **`.env.example`** en **`.env`** :

```bash
mv .env.example .env
```

Ensuite, ouvrez le fichier `.env` et entrez vos informations de base de données

### 6. Effectuer les migrations

Déplacez-vous vers le répertoire du projet :

```bash
cd projet/
```

Ensuite, appliquez les migrations :

```bash
python manage.py migrate
```

### 7. Lancer le serveur

Pour démarrer le serveur de développement, exécutez :

```bash
python manage.py runserver
```

### 8. Créer un super utilisateur

Afin de gérer votre application via l'interface d'administration, créez un super utilisateur :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour entrer le nom d'utilisateur, l'adresse e-mail et le mot de passe.

## Documentation

La documentation Swagger est accessible à l'URL suivante après avoir démarré le serveur :

```
http://localhost:8000/swagger/
```

## Auteur

- **Link**.

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
```

### Explication des sections :

1. **Prérequis** : J'indique que Python 3.10 et PostgreSQL sont nécessaires.
2. **Installation** : Je décris les étapes pour cloner le dépôt, créer un environnement virtuel, installer les dépendances, configurer la base de données, appliquer les migrations, démarrer le serveur et créer un super utilisateur.
3. **Documentation** : L'accès à la documentation Swagger est clairement indiqué.

Ce README contient les bonnes commandes et structure pour rendre ton projet facilement compréhensible et exécutable par les autres développeurs.
