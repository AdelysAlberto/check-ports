# Especificación UX/UI & Arquitectura de Interfaz Nativa
## System: Ubuntu Port Guard & Inspector (PySide6 Desktop UI)

> *"¡Nunca miro hacia atrás, querido, me distrae del presente! ¡Sin capas! Una interfaz debe ser impoluta, funcional y sencillamente fabulosa."* — **Edna Moda**

---

## 🎨 1. Concepto Visual & Filosofía de Diseño

- **Estilo**: Dark Mode sobrio e industrial (*Ubuntu Slate & Neon Accent*).
- **Estructura**: Distribución asimétrica de 2 columnas principales (*Split-View Master-Detail*).
- **Ergonomía**: Cero distracciones, cero capas innecesarias. Todo la información crítica accesible a un solo clic.

---

## 📐 2. Layout & Wireframe de la Pantalla Principal

```text
+-----------------------------------------------------------------------------------------------+
| 🛡️ UBUNTU PORT GUARD & INSPECTOR                  [🔍 Buscar puerto/PID...] [🔄 Refrescar]    |
+---------------------------------------------------+-------------------------------------------+
| COLUMNA IZQUIERDA (Lista Master - 35% Ancho)      | COLUMNA DERECHA (Detalle Extendido - 65%) |
|                                                   |                                           |
| 🟢 PUERTOS COMUNES DE UBUNTU (Sistema)            | 📌 PUERTO SELECCIONADO: TCP/8080          |
| ├─ [TCP 22]   sshd           (127.0.0.1)         | ----------------------------------------- |
| ├─ [UDP 53]   systemd-resolv (127.0.0.53)        | ⚙️ INFORMACIÓN DEL PROCESO                |
| └─ [TCP 631]  cupsd          (127.0.0.1)         | • Nombre:      node                       |
|                                                   | • PID:         14582                      |
| 🟠 PUERTOS NO COMUNES / APLICACIONES              | • Ruta:        /usr/bin/node              |
| ├─ [TCP 3000] node (Web App)                      | • Usuario:     adalbeca                   |
| ├─ [TCP 5432] postgres                            | • Comando:     node server.js --port 8080 |
| └─ [TCP 8080] python3                             |                                           |
|                                                   | 📚 CONOCIMIENTO Y DESCRIPCIÓN LOCAL       |
|                                                   | [Categoría: Puerto No Común / Web Server] |
|                                                   | "Servidor HTTP alternativo comúnmente     |
|                                                   | usado por entornos Node.js / Tomcat."     |
|                                                   |                                           |
|                                                   | ⚡ ACCIONES RÁPIDAS                        |
|                                                   | [ 🛑 Matar Proceso (SIGKILL) ]           |
|                                                   | [ 📋 Copiar Info ] [ 🔍 Ver en /proc ]    |
+---------------------------------------------------+-------------------------------------------+
| Status: 12 puertos abiertos (4 Sistema, 8 Apps) | Auto-refresco: [5s v]  | Permisos: Normal |
+-----------------------------------------------------------------------------------------------+
```

---

## ⚡ 3. Componentes Visuales & Comportamiento

1. **Barra Superior (Header Panel)**:
   - Título de la aplicación con icono distintivo.
   - Caja de búsqueda en tiempo real que filtra al escribir por número de puerto, nombre de servicio o ejecutable.
   - Botón de refresco manual instantáneo con micro-animación de rotación.

2. **Columna Izquierda (Master Tree / List View)**:
   - Sección colapsable 1: **Puertos Comunes de Ubuntu** (Insignia verde `[SISTEMA]`).
   - Sección colapsable 2: **Puertos No Comunes / Apps** (Insignia naranja/azul `[USUARIO/DEV]`).
   - Cada elemento muestra: Puerto, Protocolo (TCP/UDP), Nombre del proceso y badge distintivo.
   - Resaltado activo evidente al seleccionar un elemento.

3. **Columna Derecha (Detail Panel)**:
   - Tarjeta superior con datos del proceso del sistema en tiempo real.
   - Tarjeta de Base de Conocimiento (Knowledge Base Card): Información contextual extraída del diccionario local `ports_knowledge.json`.
   - Panel de Acciones con botones destacados:
     - `Matar Proceso` (Color rojo de peligro, diálogo modal de confirmación).
     - `Copiar Info` (Copia resumen técnico al portapapeles).
