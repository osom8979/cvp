#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

if ! command -v fc-query &> /dev/null; then
    opm-println-error "Not found fc-query command"
    exit 1
fi

function save_font_ranges
{
    local input="$1"
    local output="${input%%.*}.ranges"

    if [[ -f "$output" ]]; then
        rm -v "$output"
    fi

    local start_hex
    local end_hex

    echo "Generate font range file: '$output'"
    for range in $(fc-query --format "%{charset}" "$input"); do
        if [[ "$range" == *"-"* ]]; then
            IFS="-" read -r start end <<< "$range"
            start_hex=$(printf "0x%06x" "0x$start")
            end_hex=$(printf "0x%06x" "0x$end")
            echo "$start_hex $end_hex" >> "$output"
        else
            single_hex=$(printf "0x%06x" "0x$range")
            echo "$single_hex $single_hex" >> "$output"
        fi
    done
}

for i in "$ROOT_DIR/cvp/assets/fonts/"*.ttf; do
    save_font_ranges "$i"
done
