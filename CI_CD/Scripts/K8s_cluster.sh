#!/bin/bash

# Run Terraform
cd ../Terraform
terraform init || { echo "Terraform init failed"; exit 1; }
terraform apply -auto-approve || { echo "Terraform apply failed"; exit 1; }

# Generate Ansible inventory
../Scripts/terraform_inventory.py > ../Ansible/inventory || { echo "Inventory generation failed"; exit 1; }

# Wait for resources to be ready
echo "Waiting for resources to be ready..."
sleep 60  # Pause de 60 secondes (ajuster selon vos besoins)

# Run Ansible playbooks
cd ../Ansible
ansible-playbook playbooks/configure_k8s_nodes.yml || { echo "Ansible playbook { configure_k8s_nodes } failed"; exit 1; }
ansible-playbook playbooks/deploy_kafka.yaml || { echo "Ansible playbook { deploy_kafka } failed"; exit 1; }
ansible-playbook playbooks/deploy_mongodb.yaml || { echo "Ansible playbook { deploy_mongodb } failed"; exit 1; }
ansible-playbook playbooks/deploy_traffic_capture_app.yaml || { echo "Ansible playbook { deploy_traffic_capture_app } failed"; exit 1; }
ansible-playbook playbooks/deploy_processing_app.yaml || { echo "Ansible playbook { deploy_processing_app } failed"; exit 1; }
ansible-playbook playbooks/grafana_prometheus.yaml || { echo "Ansible playbook { grafana_prometheus } failed"; exit 1; }
# Clean up: Uncomment and adjust as needed
# terraform destroy -auto-approve