#!/bin/bash

main() {
  cd builds/tests/code
  localhost="127.0.0.1"
  pytest \
    --selenoid-netloc "$localhost:${SELENOID_PORT}" \
    --application-api-netloc "$localhost:${PROXY_PORT}" \
    --application-ui-netloc "${COMPOSE_PROXY_IP_ADDRESS}:80" \
    --mock-netloc "$localhost:${MOCK_PORT}" \
    --mysql-host "$localhost" \
    --mysql-port "${MYSQL_PORT}" \
    --screenshots-dir "$PROJECT_PATH/mount/screenshots" \
    --video-dir "$PROJECT_PATH/mount/videos" \
    --numprocesses=3 \
    --showlocals \
    --capture=no \
    --verbosity=2 \
    -rA \
    --alluredir="$PROJECT_PATH/mount/allure-results" \
    --clean-alluredir
  #    --video-enable
}

if [[ -f .env ]]; then
  source .env
else
  echo .env file not found
  exit 1
fi

main
