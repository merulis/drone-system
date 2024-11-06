# drone-system

# Set TRAEFIK_HASH_PASS
[traefik_docs](https://doc.traefik.io/traefik/middlewares/http/basicauth/)

1. Complite 
    ```bash
    echo $(htpasswd -nb your_user your_passwd) | sed -e s/\\$/\\$\\$/g
    ```
2. You will see
    ```bash
    your_user:$$apr1$$kuCA0.qi$$XTPSRk8lxwbGOlebYM1Aa/
    ```
    Copy that in .env like for example

    ```
    TRAEFIK_USER="your_user"
    TRAEFIK_HASH_PASSWORD="$$apr1$$kuCA0.qi$$XTPSRk8lxwbGOlebYM1Aa/"
    ```
