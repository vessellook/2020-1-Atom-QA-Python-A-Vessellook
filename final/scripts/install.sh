#!/bin/bash
mkdir --parents mount/allure-results mount/myapp mount/mysql/data mount/mysql/init \
                mount/selenoid mount/videos mount/screenshots
cp --force --no-clobber configs/app_config mount/myapp/config
cp --force --no-clobber configs/init_query.sql mount/mysql/init/init_query.sql
cp --force --no-clobber configs/browsers.json mount/selenoid/browsers.json
if ! test `stat -c "%a" mount/mysql/data` -eq 777; then
  sudo chmod 777 mount/mysql/data;
fi;