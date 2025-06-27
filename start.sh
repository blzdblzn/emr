#!/bin/bash

# Start the EMR application
cd /home/ubuntu/emr_system/emr_app
source venv/bin/activate
cd src
python main.py
