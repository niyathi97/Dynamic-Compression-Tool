import gzip
import bz2
import lzma
import zstandard as zstd
import pathlib

from src.strategy import choose_strategy


def calculate_ratio(original_size, compressed_size):
    return round(
        ((original_size - compressed_size) / original_size) * 100,
        2
    )


def compress_file(file_path, mode="auto"):

    plan = choose_strategy(file_path, mode)

    source = pathlib.Path(file_path)

    # STORE ONLY
    if plan.store:
        return {
            "codec": "store",
            "output": file_path,
            "ratio": 0
        }

    # ZSTD
    if plan.codec == "zstd":

        output_file = (
            "compressed_files/" +
            source.name +
            ".zst"
        )

        compressor = zstd.ZstdCompressor(
            level=plan.level
        )

        with open(file_path, "rb") as fin:
            with open(output_file, "wb") as fout:

                compressed = compressor.compress(
                    fin.read()
                )

                fout.write(compressed)

    # GZIP
    elif plan.codec == "gzip":

        output_file = (
            "compressed_files/" +
            source.name +
            ".gz"
        )

        with open(file_path, "rb") as fin:
            with gzip.open(
                output_file,
                "wb",
                compresslevel=plan.level
            ) as fout:

                fout.write(fin.read())

    # BZ2
    elif plan.codec == "bz2":

        output_file = (
            "compressed_files/" +
            source.name +
            ".bz2"
        )

        with open(file_path, "rb") as fin:
            with bz2.open(
                output_file,
                "wb"
            ) as fout:

                fout.write(fin.read())

    # LZMA
    elif plan.codec == "lzma":

        output_file = (
            "compressed_files/" +
            source.name +
            ".xz"
        )

        with open(file_path, "rb") as fin:
            with lzma.open(
                output_file,
                "wb"
            ) as fout:

                fout.write(fin.read())

    else:
        raise ValueError(
            f"Unsupported codec: {plan.codec}"
        )

    original_size = pathlib.Path(
        file_path
    ).stat().st_size

    compressed_size = pathlib.Path(
        output_file
    ).stat().st_size

    ratio = calculate_ratio(
        original_size,
        compressed_size
    )

    return {
        "codec": plan.codec,
        "output": output_file,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "ratio": ratio
    }