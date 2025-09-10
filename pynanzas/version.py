from pathlib import Path
import tomllib

from packaging.version import Version


def _read_from_toml() -> str:
    """Siempre lee la versión desde pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text())
    return data["project"]["version"]


__version__ = _read_from_toml()

_ver = Version(__version__)
__version_num__ = _ver.major * 10000 + _ver.minor * 100 + _ver.micro
VERSION_DB = _ver.major * 10 + _ver.minor * 1

