#!/bin/bash

echo "Installing Journal App..."

# Copy executable to local bin
mkdir -p ~/.local/bin
cp dist/Journal ~/.local/bin/Journal
chmod +x ~/.local/bin/Journal

# Create desktop entry
cat > ~/.local/share/applications/journal.desktop << DESKTOP
[Desktop Entry]
Name=Journal
Comment=My personal journal app
Exec=$HOME/.local/bin/Journal
Icon=accessories-text-editor
Terminal=false
Type=Application
Categories=Utility;
DESKTOP

echo "Done! Journal app installed. Look for it in your app menu!"
