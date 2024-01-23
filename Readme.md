## Créer l'infrastructure et déployer kafka:

`cd CI_CD/Scripts`
`sudo k8s_cluster.sh`

## Génerer les clés ssh
ssh-keygen -t rsa -b 2048 -f ../.ssh/ansible_key -C "cis-project"
cp ../.ssh/ansible_key ~/.ssh/
cp ../.ssh/ansible_key.pub ~/.ssh/


# L'ajout de la clé de GCP aux variables d'environements:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\hp\Desktop\SDTD\Credentials\sdtd-key.json"

# Création du container mongo:
docker run --name mongo -d -p 27017:27017 mongo:latest

A Voir:
    Var d'env

