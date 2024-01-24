provider "google" {
  credentials = file("../Credentials/cis-key.json")
  project     = var.project_id
  region      = var.region
}

resource "google_compute_network" "vpc_network" {
  name                    = "cluster-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "cluster_subnet" {
  name          = "cluster-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.name
}

resource "google_compute_instance" "cp_node" {
  name         = "cp"
  machine_type = "e2-standard-2"
  zone         = "us-central1-a"
  tags         = ["allow-http"]

  boot_disk {
    initialize_params {
      size = 20
      type = "pd-balanced"
      image = "ubuntu-os-cloud/ubuntu-2004-focal-v20230605"
    }
  }

  service_account {
    scopes = ["cloud-platform"]
  }

  network_interface {
    network     = google_compute_network.vpc_network.name
    subnetwork  = google_compute_subnetwork.cluster_subnet.name
    access_config {}
  }

  metadata = {
    ssh-keys = "k8s-project:${file("../.ssh/ansible_key.pub")}"
  }
}

resource "google_compute_instance" "worker_node" {
  count        = 3
  name         = "worker-${count.index + 1}"
  machine_type = "e2-standard-2"
  zone         = "us-central1-a"
  tags         = ["allow-http"]

  boot_disk {
    initialize_params {
      size = 20
      type = "pd-balanced"
      image = "ubuntu-os-cloud/ubuntu-2004-focal-v20230605"
    }
  }

  service_account {
    scopes = ["cloud-platform"]
  }

  network_interface {
    network     = google_compute_network.vpc_network.name
    subnetwork  = google_compute_subnetwork.cluster_subnet.name
    access_config {}
  }

  metadata = {
    ssh-keys = "k8s-project:${file("../.ssh/ansible_key.pub")}"
  }
}

resource "google_compute_firewall" "vpc_firewall" {
  name        = "vpc-firewall"
  network     = google_compute_network.vpc_network.name
  direction   = "INGRESS"
  allow {
    protocol = "all"
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-http"]
}

#############################   OUTPUTS   ##################################
############################################################################

output "cp_instance_ip" {
  value = google_compute_instance.cp_node.network_interface[0].access_config[0].nat_ip
}

output "worker_instance_ips" {
  value = [for instance in google_compute_instance.worker_node : instance.network_interface[0].access_config[0].nat_ip]
}