#!/bin/bash

# Install python module
sudo python setup.py install

# Install systemd unit
sudo cp envmon.service /etc/systemd/system
sudo chmod 664 /etc/systemd/system/envmon.service

# Reload systemd units
sudo systemctl daemon-reload

