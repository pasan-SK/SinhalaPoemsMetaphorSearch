from elasticsearch import Elasticsearch
import csv

es = Elasticsearch('http://localhost:9200', basic_auth=("elastic", "Si7DY1hc3Nb9Sj+6WCIp"))
index_name = "sinhala_poems_corpus"

def search_data(es, index, query):
    result = es.search(index=index, query=query)
    return result

# This query retrieves all documents in the index.
query = {
    "match_all": {}
}

search_result = search_data(es, index_name, query)

# Display the total number of documents
total_hits = search_result['hits']['total']['value']
print(f"Total documents found: {total_hits}\n")

# Display the first few documents 
for hit in search_result['hits']['hits']:
    print(hit['_source'])
    print("\n")
