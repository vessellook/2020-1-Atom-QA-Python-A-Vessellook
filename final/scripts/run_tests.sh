#!/bin/bash

main() {
  cd builds/tests/code
  pytest \
     -c="$PROJECT_PATH/builds/tests/code/pytest.ini"\
    --rootdir="$PROJECT_PATH/builds/tests/code" \
    --numprocesses=3 \
    --showlocals \
    --capture=no \
    --verbosity=2 \
    -rA \
    --alluredir="$PROJECT_PATH/mount/allure-results" \
    --clean-alluredir
}

if [[ -f .env ]]; then
  source .env
else
  echo .env file not found
  exit 1
fi

while test $(docker-compose ps | grep -E 'selenoid.*Up' | wc -l) -eq 0; do sleep 5; done
sleep 5

main
