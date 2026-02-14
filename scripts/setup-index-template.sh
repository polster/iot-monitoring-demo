#!/usr/bin/env bash
set -euo pipefail

ELASTIC_URL=${ELASTIC_URL:-http://localhost:9200}
TEMPLATE_NAME=${TEMPLATE_NAME:-iot-events-v1-template}
INDEX_PATTERN=${INDEX_PATTERN:-iot-events-v1-*}
ILM_POLICY=${ILM_POLICY:-logs}

curl -sS -X PUT "${ELASTIC_URL}/_index_template/${TEMPLATE_NAME}" \
  -H 'Content-Type: application/json' \
  -d @- <<EOF
{
  "index_patterns": ["${INDEX_PATTERN}"],
  "data_stream": {},
  "template": {
    "settings": {
      "index.lifecycle.name": "${ILM_POLICY}"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "device_id": { "type": "keyword" },
        "temperature": { "type": "float" },
        "location": { "type": "geo_point" },
        "battery_level": { "type": "float" },
        "status": { "type": "keyword" }
      }
    }
  }
}
EOF

echo
echo "Index template '${TEMPLATE_NAME}' updated at ${ELASTIC_URL}."
