#!/bin/bash

/opt/graphdb/dist/bin/importrdf load -f -c /graphdb-data/Nama-Kelompok-config.ttl -m parallel /graphdb-data/NamaKelompok_RDF.ttl
/opt/graphdb/dist/bin/graphdb -s