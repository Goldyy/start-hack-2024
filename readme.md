# OVO-HUNTERS Setup

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [`mkcert`](https://github.com/FiloSottile/mkcert) - Optional. Only if certificates other than those in the repo are required. 

## Installation (Linux/Mac)
1. Clone this repository

2. *Optional. Only if certificates other than those in the repo are required.*<br>Generate a local CA using `mkcert`...

    ```bash
    $ mkcert -install # only needed once after installation of mkcert
    ```

3. *Optional. Only if certificates other than those in the repo are required.*<br>Generate a wildcard certificate for your local setup...

    ```bash
    $ mkcert --cert-file traefik/ssl/_wildcard.dev.ovo-hunters.pem --key-file traefik/ssl/_wildcard.dev.ovo-hunters-key.pem '*.dev.ovo-hunters'
    ```


5. Startup setup...
    ```bash
    $ docker compose up --build
    ```

6. Accessing the services...
    - **Traefik Dashboard** <br> https://127.0.0.1/traefik
    - **Backend Swagger API** <br> https://127.0.0.1/backend/api/doc/



## Development

### Backend
1. There's a requirements.txt in backend/. Feel free to use conda or venv for your development.<br>https://code.visualstudio.com/docs/python/environments

![Video](StartHack24.mp4)
