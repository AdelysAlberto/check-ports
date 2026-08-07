#!/usr/bin/env sh
set -e

# Configuración de rutas de instalación
INSTALL_DIR="$HOME/.local/share/check-ports"
BIN_DIR="$HOME/.local/bin"
EXECUTABLE="$BIN_DIR/check-ports"
REPO_URL="https://github.com/AdelysAlberto/check-ports.git"

echo "🛡️  Iniciando instalación automática de CheckPorts..."

# 1. Verificar dependencias del sistema
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Error: Python 3 no está instalado en el sistema."
    exit 1
fi

if ! command -v git >/dev/null 2>&1; then
    echo "❌ Error: git no está instalado en el sistema."
    exit 1
fi

# 2. Descargar o actualizar el repositorio
if [ -d "$INSTALL_DIR" ]; then
    echo "🔄 Actualizando CheckPorts en $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "📦 Clonando repositorio en $INSTALL_DIR..."
    git clone --quiet "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 3. Crear entorno virtual (.venv) e instalar dependencias
echo "🐍 Configurando entorno virtual Python..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv || python3 -m venv --without-pip .venv
fi

if [ ! -f ".venv/bin/pip" ]; then
    curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python3
fi

echo "📥 Instalando dependencias (PyQt5, psutil)..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet PyQt5 psutil

# 4. Crear directorio de binarios de usuario si no existe
mkdir -p "$BIN_DIR"

# 5. Crear el ejecutable lanzador en ~/.local/bin/check-ports
cat << 'EOF' > "$EXECUTABLE"
#!/usr/bin/env sh
INSTALL_DIR="$HOME/.local/share/check-ports"
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    exec .venv/bin/python3 main.py "$@"
else
    echo "❌ Error: CheckPorts no está instalado en $INSTALL_DIR."
    exit 1
fi
EOF

chmod +x "$EXECUTABLE"

# 6. Crear acceso directo .desktop para el menú de aplicaciones de Ubuntu/Linux
DESKTOP_DIR="$HOME/.local/share/applications"
if [ -d "$DESKTOP_DIR" ] || mkdir -p "$DESKTOP_DIR" 2>/dev/null; then
    cat << EOF > "$DESKTOP_DIR/check-ports.desktop"
[Desktop Entry]
Name=CheckPorts
Comment=Inspector & Guard de Puertos y Procesos
Exec=$EXECUTABLE
Terminal=false
Type=Application
Categories=Utility;System;Network;
EOF
fi

echo ""
echo "✅ CheckPorts instalado con éxito!"
echo ""
echo "📌 Para ejecutar la app desde cualquier terminal:"
echo "   check-ports"
echo ""
echo "📌 O búscala en el menú de aplicaciones de tu sistema."
echo ""
