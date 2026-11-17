"""Vérifie le critère d'acceptation T0-2 (sans Jupyter ni matplotlib)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ppg.io import load_rgb_signal, save_red_channel_svg  # noqa: E402


def main() -> int:
    path = ROOT / "tests" / "fixtures" / "sample_ppg_signal.csv"
    signal = load_rgb_signal(path)

    assert len(signal) > 100
    assert signal.duration_s > 25

    print(f"OK T0-2 : {len(signal)} échantillons, durée ≈ {signal.duration_s:.1f} s")
    print(signal.head(3))

    out = ROOT / "data" / "processed" / "t0_2_red_channel.svg"
    save_red_channel_svg(signal, out)
    print(f"Courbe du canal rouge : {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
