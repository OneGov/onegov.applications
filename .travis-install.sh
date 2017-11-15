#!/bin/bash
if [ "${TRAVIS_TAG}" == "" ]; then
    echo "Skipping tests because this is not a tagged commit"
else
    python install_requirements.py
fi
