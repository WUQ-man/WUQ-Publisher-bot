#!/usr/bin/env bash
# build.sh

# Install Python 3.11.9 using pyenv (which is pre-installed on Render)
pyenv install 3.11.9 -s
# Set the local Python version for this project
pyenv local 3.11.9

# Then proceed with your normal build steps
pip install -r requirements.txt
