# Distributed Systems for Data Processing with a Kubernetes Cluster Created Using kubeadm

## Project setup:

- Go to `K8s-cluster-with-kubeadm` directory

- Copy *YOUR_GCP_KEY* in this folder `./CI_CD/Credentials`

#### Generate SSH keys:

`ssh-keygen -t rsa -b 2048 -f ./CI_CD/.ssh/ansible_key -C "k8s-project"`

`cp ./CI_CD/.ssh/ansible_key ~/.ssh/`

`cp ./CI_CD/.ssh/ansible_key.pub ~/.ssh/`

#### Connect to gcloud:

`gcloud auth login --cred-file=./CI_CD/Credentials/[YOUR_GCP_KEY].json`

`gcloud config set project [YOUR_PROJECT_ID]`

#### Create K8s cluster & deploy applications:

Go to `K8s-cluster-with-kubeadm` directory

`cd ./CI_CD/Scripts`

`sudo ./k8s_cluster.sh`

#### Connect to the master via SSH:

- Retrieve the master's IP address from the inventory file `./CI_CD/Ansible/inventory`

- Use the following command:
`ssh -i .\CI_CD\.ssh\ansible_key -o StrictHostKeyChecking=no k8s-project@[CLUSTER_IP_ADDRESS]`

----------
----------



## Installer Kompose en Ubuntu:

`sudo curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-linux-amd64 -o /usr/local/bin/kompose`

`chmod a+x /usr/local/bin/kompose`

## Use Kompose:

`python3 ./CI_CD/Apps/replace_env_variables/replace_env_variables.py ./CI_CD/Apps/dataProcessing/`

`sudo kompose convert -f docker-compose-env.yaml -o ../../Manifests/DataProcessing/ --with-kompose-annotation=false --build local --push-image=True -v`


## L'ajout de la clé de GCP aux variables d'environements:
$env:GOOGLE_APPLICATION_CREDENTIALS="[YOUR_GCP_KEY]"
