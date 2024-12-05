from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings

# Inisialisasi SPARQL endpoints
local_sparql = SPARQLWrapper(settings.GRAPHDB_URL)
local_sparql.setReturnFormat(JSON)
wikidata_sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
wikidata_sparql.setReturnFormat(JSON)

# Export untuk digunakan di modul lain
__all__ = ['local_sparql', 'wikidata_sparql']
