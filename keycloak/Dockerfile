# --- build stage
FROM quay.io/keycloak/keycloak:22.0.1 as build

# environment
ENV KC_HEALTH_ENABLED=true

# run build
RUN /opt/keycloak/bin/kc.sh build --db=postgres

# --- final stage
FROM quay.io/keycloak/keycloak:22.0.1

USER root

# copy build results
COPY --from=build /opt/keycloak/ /opt/keycloak/

# copy entrypoint
COPY docker/entrypoint.sh /entrypoint.sh

# copy configuration
RUN mkdir -p /opt/keycloak/data/import
COPY keycloak-config/realm-tars.json /opt/keycloak/data/import/realm-tars.json

# copy theme
#COPY theme/tars /opt/keycloak/themes/tars

# define entrypoint & command
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "/opt/keycloak/bin/kc.sh", "start", "--optimized" ]

