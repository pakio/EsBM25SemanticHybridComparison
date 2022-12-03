import streamlit as st
import requests
import json

es_url = "http://127.0.0.1:9200"
model_name = "sentence-transformers__msmarco-minilm-l-12-v3"
index_name = "wiki"
vector_field = "_vector.predicted_value"
text_field = "title"

def main():
    st.set_page_config(layout="wide")
    
    query = st.text_input('query')
    if query == "":
        exit()
    
    col1, col2, col3 = st.columns(3)

    resp = get_vector_response(query).json()
    vec = ext_vector(resp)

    with col1:
        st.header("lexical matching")
        resp, q = text_search(query)
        render_title_and_url(resp.json())
        st.json(q)

    with col2:
        st.header("semantic matching")
        resp, q = knn_search(vec)
        render_title_and_url(resp.json())
        st.json(q)

    with col3:
        st.header("hybrid search")
        resp, q = hybrid_search(query, vec)
        render_title_and_url(resp.json())
        st.json(q)


def get_vector_response(query: str):
    path = "/_ml/trained_models/{model}/deployment/_infer"

    req = {
        "docs": {
            "text_field": query
        }
    }

    headers = {'content-type': 'application/json'}
    return requests.post(es_url + path.format(model=model_name), data=json.dumps(req), headers=headers)

def ext_vector(vector_resp):
    return vector_resp['predicted_value']

def knn_search(vector):
    path = "/{index_name}/_search"
    req = {
        "knn": {
            "field": vector_field,
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector
        },
        "_source": [
            "url",
            "title"
        ]
    }
    headers = {'content-type': 'application/json'}
    return requests.post(es_url + path.format(index_name=index_name), data=json.dumps(req), headers=headers), req

def text_search(query):
    path = "/{index_name}/_search"
    req = {
        "query": {
            "match": {
                text_field: query
            }
        },
        "_source": [
            "url",
            "title"
        ]
    }
    headers = {'content-type': 'application/json'}
    return requests.post(es_url + path.format(index_name=index_name), data=json.dumps(req), headers=headers), req

def hybrid_search(query, vector):
    path = "/{index_name}/_search"
    req = {
        "query": {
            "match": {
                text_field: query
            }
        },
        "knn": {
            "field": vector_field,
            "k": 10,
            "num_candidates": 100,
            "query_vector": vector
        },
        "_source": [
            "url",
            "title"
        ]
    }
    headers = {'content-type': 'application/json'}
    return requests.post(es_url + path.format(index_name=index_name), data=json.dumps(req), headers=headers), req

def render_title_and_url(list):
    template = """
    ## {title}
    url: {url}  
    score: {score}  
    """
    st.markdown("""
    ## total hits : {hits}
    """.format(hits=list['hits']['total']['value']))
    for hit in list['hits']['hits']:
        source = hit['_source']
        st.markdown(template.format(title=source['title'], url=source['url'], score=hit['_score']))

    st.markdown("----")
    
if __name__ == '__main__':
    main()