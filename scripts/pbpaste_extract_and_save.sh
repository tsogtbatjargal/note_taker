#!/bin/bash

# Exit immediately if a command exits with non-zero status.
set -e
# Treat unset variables and parameters other than the special parameters "@" and "* as errors.
set -u

VAULT_PATH="/mnt/c/someTestTB/ObsidianVault/ObsidianVault"


# The first command line argument is the model
MODEL=$1
# The second command line argument is the subdirectory in the vault
VAULT_PATH_SUB=$2

# The third command line argument is the pattern
PATTERN=$3

WEB_URL=$4

# Set the output path environment variable
export FABRIC_OUTPUT_PATH="$VAULT_PATH/$VAULT_PATH_SUB"

# Create the vault subdirectory if it doesn't exist
mkdir -p "$FABRIC_OUTPUT_PATH"

# Read the input data from the clipboard using pbpaste

# Non interactive shell cant use that alias 
#INPUT_DATA=$(pbpaste)
INPUT_DATA=$(xclip -selection clipboard -o)

# Assume the title is on the first line of the input data
TITLE=$(echo "$INPUT_DATA" | head -n 1)
if [ -z "$TITLE" ]; then
  echo "Failed to extract title from metadata."
  exit 1
fi

# Replace spaces with underscores in the title
#TITLE_TAG=$(echo "$TITLE" | sed 's/ /_/g')
TITLE_TAG=$(echo "$TITLE" | sed 's/ /_/g; s/\//-/g; s/\\/-/g') || { echo "Failed to sanitize title"; exit 1; }

echo "Title: $TITLE_TAG"


# Process the input data using the specified pattern
SUMMARY=$(echo "$INPUT_DATA" | fabric --pattern "$PATTERN" --model "$MODEL")

# Save the summary to the specified location
#echo "$SUMMARY" > "$FABRIC_OUTPUT_PATH/"$TITLE_TAG".md"

echo "$SUMMARY" | save --tag web_script --tag "$WEB_URL" --nofabric --silent "$TITLE_TAG"


# Notify the user that the summary has been saved
echo "Summary saved to $FABRIC_OUTPUT_PATH/"$TITLE_TAG".md"
