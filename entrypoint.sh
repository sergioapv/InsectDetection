#!/bin/bash

python ./pestcontrol/manage.py makemigrations
python ./pestcontrol/manage.py migrate
