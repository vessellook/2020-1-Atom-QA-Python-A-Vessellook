#!/bin/bash
pytest --showlocals \
       --capture=no \
       --verbosity=2 \
       -rA \
       --clean-alluredir \
       --alluredir=/alluredir \
       --numprocesses=3 \
       --video-enable
