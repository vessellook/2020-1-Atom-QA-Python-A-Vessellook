#!/bin/bash

main() {
  docker-compose down;
  docker-compose --file tests.docker-compose.yml down;
  [ -d mount ] && sudo rm --recursively --force mount;
  [ -d allure-reports ] && sudo rm --recursively --force allure-reports;
}

main;