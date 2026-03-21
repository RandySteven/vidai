import os
import tomllib
from functools import lru_cache
from pathlib import Path


def _default_service_toml_path() -> Path:
    return Path(__file__).resolve().parent.parent / "toml" / "service-config.local.toml"


def service_config_path() -> Path:
    """Path to TOML config; override with VIDAI_SERVICE_CONFIG_PATH for CI or containers."""
    override = os.environ.get("VIDAI_SERVICE_CONFIG_PATH", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return _default_service_toml_path()


@lru_cache
def load_service_config() -> dict:
    path = service_config_path()
    with open(path, "rb") as f:
        return tomllib.load(f)


def reload_service_config() -> dict:
    """Clear cache after swapping config files at runtime (e.g. tests)."""
    load_service_config.cache_clear()
    return load_service_config()
