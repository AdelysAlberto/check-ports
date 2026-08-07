# Plan de Sprint & Desglose de Tareas 1 a 1
## System: Ubuntu Port Inspector

> *"Todo perfectamente alienado, ordenado y desglosado paso por paso."* — **Adrian Monk**

---

## 📋 Tareas Ejecutables Paso a Paso (Sprint 1)

1. **TASK-01**: Crear archivo de base de conocimientos local `data/ports_knowledge.json` con catálogo de puertos de Ubuntu y desarrollo.
2. **TASK-02**: Crear utilitarios y modelos de datos `src/models/port_model.py` y `src/utils/result.py`.
3. **TASK-03**: Crear el motor de escaneo de puertos de sistema `src/core/scanner.py` e integración con `psutil`.
4. **TASK-04**: Crear el motor de consulta y enriquecimiento `src/core/knowledge_base.py`.
5. **TASK-05**: Crear el gestor de terminación de procesos `src/core/process_manager.py` con escudo contra PIDs protegidos.
6. **TASK-06**: Crear cargador de estilos QSS `src/ui/styles.py` e integrar la paleta de colores.
7. **TASK-07**: Desarrollar la columna izquierda `src/ui/port_list_widget.py` con árbol de puertos comunes vs no comunes y barra de búsqueda.
8. **TASK-08**: Desarrollar la columna derecha `src/ui/port_detail_widget.py` con datos extendidos del proceso y botones de acción.
9. **TASK-09**: Ensamblar la ventana principal `src/ui/main_window.py` y el punto de entrada `main.py`.
10. **TASK-10**: Ejecutar y validar la aplicación nativa en Ubuntu Linux.
