#!/bin/zsh

set -euo pipefail

PROJECT_DIR="/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio"
APP_NAME="Video to MP3 Studio"
APP_PATH="$PROJECT_DIR/dist/$APP_NAME.app"
ICONSET_DIR="$PROJECT_DIR/build/$APP_NAME.iconset"
ICON_PNG="$PROJECT_DIR/assets/icon-1024.png"
ICON_ICNS="$PROJECT_DIR/assets/VideoToMP3Studio.icns"
INSTALL_PATH="$HOME/Applications/$APP_NAME.app"

cd "$PROJECT_DIR"

rm -rf "$APP_PATH" "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

cp "$ICON_PNG" "$ICONSET_DIR/icon_512x512@2x.png"
/usr/bin/sips -z 16 16 "$ICON_PNG" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null
/usr/bin/sips -z 32 32 "$ICON_PNG" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null
/usr/bin/sips -z 32 32 "$ICON_PNG" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null
/usr/bin/sips -z 64 64 "$ICON_PNG" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null
/usr/bin/sips -z 128 128 "$ICON_PNG" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null
/usr/bin/sips -z 256 256 "$ICON_PNG" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null
/usr/bin/sips -z 256 256 "$ICON_PNG" --out "$ICONSET_DIR/icon_256x256.png" >/dev/null
/usr/bin/sips -z 512 512 "$ICON_PNG" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null
/usr/bin/sips -z 512 512 "$ICON_PNG" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null

/usr/bin/iconutil -c icns "$ICONSET_DIR" -o "$ICON_ICNS"
/usr/bin/osacompile -o "$APP_PATH" "$PROJECT_DIR/launcher.applescript"

cp "$ICON_ICNS" "$APP_PATH/Contents/Resources/applet.icns"
PLIST="$APP_PATH/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleIconFile applet" "$PLIST" || /usr/libexec/PlistBuddy -c "Add :CFBundleIconFile string applet" "$PLIST"
/usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier com.leaton79.videotomp3studio.launcher" "$PLIST" || /usr/libexec/PlistBuddy -c "Add :CFBundleIdentifier string com.leaton79.videotomp3studio.launcher" "$PLIST"
/usr/libexec/PlistBuddy -c "Set :CFBundleName $APP_NAME" "$PLIST" || /usr/libexec/PlistBuddy -c "Add :CFBundleName string $APP_NAME" "$PLIST"
/usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $APP_NAME" "$PLIST" || /usr/libexec/PlistBuddy -c "Add :CFBundleDisplayName string $APP_NAME" "$PLIST"

mkdir -p "$HOME/Applications"
rm -rf "$INSTALL_PATH"
cp -R "$APP_PATH" "$INSTALL_PATH"
