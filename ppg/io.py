"""Chargement et extraction du signal RGB pour la validation PPG.

Utilise NumPy (obligatoire). Pandas / OpenCV sont optionnels :
utiles plus tard, mais T0-2 fonctionne sans eux.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ppg.config import ROI_FRACTION

RGB_COLUMNS = ("timestamp_ms", "mean_r", "mean_g", "mean_b")


@dataclass
class RgbSignal:
    """Série temporelle des moyennes R, G, B (une ligne = une image)."""

    timestamp_ms: np.ndarray
    mean_r: np.ndarray
    mean_g: np.ndarray
    mean_b: np.ndarray

    def __len__(self) -> int:
        return int(self.timestamp_ms.shape[0])

    @property
    def duration_s(self) -> float:
        if len(self) < 2:
            return 0.0
        return float(self.timestamp_ms[-1] - self.timestamp_ms[0]) / 1000.0

    def head(self, n: int = 5) -> str:
        n = min(n, len(self))
        lines = ["timestamp_ms  mean_r  mean_g  mean_b"]
        for i in range(n):
            lines.append(
                f"{self.timestamp_ms[i]:12.3f}  {self.mean_r[i]:6.2f}  "
                f"{self.mean_g[i]:6.2f}  {self.mean_b[i]:6.2f}"
            )
        return "\n".join(lines)

    def to_csv(self, path: str | Path) -> None:
        path = Path(path)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(RGB_COLUMNS)
            for i in range(len(self)):
                writer.writerow(
                    [
                        f"{self.timestamp_ms[i]:.3f}",
                        f"{self.mean_r[i]:.6f}",
                        f"{self.mean_g[i]:.6f}",
                        f"{self.mean_b[i]:.6f}",
                    ]
                )


def load_rgb_csv(path: str | Path) -> RgbSignal:
    """Charge un CSV au format : timestamp_ms,mean_r,mean_g,mean_b."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV vide ou sans en-tête : {path}")
        missing = [c for c in RGB_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Colonnes manquantes dans {path.name} : {missing}")

        ts, r, g, b = [], [], [], []
        for row in reader:
            ts.append(float(row["timestamp_ms"]))
            r.append(float(row["mean_r"]))
            g.append(float(row["mean_g"]))
            b.append(float(row["mean_b"]))

    if not ts:
        raise ValueError(f"Aucune ligne de données dans {path}")

    return RgbSignal(
        timestamp_ms=np.asarray(ts, dtype=float),
        mean_r=np.asarray(r, dtype=float),
        mean_g=np.asarray(g, dtype=float),
        mean_b=np.asarray(b, dtype=float),
    )


def _central_roi_slices(height: int, width: int, fraction: float = ROI_FRACTION):
    """Découpe une zone centrale (ex. 50 % de chaque dimension)."""
    fh = int(height * fraction)
    fw = int(width * fraction)
    y0 = (height - fh) // 2
    x0 = (width - fw) // 2
    return slice(y0, y0 + fh), slice(x0, x0 + fw)


def extract_rgb_means_from_video(
    path: str | Path,
    *,
    roi_fraction: float = ROI_FRACTION,
) -> RgbSignal:
    """
    Lit une vidéo image par image et calcule les moyennes R, G, B
    sur la zone centrale, avec un horodatage en millisecondes.

    Nécessite opencv-python-headless. Sinon, utilise un CSV.
    """
    try:
        import cv2
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "OpenCV est requis pour lire une vidéo. "
            "Sinon, utilise un CSV (tests/fixtures/)."
        ) from exc

    path = Path(path)
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise FileNotFoundError(f"Impossible d'ouvrir la vidéo : {path}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 1e-3:
        fps = 30.0

    ts, r_vals, g_vals, b_vals = [], [], [], []
    frame_index = 0

    while True:
        ok, frame_bgr = capture.read()
        if not ok:
            break

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w, _ = frame_rgb.shape
        ys, xs = _central_roi_slices(h, w, roi_fraction)
        roi = frame_rgb[ys, xs]
        mean_r, mean_g, mean_b = roi.reshape(-1, 3).mean(axis=0)

        ts.append((frame_index / fps) * 1000.0)
        r_vals.append(float(mean_r))
        g_vals.append(float(mean_g))
        b_vals.append(float(mean_b))
        frame_index += 1

    capture.release()

    if not ts:
        raise ValueError(f"Aucune image lue dans {path}")

    return RgbSignal(
        timestamp_ms=np.asarray(ts, dtype=float),
        mean_r=np.asarray(r_vals, dtype=float),
        mean_g=np.asarray(g_vals, dtype=float),
        mean_b=np.asarray(b_vals, dtype=float),
    )


def load_rgb_signal(path: str | Path) -> RgbSignal:
    """Charge un CSV ou extrait le signal depuis une vidéo."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_rgb_csv(path)
    if suffix in {".mp4", ".avi", ".mov", ".mkv", ".webm"}:
        return extract_rgb_means_from_video(path)
    raise ValueError(f"Extension non supportée ({suffix}). Attendu : .csv ou vidéo.")


def save_red_channel_svg(signal: RgbSignal, path: str | Path, *, width: int = 900, height: int = 320) -> Path:
    """Enregistre une courbe SVG du canal rouge (sans matplotlib)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    t = signal.timestamp_ms / 1000.0
    y = signal.mean_r
    margin_l, margin_r, margin_t, margin_b = 60, 20, 40, 50
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    t_min, t_max = float(t[0]), float(t[-1])
    y_min, y_max = float(np.min(y)), float(np.max(y))
    if y_max <= y_min:
        y_max = y_min + 1.0

    def sx(v: float) -> float:
        return margin_l + (v - t_min) / (t_max - t_min) * plot_w

    def sy(v: float) -> float:
        return margin_t + (1.0 - (v - y_min) / (y_max - y_min)) * plot_h

    # Sous-échantillonner pour un SVG léger
    step = max(1, len(signal) // 800)
    points = " ".join(f"{sx(float(t[i])):.2f},{sy(float(y[i])):.2f}" for i in range(0, len(signal), step))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#F7F9FB"/>
  <text x="{width/2:.0f}" y="24" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#172B3C">Canal rouge (mean_r)</text>
  <line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{height-margin_b}" stroke="#D5DEE6"/>
  <line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#D5DEE6"/>
  <polyline fill="none" stroke="#C62828" stroke-width="1.5" points="{points}"/>
  <text x="{width/2:.0f}" y="{height-12}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5B6B7A">Temps (s)</text>
  <text x="16" y="{height/2:.0f}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#5B6B7A" transform="rotate(-90 16 {height/2:.0f})">mean_r</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")
    return path
