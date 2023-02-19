#!/bin/bash

echo "Running isort..."
isort .
echo "-----"

echo "Running black..."
black .
echo "-----"

echo "Running ruff..."
ruff check .
echo "-----"