# from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
# import pandas as pd

# Initialize Elasticsearch client
# es = Elasticsearch()
# es = Elasticsearch('http://localhost:9200', basic_auth=("elastic", "Si7DY1hc3Nb9Sj+6WCIp"))

# # Load your dataset (CSV or JSON) into a Pandas DataFrame
# data = pd.read_csv("./song-corpus/190290U-Corpus.csv")

# # Prepare data for indexing (convert to JSON documents)
# actions = []
# for _, row in data.iterrows():
#     doc = row.to_dict() 
#     action = {
#         "_index": "sinhala_poems_corpus",  
#         "_source": doc
#     }
#     actions.append(action)

# # Bulk index the data into Elasticsearch
# success, failed = bulk(es, actions)
# print(f"Indexed {success} documents successfully.")


from elasticsearch import Elasticsearch
import csv

es = Elasticsearch('http://localhost:9200', basic_auth=("elastic", "Si7DY1hc3Nb9Sj+6WCIp"))
index_name = "sinhala_poems_corpus"
csv_file = ".\\song-corpus\\190290U-Corpus.csv"

# Define a function to index a document into Elasticsearch
def index_document(es, index, doc):
    es.index(index=index, body=doc)

# Open and read the CSV file
with open(csv_file, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        # Document to be indexed
        document = {
            "Poem_number": int(row["Poem_number"]),
            "Line_number_of_the_peom": int(row["Line_number_of_the_peom"]),
            "Poem_name": row["Poem_name"],
            "Poet": row["Poet"],
            "Year": int(row["Year"]),
            "Line": row["Line"],
            "Metaphor_present_or_not": row["Metaphor_present_or_not"],
            "Count_of_the_metaphor": int(row["Count_of_the_metaphor"]) if row["Count_of_the_metaphor"] else None,
            "metaphorical_term_source_domain": row["metaphorical_term_source_domain"],
            "Target_domain": row["Target_domain"],
        }
        # Index the document
        index_document(es, index_name, document)

print("Data from CSV file has been indexed in Elasticsearch.")
