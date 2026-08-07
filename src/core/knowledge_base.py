"""
Knowledge Base Engine Module
Carga el diccionario local data/ports_knowledge.json y enriquece los datos de los puertos escaneados.
"""

import json
import os
from typing import Dict, List, Any
from src.models.port_model import PortInfo, ProcessDetail
from src.utils.result import Result


class KnowledgeBase:
    """Motor de consulta y enriquecimiento de información de puertos."""

    def __init__(self, json_path: str = "data/ports_knowledge.json"):
        self.json_path = json_path
        self.common_ports = set()
        self.ports_dict: Dict[str, Dict[str, Any]] = {}
        self.is_loaded = False

    def load(self) -> Result[bool, str]:
        """Carga el archivo JSON de base de conocimientos en memoria."""
        if not os.path.exists(self.json_path):
            return Result.fail(f"No se encontró el archivo de base de conocimiento en {self.json_path}")
        
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.common_ports = set(data.get("common_ubuntu_ports", []))
            self.ports_dict = data.get("ports_dictionary", {})
            self.is_loaded = True
            return Result.ok(True)
        except Exception as e:
            return Result.fail(f"Error al leer la base de conocimiento JSON: {str(e)}")

    def enrich_port(self, raw_data: dict) -> PortInfo:
        """
        Enriquece los datos brutos de un puerto con la información del diccionario local.
        Si el puerto no está en la base de datos, genera una descripción genérica adecuada.
        """
        port = raw_data["port"]
        protocol = raw_data["protocol"]
        status = raw_data["status"]
        ip_address = raw_data["ip_address"]
        proc_detail: ProcessDetail = raw_data["process"]

        port_str = str(port)
        known_info = self.ports_dict.get(port_str)

        if known_info:
            is_common = known_info.get("is_common", port in self.common_ports)
            service_name = known_info.get("service", proc_detail.name if proc_detail else "Desconocido")
            summary = known_info.get("summary", "Servicio sin resumen específico.")
            description = known_info.get("description", "Sin descripción registrada.")
            risk_level = known_info.get("risk_level", "MEDIO")
            recommendations = known_info.get("recommendations", "Inspeccionar el proceso activo.")
        else:
            is_common = port in self.common_ports
            proc_name = proc_detail.name if proc_detail else "Proceso Desconocido"
            service_name = f"{proc_name} (Puerto Custom {port})"
            
            if is_common:
                summary = "Puerto Estándar de Sistema Linux"
                description = f"Puerto {port} comúnmente reservado para servicios del sistema operativo."
                risk_level = "BAJO"
                recommendations = "Servicio estándar de sistema."
            else:
                summary = "Puerto Personalizado / Aplicación de Usuario"
                description = f"El puerto {port} está siendo utilizado por el ejecutable '{proc_name}'. No figura en el catálogo de puertos comunes por defecto."
                risk_level = "MEDIO"
                recommendations = "Verificar si corresponde a una aplicación o entorno de desarrollo en uso."

        return PortInfo(
            port=port,
            protocol=protocol,
            status=status,
            ip_address=ip_address,
            process=proc_detail,
            is_common=is_common,
            service_name=service_name,
            summary=summary,
            description=description,
            risk_level=risk_level,
            recommendations=recommendations
        )

    def enrich_all(self, raw_ports_list: List[dict]) -> List[PortInfo]:
        """Enriquece una lista de puertos brutos escaneados."""
        if not self.is_loaded:
            self.load()
        return [self.enrich_port(raw) for raw in raw_ports_list]
