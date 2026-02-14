#!/usr/bin/env bash
set -euo pipefail

KIBANA_URL=${KIBANA_URL:-http://localhost:5601}
DATA_VIEW_NAME=${DATA_VIEW_NAME:-IoT Events}
DATA_VIEW_TITLE=${DATA_VIEW_TITLE:-iot-events*}
TIME_FIELD=${TIME_FIELD:-@timestamp}

curl -sS -X POST "${KIBANA_URL}/api/data_views/data_view" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d @- <<EOF
{
  "data_view": {
    "title": "${DATA_VIEW_TITLE}",
    "name": "${DATA_VIEW_NAME}",
    "timeFieldName": "${TIME_FIELD}"
  }
}
EOF

echo
echo "Data view '${DATA_VIEW_NAME}' created in Kibana at ${KIBANA_URL}."
