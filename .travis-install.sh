#!/usr/bin/env sh
python install_requirements.py

if [ "$ES_URL" != 'no' ]; then
    mkdir /tmp/elasticsearch
    wget -O - "$ES_URL" | tar xz --directory=/tmp/elasticsearch --strip-components=1
fi
