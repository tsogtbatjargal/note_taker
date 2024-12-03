#!/bin/bash

# Enable debug mode
#set -x

set -e # Exit immediately if a command exits with non-zero status.
set -u # Treat unset variables and parameters other than the special parameters "@" and "* as errors.


# Configuration
VAULT_PATH="/mnt/c/someTestTB/ObsidianVault/ObsidianVault"

VAULT_PATH_SUB=$1
# Output file uses this env variable to store
export FABRIC_OUTPUT_PATH="$VAULT_PATH/$VAULT_PATH_SUB"

YOUTUBE_URL=$2
PATTERN=$3
#STUB=$(date +"%Y-%m-%d")-youtube-summary

# Create vault directory if it doesn't exist
mkdir -p "$VAULT_PATH/$VAULT_PATH_SUB"

# Extract transcript
TRANSCRIPT=$(yt --transcript "$YOUTUBE_URL")
if [ $? -ne 0 ]; then
  echo "Failed to extract transcript from YouTube URL: $YOUTUBE_URL"
  exit 1
fi

# Extract duration
DURATION=$(yt --duration "$YOUTUBE_URL")
if [ $? -ne 0 ]; then
  echo "Failed to extract duration from YouTube URL: $YOUTUBE_URL"
  exit 1
fi

# Extract metadata
METADATA=$(yt --metadata "$YOUTUBE_URL")
if [ $? -ne 0 ]; then
  echo "Failed to extract metadata from YouTube URL: $YOUTUBE_URL"
  exit 1
fi

# Extract title from metadata
TITLE=$(echo "$METADATA" | jq -r '.title')
if [ -z "$TITLE" ]; then
  echo "Failed to extract title from metadata."
  exit 1
fi

# Replace spaces with underscores in the title
#TITLE_TAG=$(echo "$TITLE" | sed 's/ /_/g')
TITLE_TAG=$(echo "$TITLE" | sed 's/ /_/g; s/\//-/g; s/\\/-/g') || { echo "Failed to sanitize title"; exit 1; }


# Debug: Print the extracted information to verify
echo "Title for $YOUTUBE_URL: $TITLE"
echo "Duration for $YOUTUBE_URL: $DURATION"
echo "---------------------------------------------------"


# Summarize using Fabric with the llama2:latest model
MODEL="llama2:latest"
SUMMARY=$(echo "$TRANSCRIPT" | fabric --stream --pattern "$PATTERN" --model "$MODEL")
if [ $? -ne 0 ]; then
  echo "Failed to summarize transcript."
  exit 1
fi


# Debug: Print the summary to verify
echo "Summary for $YOUTUBE_URL:"
echo "$SUMMARY"
echo "---------------------------------------------------"

# Save to Obsidian
echo "$SUMMARY" | save --tag youtube --tag transcript --tag duration="$DURATION"_mins --tag "$YOUTUBE_URL" --nofabric --silent "$TITLE_TAG"

# Notify user
echo "Summary saved to $VAULT_PATH/$VAULT_PATH_SUB/$TITLE_TAG.md"