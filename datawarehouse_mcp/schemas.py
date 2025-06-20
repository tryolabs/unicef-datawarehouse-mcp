from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "sse", "streamable-http"]


@dataclass
class ServerConfig:
    """Server configuration settings."""

    port: int
    transport: Transport


@dataclass
class Config:
    """Configuration settings."""

    server: ServerConfig
