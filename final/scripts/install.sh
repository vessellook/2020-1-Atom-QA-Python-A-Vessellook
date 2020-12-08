#!/bin/bash

if [[ -f .env ]]; then
  source .env
else
  echo .env file not found
  exit 1
fi

mkdir --parents mount/allure-results mount/myapp mount/mysql/init \
                mount/selenoid mount/videos mount/screenshots
mkdir --mode 777 mount/mysql/data 

echo 'mount/ directory structure  created'

cp --force --no-clobber configs/app_config mount/myapp/config
cp --force --no-clobber configs/init_query.sql mount/mysql/init/init_query.sql
cp --force --no-clobber configs/browsers.json mount/selenoid/browsers.json

echo 'configs copied'

./scripts/copy_env.sh
