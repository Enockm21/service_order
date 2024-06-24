# Utiliser une image de base officielle de Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de votre application dans le conteneur
COPY . /app

# Installer les dépendances de votre application
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application Django va fonctionner
EXPOSE 8000

# Définir la commande de démarrage de l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_order.wsgi:application"]
