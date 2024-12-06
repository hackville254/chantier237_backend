# Utilisation d'une image légère basée sur Alpine Linux pour Python
FROM python:3.10-alpine

# Configuration des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Définition du répertoire de travail
WORKDIR /chantier237

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application
COPY . .

# Exposition du port de l'application
EXPOSE 8013

# Commande de démarrage de l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8013", "chantier237_Api.wsgi:application"]
