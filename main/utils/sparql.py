from SPARQLWrapper import SPARQLWrapper, JSON

# Inisialisasi SPARQL endpoints
host = "http://localhost:7200"
local_sparql = SPARQLWrapper(f"{host}/repositories/Nama-Kelompok")
local_sparql.setReturnFormat(JSON)
wikidata_sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
wikidata_sparql.setReturnFormat(JSON)

# Export untuk digunakan di modul lain
__all__ = ['local_sparql', 'wikidata_sparql']
