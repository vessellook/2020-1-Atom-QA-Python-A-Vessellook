#!/bin/bash

main() {
  docker-compose down;
  docker-compose --file tests.docker-compose.yml down;
  [ -d mount ] && sudo rm --recursively --force mount;
  [ -d allure-reports ] && sudo rm --recursively --force allure-reports;
}

if [[ -f .env ]]; then
  source .env;
else
  echo .env file not found;
  exit 1;
fi

main;