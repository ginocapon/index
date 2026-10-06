# -*- coding: utf-8 -*-
"""Alias: rigenera i grafici chart-wrap (vedi rebuild_blog_chart_svg.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rebuild_blog_chart_svg import main  # noqa: E402

if __name__ == "__main__":
    main()
