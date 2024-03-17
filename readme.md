# OVO-HUNTERS Setup

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [`mkcert`](https://github.com/FiloSottile/mkcert) - Optional. Only if certificates other than those in the repo are required. 

## Installation (Linux/Mac)
1. Clone this repository

2. *Optional. Only if certificates other than those in the repo are required.*<br>Generate a local CA using `mkcert`

    ```bash
    $ mkcert -install # only needed once after installation of mkcert
    ```

3. *Optional. Only if certificates other than those in the repo are required.*<br>Generate a wildcard certificate for your local setup

    ```bash
    $ mkcert --cert-file traefik/ssl/_wildcard.dev.ovo-hunters.pem --key-file traefik/ssl/_wildcard.dev.ovo-hunters-key.pem '*.dev.ovo-hunters'
    ```

4. Redirect dev.ovo-hunters to your host/dev
    ```bash
    $ sudo nano /etc/hosts
    ```
    Then add the following lines to the file:
    ```bash
    # for ovo-hunters (hackathon starthack st. gallen 2024)
    127.0.0.1 dev.ovo-hunters
    ```

5. Startup setup
    ```bash
    $ docker compose up --build
    ```

6. Accessing the services
    - Traefik Dashboard<br>https://dev.ovo-hunters/traefik. 
