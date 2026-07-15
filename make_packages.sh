#!/bin/bash
set -e

SRC_DIR="$(pwd)"
VERSION="1.28.0-rc1"
APP_NAME="YTMDPlayer"
DESCRIPTION="Turns the YouTube Music site into a desktop application."
MAINTAINER="deeffest"
LICENSE="GPLv3"
ICON_NAME="ytmdplayer"
INSTALL_PREFIX="/opt/$APP_NAME"
DEB_ARCH="amd64"
RPM_ARCH="x86_64"

DIST_ROOT="$SRC_DIR/${APP_NAME}.dist"
LINUX_SRC_DIR="$DIST_ROOT/${APP_NAME}-v${VERSION}-Linux/$APP_NAME"

if ! command -v fpm &> /dev/null; then
    echo "Error: fpm not found. Install it: https://fpm.readthedocs.io/en/latest/installation.html"
    exit 1
fi

FS_TYPE="$(findmnt -no FSTYPE -T "$SRC_DIR" 2>/dev/null || true)"

cleanup() { [[ -n "${WORK_DIR:-}" ]] && rm -rf "$WORK_DIR"; }
trap cleanup EXIT

if [[ "$FS_TYPE" == "vboxsf" ]]; then
    echo "Detected VirtualBox shared folder, building via /tmp..."
    WORK_DIR="$(mktemp -d /tmp/ytmdplayer_build.XXXXXX)"
    APP_SRC="$WORK_DIR/app"
    mkdir -p "$APP_SRC"
    cp -r "$LINUX_SRC_DIR/"* "$APP_SRC"
    PKG_OUT_DIR="$WORK_DIR"
else
    WORK_DIR="$SRC_DIR/build_pkg_tmp"
    APP_SRC="$LINUX_SRC_DIR"
    PKG_OUT_DIR="$DIST_ROOT"
fi

BUILD_DIR="$WORK_DIR/build_pkg"
DESKTOP_FILE="$BUILD_DIR/usr/share/applications/${APP_NAME}.desktop"
ICON_TARGET="$BUILD_DIR/usr/share/icons/hicolor/512x512/apps/${ICON_NAME}.png"

echo "Preparing build directory..."
mkdir -p "$BUILD_DIR/usr/share/applications" \
         "$BUILD_DIR/usr/share/icons/hicolor/512x512/apps" \
         "$BUILD_DIR$INSTALL_PREFIX"

echo "Copying binaries..."
cp -r "$APP_SRC/"* "$BUILD_DIR$INSTALL_PREFIX"

echo "Setting permissions..."
find "$BUILD_DIR$INSTALL_PREFIX" -type d -exec chmod 755 {} \;
find "$BUILD_DIR$INSTALL_PREFIX" -type f -exec chmod 644 {} \;
while IFS= read -r -d '' file; do
    chmod 755 "$file"
done < <(find "$BUILD_DIR$INSTALL_PREFIX" -type f -print0 | xargs -0 file | grep -E ':.*(ELF|shell script|Python script|executable|script)' | cut -d: -f1 | uniq | tr '\n' '\0')

echo "Adding an icon and desktop file..."
ICON_SOURCE="$APP_SRC/_internal/resources/icons/logo.png"
if [[ ! -f "$ICON_SOURCE" ]]; then
    echo "Error: icon not found at path $ICON_SOURCE"
    exit 1
fi
cp "$ICON_SOURCE" "$ICON_TARGET"
chmod 644 "$ICON_TARGET"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=$APP_NAME
Comment=$DESCRIPTION
Exec=$INSTALL_PREFIX/$APP_NAME
Icon=${ICON_NAME}
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Music;
StartupWMClass=$APP_NAME
EOF

build_pkg() {
    local type="$1" arch="$2"; shift 2
    fpm -s dir -t "$type" \
        -n "$APP_NAME" -v "$VERSION" \
        --license "$LICENSE" --maintainer "$MAINTAINER" \
        --description "$DESCRIPTION" \
        -a "$arch" -p "$PKG_OUT_DIR/${APP_NAME}-v${VERSION}-Linux-${arch}.${type}" \
        "$@" .
}

echo "Creating .deb and .rpm using fpm..."
(
    cd "$BUILD_DIR"
    build_pkg deb "$DEB_ARCH" --category sound --deb-no-default-config-files --deb-compression xz
    build_pkg rpm "$RPM_ARCH" --rpm-os linux --rpm-compression xz
)

if [[ "$FS_TYPE" == "vboxsf" ]]; then
    echo "Copying packages to $DIST_ROOT..."
    cp "$PKG_OUT_DIR/${APP_NAME}-v${VERSION}-Linux-${DEB_ARCH}.deb" \
       "$PKG_OUT_DIR/${APP_NAME}-v${VERSION}-Linux-${RPM_ARCH}.rpm" \
       "$DIST_ROOT/"
fi

echo "Done."
