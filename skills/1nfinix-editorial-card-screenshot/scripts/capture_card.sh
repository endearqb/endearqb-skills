#!/bin/bash
# Linux-compatible capture_card.sh (direct screenshot, works with snap Chromium)
# Uses Chromium --screenshot to capture HTML as PNG.
# Usage: capture_card.sh <input.html> <output.png> <ratio>
# Ratios: 3:4 4:3 1:1 16:9 9:16 2.35:1 3:1 5:2

set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <input.html> <output.png> <ratio>" >&2
  echo "Supported ratios: 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, 5:2" >&2
  exit 1
fi

input_path=$1
output_path=$2
ratio_key=$3

case "$ratio_key" in
  "3:4")    vp_width=1500; vp_height=2000 ;;
  "4:3")    vp_width=2000; vp_height=1500 ;;
  "1:1")    vp_width=1800; vp_height=1800 ;;
  "16:9")   vp_width=1920; vp_height=1080 ;;
  "9:16")   vp_width=1080; vp_height=1920 ;;
  "2.35:1") vp_width=2350; vp_height=1000 ;;
  "3:1")    vp_width=1800; vp_height=600 ;;
  "5:2")    vp_width=2500; vp_height=1000 ;;
  *)         echo "Unsupported ratio: $ratio_key" >&2; exit 1 ;;
esac

if [[ -n "${CHROME_BIN:-}" ]]; then
  chrome_bin=$CHROME_BIN
elif [[ -x /snap/bin/chromium ]]; then
  chrome_bin=/snap/bin/chromium
elif [[ -x /usr/bin/chromium-browser ]]; then
  chrome_bin=/usr/bin/chromium-browser
elif [[ -x /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome ]]; then
  chrome_bin=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
else
  echo "Chrome/Chromium binary not found. Set CHROME_BIN env var." >&2
  exit 1
fi

if [[ ! -f "$input_path" ]]; then
  echo "Input HTML not found: $input_path" >&2
  exit 1
fi

mkdir -p "$(dirname "$output_path")"

abs_input=$(cd "$(dirname "$input_path")" && pwd)/$(basename "$input_path")
abs_output=$(cd "$(dirname "$output_path")" && pwd)/$(basename "$output_path")

use_xvfb=false
if command -v xvfb-run &>/dev/null; then
  use_xvfb=true
fi

work_dir="/home/ubuntu"
mkdir -p "$work_dir"
staged_input="${work_dir}/capture_card_input_$$.html"
staged_output="${work_dir}/capture_card_output_$$.png"

cleanup() {
  rm -f "$staged_input" "$staged_output"
}
trap cleanup EXIT

cp "$abs_input" "$staged_input"
input_url="file://${staged_input}"

capture_cmd=(
  "$chrome_bin"
  --headless=new
  --disable-gpu
  --no-sandbox
  --disable-dev-shm-usage
  --hide-scrollbars
  --default-background-color=FFFFFFFF
  --window-size="${vp_width},${vp_height}"
  --force-device-scale-factor=1
  --screenshot="$staged_output"
  "$input_url"
)

if $use_xvfb; then
  xvfb-run -a --server-args="-screen 0 ${vp_width}x${vp_height}x24" \
    "${capture_cmd[@]}" 2>/dev/null
else
  "${capture_cmd[@]}" 2>/dev/null
fi

if [[ ! -f "$staged_output" ]]; then
  echo "Failed to generate output PNG" >&2
  exit 1
fi

mv "$staged_output" "$abs_output"
echo "Saved screenshot to $abs_output"
