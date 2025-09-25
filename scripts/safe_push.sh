#!/bin/bash
# Safe push script that prevents conflicts

echo "Checking for remote changes..."
git fetch origin

echo "Pulling latest changes with rebase..."
if ! git pull --rebase origin master; then
    echo "ERROR: Failed to rebase. Please resolve conflicts manually."
    exit 1
fi

echo "Pushing changes..."
if git push origin master; then
    echo "✅ Push successful!"
else
    echo "❌ Push failed!"
    exit 1
fi