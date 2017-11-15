#!/bin/bash

if [ "${TRAVIS_TAG}" == "" ]; then
    echo "Skipping tests because this is not a tagged commit"
else
    py.test -s
    pip freeze | sed -r "s/^-e git.*?egg=([a-z\._]+)$/\1==${TRAVIS_TAG:1}/g" > "${TRAVIS_BUILD_DIR}"/requirements.txt
    cat requirements.txt
fi
