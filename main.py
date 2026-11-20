"""Copy the committed news image to the grader's output path.

The repository holds news.png, drawn by tools/draw_news.py from the verified
headlines of Thursday 19 November 2026. The grader runs this file with no
network; MAKEFUN_OUTPUT_DIR stands in for /output outside the container.
"""
import os
from pathlib import Path

out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
source = Path(__file__).resolve().parent / "news.png"

# Copy the exact bytes: both graded runs must write a byte-identical entry.png.
image = source.read_bytes()
if len(image) > 1024 * 1024:
    raise ValueError("image exceeds the 1 MiB gate")
(out_dir / "entry.png").write_bytes(image)
