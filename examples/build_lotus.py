import argparse

from tqdm.auto import tqdm

from lotus_dataset import Dataset, DatasetSettings


def build_lotus(version: str) -> Dataset:
    settings = DatasetSettings(version=version).set_verbose()
    return Dataset.download(settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a version of LOTUS.")
    parser.add_argument(
        "version",
        type=str,
        help="The version of the LOTUS to build.",
    )
    args = parser.parse_args()

    if args.version == "all":
        versions = DatasetSettings.available_versions()
    else:
        versions = [args.version]

    for v in tqdm(
        versions,
        desc="Building LOTUS",
        unit="version",
        disable=len(versions) == 1,
    ):
        _dataset: Dataset = build_lotus(v)
