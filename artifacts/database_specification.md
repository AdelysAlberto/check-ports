# Especificación de Datos & Base de Conocimientos Local
## System: Ubuntu Port Inspector (`ports_knowledge.json`)

> *"¡Santo Cielos! Almacenar la información de los puertos en un archivo JSON en memoria nos da una velocidad de respuesta a 88 millas por hora, ¡sin latencia de red! ¡1.21 Gigawatts de eficiencia!"* — **Doc Brown**

---

## 💾 1. Esquema JSON de la Base de Conocimiento (`data/ports_knowledge.json`)

```json
{
  "version": "1.0.0",
  "updated_at": "2026-08-07",
  "common_ubuntu_ports": [22, 53, 80, 443, 631, 5353],
  "ports_dictionary": {
    "22": {
      "port": 22,
      "protocol": "TCP",
      "service": "SSH (Secure Shell)",
      "category": "common_ubuntu",
      "is_common": true,
      "summary": "Servicio de acceso remoto seguro a la consola de Ubuntu.",
      "description": "Utilizado por OpenSSH para permitir inicios de sesión remotos cifrados y transferencia de archivos SCP/SFTP.",
      "risk_level": "BAJO",
      "recommendations": "Mantener actualizado OpenSSH Server y deshabilitar autenticación por contraseña si es expuesto públicamente."
    },
    "53": {
      "port": 53,
      "protocol": "TCP/UDP",
      "service": "DNS (Domain Name System)",
      "category": "common_ubuntu",
      "is_common": true,
      "summary": "Resolución de nombres de dominio en Linux.",
      "description": "Utilizado por systemd-resolved o BIND9 para traducir nombres de dominio en direcciones IP.",
      "risk_level": "BAJO",
      "recommendations": "Esencial para la conectividad del sistema."
    },
    "80": {
      "port": 80,
      "protocol": "TCP",
      "service": "HTTP",
      "category": "common_ubuntu",
      "is_common": true,
      "summary": "Servidor web sin cifrado.",
      "description": "Puerto estándar para servidores web Apache2, NGINX o Lighttpd sirviendo páginas HTTP.",
      "risk_level": "MEDIO",
      "recommendations": "Redirigir todo el tráfico a HTTPS (puerto 443)."
    },
    "443": {
      "port": 443,
      "protocol": "TCP",
      "service": "HTTPS",
      "category": "common_ubuntu",
      "is_common": true,
      "summary": "Servidor web cifrado SSL/TLS.",
      "description": "Puerto seguro predeterminado para servidores web NGINX, Apache, Traefik o Caddy.",
      "risk_level": "BAJO",
      "recommendations": "Asegurar certificados TLS válidos (Let's Encrypt)."
    },
    "631": {
      "port": 631,
      "protocol": "TCP/UDP",
      "service": "CUPS (Common Unix Printing System)",
      "category": "common_ubuntu",
      "is_common": true,
      "summary": "Sistema de impresión de Ubuntu.",
      "description": "Gestor de colas de impresión y detección de impresoras en la red local de Ubuntu.",
      "risk_level": "BAJO",
      "recommendations": "Desactivar si el equipo no utiliza impresoras."
    },
    "3000": {
      "port": 3000,
      "protocol": "TCP",
      "service": "Node.js / React / Dev Server",
      "category": "custom_app",
      "is_common": false,
      "summary": "Puerto alternativo habitual en desarrollo web.",
      "description": "Usado frecuentemente por aplicaciones React, Express, Next.js, Ruby on Rails o Grafana.",
      "risk_level": "MEDIO",
      "recommendations": "Verificar qué proceso local está escuchando si no estás desarrollando actualmente."
    },
    "5432": {
      "port": 5432,
      "protocol": "TCP",
      "service": "PostgreSQL Database",
      "category": "custom_app",
      "is_common": false,
      "summary": "Servidor de base de datos PostgreSQL.",
      "description": "Puerto por defecto del sistema gestor de base de datos relacional PostgreSQL.",
      "risk_level": "MEDIO",
      "recommendations": "Verificar `pg_hba.conf` para restringir el acceso solo a `localhost` (127.0.0.1)."
    },
    "8080": {
      "port": 8080,
      "protocol": "TCP",
      "service": "HTTP Alternate / Tomcat / Spring",
      "category": "custom_app",
      "is_common": false,
      "summary": "Servidor web secundario o proxy.",
      "description": "Comúnmente utilizado por Java Tomcat, Spring Boot, Jenkins, Vue dev server o proxies de depuración.",
      "risk_level": "MEDIO",
      "recommendations": "Revisar la aplicación asociada y la autenticación activa."
    }
  }
}
```

---

## ⚡ 2. Estrategia de Carga y Búsqueda O(1)

- Al iniciar la aplicación, el módulo `knowledge_base.py` lee `ports_knowledge.json` y construye un diccionario hash en memoria Python `dict[int, PortMetadata]`.
- Al detectar un puerto `N`, se realiza la búsqueda `dict.get(N)` instantánea (tiempo constante $O(1)$).
- Si el puerto `N` no está en la base de conocimientos, se genera dinámicamente un objeto de reserva (*fallback object*) categorizándolo como `"custom_app"` (Puerto No Común).
