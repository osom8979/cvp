#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

if ! VERSION=$("$ROOT_DIR/version"); then
    echo "Python code execution failed ($?)" 1>&2
    exit 1
fi

"$ROOT_DIR/python" -m twine upload "${ROOT_DIR}/dist/cvp-${VERSION}-*.whl"
