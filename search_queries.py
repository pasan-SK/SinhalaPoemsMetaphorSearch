SIZE = 10

def get_source_query(source):
    query = {
        "size": SIZE,
        "query": 
        {
            "bool": 
            {
            "must":
            {
                "match": 
                { 
                    "metaphorical terms(Source domain).case_insensitive_and_inflections": source
                }
            }
            }
        }
        }
    return query

def get_target_query(target):
    query = {
        "size": SIZE,
        "query": 
        {
            "bool": 
            {
            "must": 
            { 
                "match": 
                { 
                    "Target domain.case_insensitive_and_inflections": target
                } 
            }
            }
        }
    }
    return query

def get_source_target_query(source, target, operation='and'):
    if operation == 'and':
        query = {
            "size": SIZE,
            "query": 
            { 
                "bool": 
                { 
                "must":
                [
                    { "match": { "metaphorical terms(Source domain).case_insensitive_and_inflections": source}},
                    { "match": { "Target domain.case_insensitive_and_inflections": target}}
                ]
                }
            }
        }
    else:
        query = {
            "size": SIZE,
            "query": 
            { 
                "bool": 
                { 
                "should":
                [
                    { "match": { "metaphorical terms(Source domain).case_insensitive_and_inflections": source}},
                    { "match": { "Target domain.case_insensitive_and_inflections": target}}
                ]
                }
            }
        }

    return query

def process_advance_search_query(source, target, poet, year, operation='and'):
    conditions_list =[]
    filter_list = []

    if source != '':
        conditions_list.append({ "match": { "metaphorical terms(Source domain).case_insensitive_and_inflections": source}})
    if target != '':
        conditions_list.append({ "match": { "Target domain.case_insensitive_and_inflections": target}})
    if poet != "Not Selected":
        filter_list.append({ "match": { "Poet.case_insensitive_and_inflections": poet}})
    if year != "Not Selected":
        filter_list.append({ "match": { "Year": year}})

    query = {}
    if operation == 'and':
        query = {
            "size": SIZE,
            "query": {
                "bool": {
                    "must": conditions_list,
                    "filter": filter_list
                }
            }
        }
    else:
        query = {
            "size": SIZE,
            "query": {
                "bool": {
                    "should": conditions_list,
                    "filter": filter_list,
                }
            }
        }

    return query

def get_entire_poem_query(poem_number, line_num_of_poem):
    query = {
        "size": SIZE,
        "query": 
        {
            "bool": 
            {
                "must": 
                { 
                    "term": 
                    { 
                        "Poem number": poem_number
                    } 
                }
                # "must": 
                # { 
                #     "match": 
                #     { 
                #         "Line number of the peom": line_num_of_poem
                #     } 
                # }
            }
        }
    }
    return query




