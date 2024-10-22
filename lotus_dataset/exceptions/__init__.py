"""Submodule defining exceptions used across the LOTUS database."""

from lotus_dataset.exceptions.unavailable_entry import UnavailableEntry
from lotus_dataset.exceptions.version_exception import VersionException

__all__ = [
    "UnavailableEntry",
    "VersionException",
]
