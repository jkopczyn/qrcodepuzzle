#!/bin/bash

# Check if a message is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <message>"
  echo "Example: $0 'HELLO123'"
  exit 1
fi

MESSAGE="$1"
# Start timing
start_time=$(date +%s.%N)

# Function to display elapsed time
show_elapsed_time() {
  local end_time=$(date +%s.%N)
  local elapsed=$(echo "$end_time - $start_time" | bc)
  echo "Elapsed time: $elapsed seconds"
  # Display message length
  echo "Message length: ${#MESSAGE} characters"
}

# Set trap to show timing on script exit
trap show_elapsed_time EXIT

echo "Starting secret to puzzle conversion at $(date)"

# Save the message to a text file
echo "$MESSAGE" > puzzleanswer.txt

# Generate a QR code from the text file
echo "Generating QR code from: $MESSAGE"
qrencode -l L -i -r puzzleanswer.txt -o alphanumeric_puzzle.png

# Display information about the generated image
echo "QR code generated as alphanumeric_puzzle.png"
file alphanumeric_puzzle.png

# Run the image_to_puzzle.py script on the generated image
echo "Converting QR code to puzzle..."
python image_to_puzzle.py alphanumeric_puzzle.png

python make_puzzle_forgiving.py