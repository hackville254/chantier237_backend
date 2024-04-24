# Utilisation d'une image de base Alpine Linux optimisée pour Python
FROM python:3.10-alpine

# Définir des variables d'environnement pour éviter les avertissements Python lors de l'exécution en mode non interactif
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créer et définir le répertoire de travail dans le conteneur
WORKDIR /chantier237

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt /chantier237/

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application Django dans le conteneur
COPY . /chantier237/

# Collecter les fichiers statiques de Django
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application Django écoute
EXPOSE 8913

# Commande pour démarrer l'application Django
CMD ["gunicorn", "--bind", "0.0.0.0:8913", "chantier237_Api.wsgi:application"]
