from engine.base import FHIRMapper

_registry: dict[str, FHIRMapper] = {}

def register(mapper: FHIRMapper) -> None:
    _registry[mapper.resource_type] = mapper

def resolve(resource_type: str) -> FHIRMapper:
    if resource_type not in _registry:
        raise KeyError(f"Recurso '{resource_type}' não suportado")
    return _registry[resource_type]

def registered_resources() -> list[str]:
    return list(_registry.keys())