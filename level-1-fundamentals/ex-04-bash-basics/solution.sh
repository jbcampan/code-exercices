#!/bin/bash
set -e

# Display help/usage information and exit
usage() {
    echo "Usage: $0 <directory> <extension>  (e.g. $0 ./data .log)" >&2
    echo "Provide a directory to scan and the file extension to search for." >&2
    exit 1
}

# Verify that the provided path exists and is a directory
check_dir() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        echo "Error: '$dir' is not a valid directory." >&2
        exit 1
    fi
}

# Analyze files matching the requested extension
analyze() {
    local dir="$1"
    local ext="$2"

    echo "Analyzed directory : $dir"
    echo "Extension          : $ext"
    echo ""

    local files
    files=$(find "$dir" -maxdepth 1 -name "*$ext" -type f)

    if [ -z "$files" ]; then
        echo "No files found."
        exit 0
    fi

    echo "Files found:"
    echo "$files" | while read -r f; do
        echo "  $(basename "$f")"
    done

    local count
    count=$(echo "$files" | wc -l | tr -d ' ')

    local size
    size=$(echo "$files" | xargs du -ch | tail -1 | cut -f1)

    echo ""
    echo "Total: $count file(s)"
    echo "Size : $size"
}

# Optional: ask user confirmation before proceeding with a destructive action
confirm() {
    local prompt="$1"
    read -r -p "$prompt [y/N] " answer
    case "$answer" in
        [yY]) return 0 ;;
        *)    return 1 ;;
    esac
}

# Delete files matching the requested extension
delete_files() {
    local dir="$1"
    local ext="$2"

    local files
    files=$(find "$dir" -maxdepth 1 -name "*$ext" -type f)

    if [ -z "$files" ]; then
        echo "No files to delete."
        exit 0
    fi

    if confirm "Delete all $ext files in $dir?"; then
        echo "$files" | xargs rm
        echo "Deleted."
    else
        echo "Aborted." >&2
        exit 1
    fi
}

# ---- Entry point ----
[ "$#" -lt 2 ] && usage

check_dir "$1"
analyze "$1" "$2"

if [ "${3:-}" = "--delete" ]; then
    delete_files "$1" "$2"
fi