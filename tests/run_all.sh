#!/usr/bin/env bash
# Runs all browser tests of the web page; needs Node.js and Playwright (npm install playwright; npx playwright install chromium).
cd "$(dirname "$0")"; fail=0
for t in tabtest filttest coltest langtest zoomtest plantest2 paneltest othertest mobtest zoompie; do
  printf '%s: ' "$t"; node "$t.js" 2>&1 | tail -1; [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "  FAILED: $t"; fail=1; }
done
exit $fail
