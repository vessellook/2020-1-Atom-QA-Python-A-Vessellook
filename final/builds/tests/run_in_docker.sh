#!/bin/bash
pytest --showlocals \
       --capture=no \
       --verbosity=2 \
       -rA \
       --clean-alluredir \
       --alluredir=/alluredir \
       --numprocesses=3

echo 'SELENOID_HOST=selenoid' > override.env
echo 'PROXY_HOST_UI=proxy' >> override.env
echo 'PROXY_HOST_API=proxy' >> override.env
echo 'MOCK_PORT=5000' >> override.env
echo 'MOCK_HOST=mock' >> override.env
echo 'MYSQL_HOST=mysql' >> override.env
echo 'SCREENSHOTS_DIR=/screenshots' >> override.env
echo 'VIDEO_DIR=/video' >> override.env
