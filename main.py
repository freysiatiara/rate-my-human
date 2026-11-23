#!/usr/bin/env python3
"""Rate My Human: The One-Line Review — entry program.

Reads the review line from entry.txt (stored beside this script) and
copies it, byte for byte, to the gate's output file. Deterministic:
the output bytes are identical on every run, from any working directory.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.txt")


def output_path():
    full_path = os.environ.get("ENTRY_OUTPUT")
    if full_path:
        return full_path
    out_dir = os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.path.isdir("/output"):
        return os.path.join("/output", "entry.txt")
    return os.path.join(HERE, "entry.txt")


def main():
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if os.path.abspath(path) != os.path.abspath(SOURCE):
        shutil.copyfile(SOURCE, path)


if __name__ == "__main__":
    main()
