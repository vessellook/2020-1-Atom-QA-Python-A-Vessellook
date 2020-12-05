#!/bin/bash
pytest -l -s -vv -rA --clean-alluredir \
       --alluredir=/alluredir \
       -m mixed \
       -n 3 \
       --video-enable
