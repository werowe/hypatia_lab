#!/bin/bash
# use ./compile.sh snippets/<file>.c
# then run ./build/<file>
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path/to/program.c"
    exit 1
fi

source_file="$1"

if [ ! -f "$source_file" ]; then
    echo "Error: file not found: $source_file"
    exit 1
fi

case "$source_file" in
    *.c) ;;
    *)
        echo "Error: source file must end in .c"
        exit 1
        ;;
esac

mkdir -p build

program_name="$(basename "$source_file" .c)"
output_file="build/$program_name"

clang \
    -Wall \
    -Wextra \
    -Wpedantic \
    -std=c17 \
    -g \
    "$source_file" \
    -o "$output_file"

echo "Compiled: $source_file"
echo "Created:  $output_file"
echo "Run with: ./$output_file"
