#!/bin/bash

supervisord -c /etc/supervisor/supervisord.conf

python3 /programa/inicio.py

