#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Mod Steam Grabber.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Mod Steam Grabber.dmg" && rm "dist/Mod Steam Grabber.dmg"
create-dmg \
  --volname "Mod Steam Grabber" \
  --volicon "pic.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Mod Steam Grabber.app" 175 120 \
  --hide-extension "Mod Steam Grabber.app" \
  --app-drop-link 425 120 \
  "dist/Mod Steam Grabber.dmg" \
  "dist/dmg/"