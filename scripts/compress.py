import argparse
import pathlib
import subprocess

from datasus_raw_fetcher import meta


def compress_files_by_year(dirpath: pathlib.Path, destdirpath: pathlib.Path):
    years = {int(f.name[:4]) for f in dirpath.iterdir()}
    for year in years:
        dest_filepath = destdirpath / f"{year}.7z"
        if dest_filepath.exists():
            continue
        if not dest_filepath.parent.exists():
            dest_filepath.parent.mkdir(parents=True)
        subprocess.run(
            [
                "7z",
                "a",
                "-t7z",
                "-m0=lzma2",
                "-mx=9",
                "-aoa",
                "-mfb=64",
                "-md=32m",
                "-ms=on",
                "-mhe",
                str(dest_filepath),
                f"{dirpath}/{year}*.dbc",
            ],
        )


def get_parser():
    parser = argparse.ArgumentParser(
        description="Compress all raw files in the given directory"
    )
    parser.add_argument(
        "dirpath",
        type=pathlib.Path,
        help="Directory to compress",
    )
    parser.add_argument(
        "destdirpath",
        type=pathlib.Path,
        help="Directory to store compressed files",
    )
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    dirpath = args.dirpath
    destdirpath = args.destdirpath
    for dataset in meta.datasets:
        dirpath = dirpath / dataset
        destdirpath = destdirpath / dataset
        compress_files_by_year(dirpath, destdirpath)
