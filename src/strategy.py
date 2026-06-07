from dataclasses import dataclass

from src.detector import (
    magic_type,
    sample_stats,
    guess_mime
)


@dataclass
class Plan:
    codec: str
    level: int
    chunk_size: int
    threads: int
    store: bool = False


def choose_strategy(path, mode="auto"):
    """
    Decide best compression strategy.
    """

    detected_type = magic_type(path)

    # Already compressed files
    if detected_type in ["gzip", "bz2", "xz", "zstd"]:
        return Plan(
            codec="store",
            level=0,
            chunk_size=0,
            threads=0,
            store=True
        )

    mime = guess_mime(path)
    stats = sample_stats(path)

    text_file = (
        stats["text_ratio"] > 0.7 and
        stats["entropy"] < 7.7
    )

    # FAST MODE
    if mode == "fast":
        return Plan(
            codec="zstd",
            level=3,
            chunk_size=1024 * 1024,
            threads=1
        )

    # MAX MODE
    if mode == "max":
        return Plan(
            codec="lzma",
            level=7,
            chunk_size=1024 * 1024,
            threads=1
        )

    # Text based files
    if (
        "text" in mime
        or mime == "application/json"
        or mime == "text/csv"
        or text_file
    ):
        return Plan(
            codec="zstd",
            level=8,
            chunk_size=4 * 1024 * 1024,
            threads=2
        )

    # Images and Videos
    if mime.startswith("image/") or mime.startswith("video/"):
        return Plan(
            codec="store",
            level=0,
            chunk_size=0,
            threads=0,
            store=True
        )

    # Binary Files
    return Plan(
        codec="lzma",
        level=6,
        chunk_size=2 * 1024 * 1024,
        threads=1
    )
def explain_strategy(path, mode="auto"):

    mime = guess_mime(path)
    stats = sample_stats(path)

    plan = choose_strategy(path, mode)

    reason = "Default Selection"

    if plan.codec == "zstd":
        reason = "Text-heavy file"

    elif plan.codec == "lzma":
        reason = "Binary file"

    elif plan.codec == "store":
        reason = "Already compressed media"

    return {
        "mime": mime,
        "entropy": stats["entropy"],
        "text_ratio": stats["text_ratio"],
        "codec": plan.codec,
        "level": plan.level,
        "reason": reason
    }