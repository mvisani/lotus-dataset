import os
from typing import Any, Dict, Iterable, List

import pandas as pd
from downloaders import BaseDownloader

from lotus_dataset.settings.dataset_settings import DatasetSettings

from .wikidata import get_lotus_from_query


class Dataset:
    """Class to handle datasets from LOTUS database."""

    def __init__(
        self,
        lotus: pd.DataFrame,
        metadata: Dict[str, Any],
    ):
        self._lotus = lotus
        self._metadata = None

    @staticmethod
    def download(settings: DatasetSettings) -> "Dataset":
        """Build a dataset from the settings."""
        assert isinstance(settings, DatasetSettings)
        downloader = BaseDownloader(
            process_number=1,
            verbose=settings.verbose,
        )

        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objective():
            paths.append(objective.path)
            urls.append(objective.url)

        downloader.download(urls=urls, paths=paths)
        lotus = pd.read_csv(paths[0], engine="pyarrow")

        return Dataset(
            lotus=lotus,
            metadata=settings.into_dict(),
        )

    def load(
        version: str, download_directory: str = "downloads", verbose: bool = True
    ) -> "Dataset":
        """Load the dataset from disk."""

        if verbose:
            settings = (
                DatasetSettings(version=version)
                .set_verbose()
                .set_downloads_directory(download_directory)
            )
        else:
            settings = DatasetSettings(version=version).set_downloads_directory(
                download_directory
            )

        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objective():
            paths.append(objective.path)
            urls.append(objective.url)

        BaseDownloader(
            verbose=verbose,
        ).download(urls=urls, paths=paths)

        lotus = pd.read_csv(paths[0], engine="pyarrow")

        return Dataset(
            lotus=lotus,
            metadata=settings.into_dict(),
        )

    @property
    def dataframe(self) -> pd.DataFrame:
        """Return the LOTUS dataframe."""
        return self._lotus

    @staticmethod
    def get_lotus_from_wikidata() -> pd.DataFrame:
        """Get the LOTUS dataset not from the CSV file but from Wikidata by querying Qlever."""
        return get_lotus_from_query()
