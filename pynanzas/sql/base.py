from abc import ABC, abstractmethod


class EsquemaBase(ABC):
    """Clase base abstracta para esquemas de tabla."""

    @abstractmethod
    def obtener_colums(self) -> dict[str, str]:
        """Retorna el diccionario de columnas y sus definiciones SQL."""
        pass

    @abstractmethod
    def obtener_colums_oblig(self) -> list[str]:
        """Retorna lista de columnas que son obligatorias."""
        pass

    def validar_esquema_propio(self, colums_propias: dict[str, str]) -> bool:
        """Valida que un schema personalizado tenga las columnas requeridas."""
        obligatorias = set(self.obtener_colums_oblig())
        propias = set(colums_propias.keys())

        faltantes = obligatorias - propias
        if faltantes:
            raise ValueError(
                f"Faltan columnas requeridas en schema personalizado: {faltantes}"
            )
        return True
