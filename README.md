# Sentiments

## Installation
Les librairies nécessaires sont dans le fichier requirements.txt et s'installent dans le projet via la commande :

`pip install -r requirements.txt --no index`

## Execution
Deux méthodes pour lancer le serveur :
 - `python app.py`
 - `export FLASK_APP=/route/vers/app.py && flask run`
 
## Utilisation

### Prédictions
Pour obtenir une prédiction et une réponse en retour, faire une requête **POST** sur l'adresse 127.0.0.1:5000/prediction avec pour donnée { 'sentiment':' [phrase]' } 

### Entraînement
Faire une requête **GET** sur l'adresse 127.0.0.1:5000/entrainement pour obtenir le résultat de l'entrainement de l'API

