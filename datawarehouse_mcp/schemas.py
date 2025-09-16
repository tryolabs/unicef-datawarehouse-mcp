from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "sse", "streamable-http"]


@dataclass
class Dataflow:
    """Dataflow metadata entry."""

    id: str
    description: str


@dataclass
class ServerConfig:
    """Server configuration settings."""

    host: str
    port: int
    transport: Transport


@dataclass
class Config:
    """Configuration settings."""

    server: ServerConfig
