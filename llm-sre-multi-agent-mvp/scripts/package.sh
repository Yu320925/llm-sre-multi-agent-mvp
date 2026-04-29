#!/usr/bin/env bash
set -e

PROJECT_NAME="llm-sre-multi-agent-mvp"
ZIP_NAME="${PROJECT_NAME}.zip"

echo "Packaging ${PROJECT_NAME} -> ${ZIP_NAME}"
zip -r "${ZIP_NAME}" . \
  -x "*.git*" \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x ".venv/*" \
  -x "venv/*" \
  -x "*.db" \
  -x "dist/*" \
  -x "build/*"

echo "Done."
