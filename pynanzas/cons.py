import os
from pathlib import Path
import tomllib

from packaging.version import Version

TEST = False

try:
    dir_base: Path = Path(__file__).resolve().parent.parent
except NameError:
    dir_base = Path(os.getcwd()).resolve().parent

if not (dir_base / "pynanzas").exists():
    dir_actual = Path(os.getcwd()).resolve()
    while dir_actual != dir_actual.parent:
        if (dir_actual / "pynanzas").exists():
            dir_base = dir_actual
            break
        dir_actual = dir_actual.parent

DIR_BASE: Path = dir_base
DIR_DATA: Path = DIR_BASE / "data"
DIR_BACKUP: Path = DIR_DATA / "backup"

def _read_from_toml() -> str:
    pyproject_path = DIR_BASE / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text())
    return data["project"]["version"]


__version__ = Version(_read_from_toml())

__version_num__ = __version__.major * 10000 + __version__.minor * 100 + __version__.micro