#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

if ! VERSION=$("$ROOT_DIR/version"); then
    echo "Python code execution failed ($?)" 1>&2
    exit 1
fi

NAME="cvp"
TAG="$NAME:$VERSION"
LATEST="$NAME:latest"

if ! docker build -f "$ROOT_DIR/Dockerfile" --tag "$TAG" "$ROOT_DIR"; then
    echo "Dockerfile build failed ($?)" 1>&2
    exit 1
fi

docker tag "$TAG" "$LATEST"
