#!/bin/sh
# -*- coding: utf-8 -*-

realm_file="/opt/keycloak/data/import/realm-tars.json"
realm_name="tars"

if [ ! -e "/home/already_imported.txt" ]; then
    echo "Importiere Realm $realm_name"
    /opt/keycloak/bin/kc.sh import --file "$realm_file"
    echo "moritz" > /home/already_imported.txt
else
  echo "Realm $realm_name already exists. Skip import."
fi


# let's go!
exec "$@"
