from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, url_for, redirect
import json
import os
import sys
import logging

from markupsafe import Markup

import search_queries

app = Flask(__name__)
# TODO: change pwd to env variable
es_client = Elasticsearch('http://localhost:9200', http_auth=("elastic", "Si7DY1hc3Nb9Sj+6WCIp"))

INDEX = 'sinhala_poems_corpus'

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
boy_pic = os.path.join(app.config['UPLOAD_FOLDER'], 'boy.png')


@app.route('/')
def homepage():
    return render_template('index.html', boy_image=boy_pic)

# Custom filter function to highlight the source domain within the line
@app.template_filter('highlight_source_domain')
def highlight_source_domain(line, source_domain):
    source_domains = source_domain.split(', ')
    for domain in source_domains:
        if domain in line:
            line = line.replace(domain, f'<span style="background-color: cyan;">{domain}</span>')
    return Markup(line)

# Custom filter function to get the entire poem by poem_number and the line number of the poem
@app.template_filter('get_entire_poem')
def get_entire_poem(poem_number, line_num_of_poem):
    query_body = search_queries.get_entire_poem_query(poem_number, line_num_of_poem)

    print("??????query_body??????", query_body)
    
    response = es_client.search(
        index=INDEX,
        body=query_body
    )

    print("??????response??????", response)

    total_hits = response['hits']['total']['value']
    if total_hits == 0:
        return "Poem could not be found"
    else:
        max_score = response['hits']['max_score']
        hits_list = response['hits']['hits']
        hits_data = []

        for hit in hits_list:
            _id = hit["_id"]
            _score = hit["_score"]
            _source = hit["_source"]

            poem_number = _source["Poem number"]
            line_num_of_poem = _source["Line number of the peom"]
            poem_name = _source["Poem Name"]
            poet = _source["Poet"]
            year = _source["Year"]
            line = _source["Line"]
            is_metaphot_present = _source["Metaphor present or not"]
            count_of_metaphors = _source["count of the metaphor"]

            print(poem_number, line_num_of_poem)

            source_domain = _source["metaphorical terms(Source domain)"]
            target_domain = _source["Target domain"]

            hits_data.append({"_id": _id, "_score": _score, "poem_number": poem_number, "line_num_of_poem": line_num_of_poem, "poem_name": poem_name, "poet": poet, "year": year, "line": line, "is_metaphot_present": is_metaphot_present, "count_of_metaphors": count_of_metaphors, "source_domain": source_domain, "target_domain": target_domain})

        s =  '\n'.join([hit['line'] for hit in hits_data])
        print(s)
        return s
    # source_domains = source_domain.split(', ')
    # for domain in source_domains:
    #     if domain in line:
    #         line = line.replace(domain, f'<span style="background-color: cyan;">{domain}</span>')
    return Markup('<span style="background-color: cyan;">AAAA</span>')

@app.route('/source_target_search', methods=['POST'])
def source_target_search():

    source_query = request.form.get('source')
    target_query = request.form.get('target')

    if target_query == '':
        query_body = search_queries.get_source_query(source_query)
    elif source_query == '':
        query_body = search_queries.get_target_query(target_query)
    else:
        query_body = search_queries.get_source_target_query(source_query, target_query)

    response = es_client.search(
        index=INDEX,
        body=query_body
    )

    total_hits = response['hits']['total']['value']
    if total_hits == 0:
        return render_template('index.html', hits=[], boy_image=boy_pic)

    else:
        max_score = response['hits']['max_score']
        hits_list = response['hits']['hits']
        hits_data = []

        for hit in hits_list:
            _id = hit["_id"]
            _score = hit["_score"]
            _source = hit["_source"]

            poem_number = _source["Poem number"]
            line_num_of_poem = _source["Line number of the peom"]
            poem_name = _source["Poem Name"]
            poet = _source["Poet"]
            year = _source["Year"]
            line = _source["Line"]
            is_metaphot_present = _source["Metaphor present or not"]
            count_of_metaphors = _source["count of the metaphor"]
        
            source_domain = _source["metaphorical terms(Source domain)"]
            target_domain = _source["Target domain"]

            hits_data.append({"_id": _id, "_score": _score, "poem_number": poem_number, "line_num_of_poem": line_num_of_poem, "poem_name": poem_name, "poet": poet, "year": year, "line": line, "is_metaphot_present": is_metaphot_present, "count_of_metaphors": count_of_metaphors, "source_domain": source_domain, "target_domain": target_domain})

        return render_template('index.html', hits=hits_data, boy_image=boy_pic)

@app.route('/advanced_search', methods=['POST'])
def advanced_search():
    source_query = request.form.get('source')
    target_query = request.form.get('target')
    operation = request.form.get('and-or')
    poet = request.form.get('poet')
    year = request.form.get('year')

    query_body = search_queries.process_advance_search_query(source_query,target_query,poet,year,operation)

    response = es_client.search(
        index=INDEX,
        body=query_body
    )

    total_hits = response['hits']['total']['value']
    if total_hits == 0:
        return render_template('index.html', hits=[], boy_image=boy_pic)

    else:
        max_score = response['hits']['max_score']
        hits_list = response['hits']['hits']
        hits_data = []

        for hit in hits_list:
            _id = hit["_id"]
            _score = hit["_score"]
            _source = hit["_source"]

            poem_number = _source["Poem number"]
            line_num_of_poem = _source["Line number of the peom"]
            poem_name = _source["Poem Name"]
            poet = _source["Poet"]
            year = _source["Year"]
            line = _source["Line"]

            print(_score, line)

            is_metaphot_present = _source["Metaphor present or not"]
            count_of_metaphors = _source["count of the metaphor"]
        
            source_domain = _source["metaphorical terms(Source domain)"]
            target_domain = _source["Target domain"]

            hits_data.append({"_id": _id, "_score": _score, "poem_number": poem_number, "line_num_of_poem": line_num_of_poem, "poem_name": poem_name, "poet": poet, "year": year, "line": line, "is_metaphot_present": is_metaphot_present, "count_of_metaphors": count_of_metaphors, "source_domain": source_domain, "target_domain": target_domain})

        return render_template('index.html', hits=hits_data, boy_image=boy_pic)

if __name__ == "__main__":
    app.run(debug=True)
