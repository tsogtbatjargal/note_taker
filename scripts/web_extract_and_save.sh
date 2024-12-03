#!/bin/bash

# Enable debugging
set -x

# Exit immediately if a command exits with a non-zero status.
set -e

# Treat unset variables and parameters other than the special parameters "@" and "* as errors.
set -u

# Adjust PATH
export PATH="/home/tsogounix/.local/bin:$PATH"

# Configuration
VAULT_PATH="/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

# Command line arguments
MODEL=$1               # The model (e.g., "llama2:latest")
VAULT_PATH_SUB=$2      # The subdirectory in the vault
PATTERN=$3             # The pattern (e.g., "summarize" or "extract_wisdom")
WEB_URL=${4:-""}       # The web page URL (optional)

# Set the output path environment variable
export FABRIC_OUTPUT_PATH="$VAULT_PATH/$VAULT_PATH_SUB"

# Create the vault subdirectory if it doesn't exist
mkdir -p "$FABRIC_OUTPUT_PATH"

# Read input data from stdin
INPUT_DATA=$(cat)

# Remove lines containing unwanted patterns
INPUT_DATA=$(echo "$INPUT_DATA" | grep -v -e 'Please figure out the best possible answer' -e 'Important: Reward for correct answer')

# Remove leading empty or whitespace-only lines
INPUT_DATA=$(echo "$INPUT_DATA" | sed '/^\s*$/d')

# Check if input data is empty
if [ -z "$INPUT_DATA" ]; then
  echo "No input data received."
  exit 1
fi

# Improved title generation
# Extract the most meaningful line for the title
TITLE=$(echo "$INPUT_DATA" | grep -E '^.{20,}' | head -n 1)

# If no meaningful line is found, fallback to the web URL domain
if [ -z "$TITLE" ] && [ -n "$WEB_URL" ]; then
  TITLE=$(echo "$WEB_URL" | awk -F'/' '{print $3}' | sed 's/www\.//')
fi

# Fallback to a generic title if still no title is found
if [ -z "$TITLE" ]; then
  TITLE="note"
fi

# Sanitize the title
TITLE_TAG=$(echo "$TITLE" |
  sed -E 's/[^a-zA-Z0-9 _-]//g' |  # Remove special characters
  tr ' ' '_' |                     # Replace spaces with underscores
  cut -c 1-50 |                    # Truncate to 50 characters
  tr '[:upper:]' '[:lower:]')      # Convert to lowercase


echo "Generated Title: $TITLE_TAG"

# Use absolute paths for commands (if needed)
FABRIC_CMD="/home/tsogounix/.local/bin/fabric"
SAVE_CMD="/home/tsogounix/.local/bin/save"

# Process the input data using the specified pattern
SUMMARY=$(echo "$INPUT_DATA" | "$FABRIC_CMD" --pattern "$PATTERN" --model "$MODEL")

# Check if the fabric command was successful
if [ $? -ne 0 ]; then
  echo "Error processing input with fabric:"
  echo "$SUMMARY"
  exit 1
fi


# Save the summary to the specified location
if [ -n "$WEB_URL" ]; then
  echo "$SUMMARY" | "$SAVE_CMD" --tag web_script --tag "$WEB_URL" --tag "$PATTERN" --nofabric --silent "$TITLE_TAG"
else
  echo "$SUMMARY" | "$SAVE_CMD" --tag web_script --tag "$PATTERN" --nofabric --silent "$TITLE_TAG"
fi

# Notify the user that the summary has been saved
echo "Summary saved to $FABRIC_OUTPUT_PATH/$TITLE_TAG.md"

# Output the summary to stdout for the Streamlit app to capture
echo "$SUMMARY"
