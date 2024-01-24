#!/usr/bin/env python3
from subprocess import run, PIPE

def terraform_output(output_name):
    cmd = f"terraform output {output_name}"
    result = run(cmd, shell=True, stdout=PIPE, text=True)
    return result.stdout.strip()

def generate_inventory():
    cp_node_ip = terraform_output("cp_instance_ip")
    worker_node_ips = terraform_output("worker_instance_ips").split("\n")
    worker_node_ips = worker_node_ips[1:len(worker_node_ips)-1]

    inventory = "[cp_nodes]\ncp_node ansible_host={cp_node_ip} ansible_user=k8s-project ansible_ssh_private_key_file=../.ssh/ansible_key\n\n[worker_nodes]".format(cp_node_ip=cp_node_ip)

    for index, worker_node_ip in enumerate(worker_node_ips):
        if worker_node_ip:
            inventory += f"\nworker_node_{index + 1} ansible_host={worker_node_ip.strip().replace(',', '')} ansible_user=k8s-project ansible_ssh_private_key_file=../.ssh/ansible_key"

    inventory += "\n\n[all:children]\ncp_nodes\nworker_nodes"

    print(inventory)

if __name__ == "__main__":
    generate_inventory()
