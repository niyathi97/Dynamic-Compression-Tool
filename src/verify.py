import gzip
import bz2
import lzma
import zstandard as zstd
import pathlib


def decompress_file(compressed_file):

    output_dir = pathlib.Path(
        "decompressed_files"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    file_name = pathlib.Path(
        compressed_file
    ).name

    # ZSTD
    if compressed_file.endswith(".zst"):

        output_file = (
            output_dir /
            file_name.replace(".zst", "")
        )

        decompressor = zstd.ZstdDecompressor()

        with open(compressed_file, "rb") as fin:
            compressed_data = fin.read()

        decompressed_data = decompressor.decompress(
            compressed_data
        )

        with open(output_file, "wb") as fout:
            fout.write(decompressed_data)

    # GZIP
    elif compressed_file.endswith(".gz"):

        output_file = (
            output_dir /
            file_name.replace(".gz", "")
        )

        with gzip.open(
            compressed_file,
            "rb"
        ) as fin:

            data = fin.read()

        with open(output_file, "wb") as fout:
            fout.write(data)

    # BZ2
    elif compressed_file.endswith(".bz2"):

        output_file = (
            output_dir /
            file_name.replace(".bz2", "")
        )

        with bz2.open(
            compressed_file,
            "rb"
        ) as fin:

            data = fin.read()

        with open(output_file, "wb") as fout:
            fout.write(data)

    # LZMA
    elif compressed_file.endswith(".xz"):

        output_file = (
            output_dir /
            file_name.replace(".xz", "")
        )

        with lzma.open(
            compressed_file,
            "rb"
        ) as fin:

            data = fin.read()

        with open(output_file, "wb") as fout:
            fout.write(data)

    else:
        raise ValueError(
            "Unsupported file type"
        )

    return str(output_file)

import hashlib


def calculate_sha256(file_path):

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()


def verify_files(original_file, recovered_file):

    original_hash = calculate_sha256(
        original_file
    )

    recovered_hash = calculate_sha256(
        recovered_file
    )

    return (
        original_hash == recovered_hash,
        original_hash,
        recovered_hash
    )