#!/usr/bin/env python3
"""Summarize byte-level entropy without displaying file content."""

import argparse
import math
from pathlib import Path
import stat
import sys


MAX_BYTES = 512 * 1024 * 1024
READ_SIZE = 64 * 1024


class InputError(ValueError):
    pass


def inspect(path):
    source = Path(path)
    file_stat = source.stat()
    if not stat.S_ISREG(file_stat.st_mode):
        raise InputError("input must be a regular file")
    if file_stat.st_size > MAX_BYTES:
        raise InputError("input exceeds the 512 MiB limit")

    counts = [0] * 256
    size = printable = 0
    with source.open("rb") as stream:
        while True:
            block = stream.read(READ_SIZE)
            if not block:
                break
            size += len(block)
            if size > MAX_BYTES:
                raise InputError("input grew beyond the 512 MiB limit while reading")
            printable += sum(1 for byte in block if 32 <= byte <= 126)
            for byte in block:
                counts[byte] += 1

    distinct = sum(count > 0 for count in counts)
    # ponytail: whole-file entropy hides local patterns; add windows only if localization matters.
    entropy = -sum((count / size) * math.log2(count / size) for count in counts if count) if size else None
    common_share = max(counts, default=0) / size if size else None
    printable_share = printable / size if size else None
    return size, distinct, entropy, printable_share, common_share


def main():
    parser = argparse.ArgumentParser(description="Estimate Shannon byte entropy without printing file data.")
    parser.add_argument("input", help="regular file to inspect")
    args = parser.parse_args()

    try:
        size, distinct, entropy, printable, common = inspect(args.input)
    except InputError as error:
        print(f"entropy-peek: unsupported input: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"entropy-peek: {error.strerror or 'unable to read input'}", file=sys.stderr)
        return 2

    print(f"Bytes: {size}")
    print(f"Distinct byte values: {distinct} / 256")
    if entropy is None:
        print("Shannon byte entropy: unavailable (empty file)")
        print("Printable ASCII: unavailable")
        print("Most common byte share: unavailable")
    else:
        print(f"Shannon byte entropy: {entropy:.4f} bits/byte")
        print(f"Printable ASCII: {printable:.1%}")
        print(f"Most common byte share: {common:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
