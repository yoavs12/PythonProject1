from json import JSONDecodeError
from pathlib import Path
from typing import Dict
import json

from virus import ConfigException


def load_config(config_path: Path) -> Dict:
    if config_path.exists():
        config_file_content = config_path.read_text()
    else:
        raise ConfigException(f"Config file, at path: {config_path.absolute()} does not exist!")
    try:
        parsed_config_file_content = json.loads(config_file_content)
    except JSONDecodeError:
        raise ConfigException(f"Invalid JSON at {config_path.absolute()} ")
    return parsed_config_file_content
