curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "query": "python*",
      "fields": ["title^4", "text^1"]
    }
  }
}
'
