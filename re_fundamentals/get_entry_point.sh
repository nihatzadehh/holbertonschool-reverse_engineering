#!/bin/bash
#
# get_entry_point.sh
#
# Extracts and displays ELF header information (Magic Number, Class,
# Byte Order, Entry Point Address) for a given ELF binary.
#
# Usage: ./get_entry_point.sh <path_to_elf_file>

# Load the reusable display function (relative path, no hardcoding)
script_dir="$(dirname "$0")"
source "$script_dir/messages.sh"

file_name="$1"

# 1. Accept the ELF file name as a command-line argument
if [ -z "$file_name" ]; then
    echo "Usage: $0 <ELF_file>"
    exit 1
fi

# 2. Check if the file exists
if [ ! -e "$file_name" ]; then
    echo "Error: File '$file_name' does not exist."
    exit 1
fi

if [ ! -f "$file_name" ]; then
    echo "Error: '$file_name' is not a regular file."
    exit 1
fi

# 3. Validate that the file is a genuine ELF file using readelf.
#    readelf fails with a non-zero exit status and prints an error
#    message to stderr if the file is not an ELF binary.
if ! readelf -h "$file_name" &>/dev/null; then
    echo "Error: '$file_name' is not a valid ELF file."
    exit 1
fi

# 4. Extract the required data using readelf
header_info="$(readelf -h "$file_name")"

magic_number="$(echo "$header_info" | grep "Magic:" | sed 's/.*Magic:[[:space:]]*//' | sed 's/[[:space:]]*$//')"
class="$(echo "$header_info" | grep "Class:" | awk '{print $2}')"
byte_order="$(echo "$header_info" | grep "Data:" | awk -F', ' '{print $2}')"
entry_point_address="$(echo "$header_info" | grep "Entry point address:" | awk '{print $NF}')"

# 5. Use messages.sh to format and display the output
display_elf_header_info
