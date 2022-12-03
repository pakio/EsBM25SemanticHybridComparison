
# start Elasticsearch and kibana
docker-compose up -d

until curl -i localhost:9200 | grep "200 OK"
  do
    sleep 5
  done

# start trial
curl -X POST 'http://127.0.0.1:9200/_license/start_trial?acknowledge=true'

# import model
eland_import_hub_model --url http://127.0.0.1:9200 --hub-model-id sentence-transformers/msmarco-MiniLM-L-12-v3 --task-type text_embedding

curl -H 'Content-Type: application/json' -X PUT 'http://127.0.0.1:9200/wiki?pretty' -d @mapping.json
curl -H 'Content-Type: application/json' -X PUT 'http://127.0.0.1:9200/_ingest/pipeline/embedding-pipeline' -d @embedding-pipeline.json
curl -X POST 'http://127.0.0.1:9200/_ml/trained_models/sentence-transformers__msmarco-minilm-l-12-v3/deployment/_start'
