#!/usr/bin/env python3
import os
import re

import colorsys

def darken(hex_color: str, factor: float = 0.7) -> str:
    """
    Darken a hex color by multiplying its lightness in HLS space.
    factor < 1 -> darker, factor > 1 -> lighter
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Convert to HLS
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Darken lightness
    l = max(0, min(1, l * factor))
    
    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

# Hardcoded accent colors
accent = "#cb7012"
accent_bg = darken(accent, 0.9)

# ------------------ Update sway/config ------------------
xdg_config_home = os.path.expanduser("~/.config")
sway_config_path = os.path.join(xdg_config_home, "sway", "config")

# Prepare lines
accent_line = f"set $accent {accent_bg}\n"
accent_bg_line = f"set $accent_bg {accent}\n"

# Read file if it exists
if os.path.exists(sway_config_path):
    with open(sway_config_path, "r") as f:
        lines = f.readlines()
else:
    lines = []

# Remove any old definitions
lines = [line for line in lines if not re.match(r"^\s*set\s+\$(accent|accent_bg)\b", line)]

# Insert new lines at the top
lines = [accent_line, accent_bg_line, "\n"] + lines

# Ensure sway config dir exists
os.makedirs(os.path.dirname(sway_config_path), exist_ok=True)

# Write back
with open(sway_config_path, "w") as f:
    f.writelines(lines)

print(f"✅ Wrote $accent={accent}, $accent_bg={accent_bg} at the top of {sway_config_path}")

# ------------------ Update Waybar accent.css ------------------
waybar_css_path = os.path.join(xdg_config_home, "waybar", "accent.css")

if os.path.exists(waybar_css_path):
    with open(waybar_css_path, "r") as f:
        css_lines = f.readlines()
else:
    css_lines = []

# Replace color lines in CSS (only the color property)
new_css_lines = []
color_pattern = re.compile(r"^\s*color\s*:\s*#([0-9A-Fa-f]{6});")
for line in css_lines:
    if color_pattern.match(line):
        new_css_lines.append(f"    color: {accent};\n")
    else:
        new_css_lines.append(line)

# Ensure Waybar config dir exists
os.makedirs(os.path.dirname(waybar_css_path), exist_ok=True)

# Write updated CSS
with open(waybar_css_path, "w") as f:
    f.writelines(new_css_lines)

print(f"✅ Updated Waybar color to {accent} in {waybar_css_path}")

# ------------------ Update Rofi colors.rasi ------------------
rofi_rasi_path = "~/.config/rofi/shared/colors.rasi"

if os.path.exists(rofi_rasi_path):
    with open(rofi_rasi_path, "r") as f:
        rasi_lines = f.readlines()
else:
    rasi_lines = []

# Replace the selected line
new_rasi_lines = []
selected_pattern = re.compile(r"^\s*selected\s*:\s*#[0-9A-Fa-f]{6,8};")
for line in rasi_lines:
    if selected_pattern.match(line):
        new_rasi_lines.append(f"    selected:     {accent};\n")
    else:
        new_rasi_lines.append(line)

# Ensure rofi theme dir exists
os.makedirs(os.path.dirname(rofi_rasi_path), exist_ok=True)

# Write updated Rasi theme
with open(rofi_rasi_path, "w") as f:
    f.writelines(new_rasi_lines)

print(f"✅ Updated Rofi selected to {accent} in {rofi_rasi_path}")
