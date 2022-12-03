#wget https://dumps.wikimedia.org/enwiki/20221201/enwiki-20221201-pages-articles-multistream1.xml-p1p41242.bz2

#python wikiextractor/WikiExtractor.py -o output -b 10M enwiki-20221201-pages-articles-multistream1.xml-p1p41242.bz2 --json

#ls ./output/AA/* -d | xargs -L 1 -P 10 bash -c './reformat_to_ndjson.py $0'
ls ./output/AA/*_new.ndjson -d | xargs -L 1 bash -c 'echo $0 ; cat $0 | curl -s -X POST -H '\''Content-Type: application/x-ndjson'\'' '\''http://127.0.0.1:9200/wiki/_bulk?pipeline=embedding-pipeline&pretty'\'' --data-binary @-;'
