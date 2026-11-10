#!/bin/sh
# Rebuild everything into public/ (used by npm run build too)
node scripts/build-assets.mjs && npx eleventy --quiet
