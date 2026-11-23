#!/usr/bin/env python3
"""Rate My Human: The One-Line Review — entry program.

Reads the review line from entry.txt (stored beside this script) and
copies it, byte for byte, to the gate's output file. The copy is
crash-safe: the bytes land in a temporary file in the destination
directory first and are then moved into place with an atomic rename,
so the output file is never observed half-written. Deterministic:
the output bytes are identical on every run, from any working directory.
"""
import os
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.txt")


def output_path():
    full_path = os.environ.get("ENTRY_OUTPUT")
    if full_path:
        return full_path
    out_dir = os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return os.path.join("/output", "entry.txt")


def main():
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if os.path.abspath(path) == os.path.abspath(SOURCE):
        return
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    fd, tmp_path = tempfile.mkstemp(dir=parent or ".", prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        # mkstemp creates the staging file with mode 0600; the rename would
        # keep those permissions, so widen them explicitly before publishing
        # — the final output file must be readable by the grader (0644).
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
