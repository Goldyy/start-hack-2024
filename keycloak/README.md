# Keycloak

## Prerequisites

- Docker (+ Compose)
- Terraform

## Setup

### 1. Prepare environment variables

```shell
# configure terraform backend
export TF_HTTP_USERNAME=<gitlab-user> # gitlab username
export TF_HTTP_PASSWORD=glpat-xxxxxxxxxxxxxxxxxxxx # personal access token
export TF_VAR_DOMAIN_PRIMARY=http://localhost:4200 # frontend redirect URL

# configure keycloak access, same values as in docker compose file
export KEYCLOAK_URL="http://localhost:8080"
export KEYCLOAK_USER="admin"
export KEYCLOAK_PASSWORD="admin"
```

### 2. Start Keycloak

```shell
docker compose up --force-recreate --build
```

### 3. Configure Keycloak via Terraform

```shell
terraform init
terraform plan
terraform apply
```


### 4. Keycloak Config laden
1. In Admin UI anmelden
2. Im Realm Dropdown Menü `Create Realm` auswählen
3. Keycloak Config File aus Ordner `keycloak-config` in Dropzone ziehen und hinzufügen abschließen