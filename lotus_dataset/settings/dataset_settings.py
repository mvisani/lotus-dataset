"""Submodule providing the settings for constructing versions of the LOTUS dataset."""

import os
from typing import Any, Dict, List

import compress_json

from lotus_dataset.exceptions import UnavailableEntry, VersionException
from lotus_dataset.utils.download_objective import DownloadObjective


class DatasetSettings:
    """Class defining the settings for constructing versions of the LOTUS dataset."""

    def __init__(self, version: str):
        local_version_path = os.path.join(
            os.path.dirname(__file__), "versions", f"{version}.json"
        )

        if not os.path.exists(local_version_path):
            available_versions = os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
            raise VersionException(version, available_versions)

        self._version_metadata: Dict[str, Any] = compress_json.load(local_version_path)
        self._verbose: bool = False
        self._to_include: List[str] = ["url"]
        self._downloads_directory: str = "downloads"

    @staticmethod
    def available_versions() -> List[str]:
        """Return the available versions of the dataset."""
        return [
            version.replace(".json", "")
            for version in os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
        ]

    def download_objective(self) -> List[DownloadObjective]:
        """Return the download objectives."""
        download_objectives: List[DownloadObjective] = []
        for included in self._to_include:
            url = self._version_metadata[included]
            file_name = url.split("/")[-1]
            path = os.path.join(
                self._downloads_directory,
                file_name,
            )
            download_objectives.append(DownloadObjective(path, url))

        return download_objectives

    def into_dict(self) -> Dict[str, Any]:
        """Return the settings as a dictionary."""
        return {
            "version": self._version_metadata,
            "verbose": self._verbose,
            "to_include": self._to_include,
            "downloads_directory": self._downloads_directory,
        }

    def set_downloads_directory(self, downloads_directory: str) -> "DatasetSettings":
        """Set the downloads directory."""
        self._downloads_directory = downloads_directory
        return self

    @property
    def verbose(self) -> bool:
        """Return the verbosity of the settings."""
        return self._verbose

    def set_verbose(self) -> "DatasetSettings":
        """Sets to verbose mode."""
        self._verbose = True
        return self
