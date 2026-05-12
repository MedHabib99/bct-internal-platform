#!/bin/bash
# This script recreates all deleted apps

echo "Creating General Info app..."
mkdir -p generalinfo/migrations
mkdir -p templates/generalinfo

echo "Creating Partners app..."
mkdir -p partners/migrations
mkdir -p templates/partners

echo "Creating News app..."
mkdir -p news/migrations
mkdir -p templates/news

echo "Creating Events app..."
mkdir -p events/migrations events/management/commands
mkdir -p templates/events

echo "Done! Now run the Python script to create files."

