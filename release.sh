#!/usr/bin/env sh
# Helper para publicar una nueva release / tag en GitHub

set -e

if [ -z "$1" ]; then
    echo "Uso: ./release.sh <version> [mensaje]"
    echo "Ejemplo: ./release.sh 1.0.1 \"Corrección de compatibilidad en macOS\""
    exit 1
fi

VERSION="$1"
# Asegurar formato vX.Y.Z
if [ "${VERSION#v}" = "$VERSION" ]; then
    TAG="v$VERSION"
else
    TAG="$VERSION"
    VERSION="${VERSION#v}"
fi

MSG="${2:-Release $TAG}"

echo "📦 Preparando Release $TAG..."

# Actualizar src/version.py
cat << EOF > src/version.py
"""
Version & Release Configuration
"""

__version__ = "$VERSION"
GITHUB_REPO = "AdelysAlberto/check-ports"
GITHUB_API_RELEASES = "https://api.github.com/repos/AdelysAlberto/check-ports/releases/latest"
GITHUB_API_TAGS = "https://api.github.com/repos/AdelysAlberto/check-ports/tags"
EOF

echo "📝 src/version.py actualizado a $VERSION"

git add src/version.py
git commit -m "chore(release): $TAG" || true
git tag -a "$TAG" -m "$MSG"

echo ""
echo "✅ Tag $TAG creado localmente."
echo "🚀 Para publicar la release en GitHub, ejecuta:"
echo "   git push origin main --tags"
