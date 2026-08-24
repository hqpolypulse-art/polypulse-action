#!/usr/bin/env bash
set -e

echo "🚀 [PolyPulse] Starting Localization & Visual QA Engine..."

if [ -z "$LOCALIZEPULSE_API_KEY" ]; then
  echo "❌ Error: LOCALIZEPULSE_API_KEY is not set. Please add it to your repository secrets."
  exit 1
fi

python /app/runner.py

echo "✅ [PolyPulse] Execution completed successfully."
