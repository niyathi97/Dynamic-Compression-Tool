import mimetypes
import math
from collections import Counter

# Known file signatures (magic bytes)
MAGIC = {
    b"\x1F\x8B": "gzip",
    b"\x42\x5A\x68": "bz2",
    b"\xFD\x37\x7A\x58\x5A\x00": "xz",
    b"\x28\xB5\x2F\xFD": "zstd",
    b"\xFF\xD8\xFF": "jpeg",
    b"\x89PNG\r\n\x1a\n": "png"
}


def magic_type(path):
    """
    Detect file type using magic bytes.
    """
    with open(path, "rb") as f:
        head = f.read(16)

    for magic, filetype in MAGIC.items():
        if head.startswith(magic):
            return filetype

    return None


def sample_stats(path, sample_size=256 * 1024):
    """
    Calculate entropy and text ratio.
    """

    with open(path, "rb") as f:
        data = f.read(sample_size)

    if not data:
        return {
            "entropy": 0,
            "text_ratio": 0,
            "newlines": 0
        }

    total = len(data)

    frequency = Counter(data)

    entropy = -sum(
        (count / total) * math.log2(count / total)
        for count in frequency.values()
    )

    text_chars = sum(
        32 <= byte <= 126 or byte in (9, 10, 13)
        for byte in data
    )

    text_ratio = text_chars / total

    return {
        "entropy": round(entropy, 3),
        "text_ratio": round(text_ratio, 3),
        "newlines": data.count(b"\n")
    }


def guess_mime(path):
    """
    Guess MIME type.
    """

    mime, _ = mimetypes.guess_type(path)

    return mime if mime else "application/octet-stream"