from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

es = Elasticsearch('http://localhost:9200', basic_auth=("elastic", "Si7DY1hc3Nb9Sj+6WCIp"))
# print(es.ping())
# print(es.info())

# CREATE INDEX
# es.create(index='sinhala_poems_corpus')

# PRINT ALL INDEXES
# indice_aliases = (es.indices.get_alias(index="*"))
# for index_name in indice_aliases:
#     print(index_name)

# SEARCH INDEX

page_size = 15
from_offset = 0

res = es.search(
        index="amazon-reviews", 
        query={"match_all": {}},
        size=page_size,
        from_=from_offset
    )

print("Got %d Hits:" % res['hits']['total']['value'])
hits = res['hits']['hits']
print("Got %d Hits:" % len(hits))
for hit in hits:
    print("%(review_title)s : %(stars)s" % hit["_source"])