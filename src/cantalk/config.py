"""Config loader for cantalk.yaml."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class CantalkConfig:
    """Parsed cantalk configuration."""

    name: str = "cantalk"
    version: str = "0.1.0"
    vad: dict = field(default_factory=dict)
    stt: dict = field(default_factory=dict)
    llm: dict = field(default_factory=dict)
    tts: dict = field(default_factory=dict)
    server: dict = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path = "cantalk.yaml") -> "CantalkConfig":
        """Load config from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, path: str | Path) -> None:
        """Save config to a YAML file."""
        with open(path, "w") as f:
            yaml.dump(self.__dict__, f, allow_unicode=True, default_flow_style=False)
