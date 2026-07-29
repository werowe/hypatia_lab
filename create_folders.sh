#!/bin/bash

set -e

categories=(
    "data_types:DATA_TYPES.md"
    "operators:OPERATORS.md"
    "conditionals:CONDITIONALS.md"
    "loops:LOOPS.md"
    "functions:FUNCTIONS.md"
    "arrays:ARRAYS.md"
    "strings:STRINGS.md"
    "pointers:POINTERS.md"
    "structs:STRUCTS.md"
    "memory:MEMORY.md"
    "bits:BITS.md"
    "registers:REGISTERS.md"
    "electronics:ELECTRONICS.md"
    "arduino:ARDUINO.md"
    "projects:PROJECTS.md"
    "snippets:SNIPPETS.md"
)

for entry in "${categories[@]}"; do
    folder="${entry%%:*}"
    markdown_file="${entry##*:}"

    mkdir -p "$folder"

    if [ ! -e "$folder/$markdown_file" ]; then
        title="${markdown_file%.md}"
        title="${title//_/ }"

        cat > "$folder/$markdown_file" <<EOF
# $title

## Concepts

Add explanations of the main concepts here.

## Programs

Add a list of the example programs in this folder.

## Compile

\`\`\`bash
clang -Wall -Wextra -Wpedantic -std=c17 source.c -o program
\`\`\`

## Run

\`\`\`bash
./program
\`\`\`
EOF

        echo "Created $folder/$markdown_file"
    else
        echo "Kept existing $folder/$markdown_file"
    fi
done

mkdir -p build

echo
echo "Folder structure created successfully."
echo "Existing folders and source-code files were not removed."
