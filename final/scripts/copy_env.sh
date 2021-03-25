#!/bin/bash

if [[ -f .env ]]; then
  source .env
else
  echo .env file not found
  exit 1
fi

if [[ -f builds/tests/code/.env ]]; then rm builds/tests/code/.env; fi

cp .env builds/tests/code/

echo '.env file copied to directory with tests'
