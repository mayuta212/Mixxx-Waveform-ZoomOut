#!/usr/bin/env python3
"""Apply a guarded Mixxx 2.6 waveform zoom-out customization.

Only three source files are changed. If the pinned upstream revision no longer
matches the expected code, stop rather than silently applying a bad patch.
"""
import argparse
from pathlib import Path

MAX_ZOOM = 1000.0


def replace_exact(root: Path, name: str, old: str, new: str) -> None:
    path = root / name
    content = path.read_text(encoding="utf-8")
    if new in content and old not in content:
        print(f"ALREADY PATCHED: {name}")
        return
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one original match in {name}, got {count}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED: {name}")


def patch(root: Path) -> None:
    replace_exact(
        root,
        "src/waveform/renderers/waveformwidgetrenderer.cpp",
        "const double WaveformWidgetRenderer::s_waveformMaxZoom = 10.0;",
        f"const double WaveformWidgetRenderer::s_waveformMaxZoom = {MAX_ZOOM:.1f};",
    )

    # Keep the Preferences default-zoom dropdown at its original ten entries.
    replace_exact(
        root,
        "src/preferences/dialog/dlgprefwaveform.cpp",
        "i <= static_cast<int>(WaveformWidgetRenderer::s_waveformMaxZoom);",
        "i <= 10; // Keep default zoom presets compact; wheel supports the extended range.",
    )

    # Wheel zoom: normal 5% steps to 10x, faster 25% steps beyond 10x.
    old = """void WWaveformViewer::wheelEvent(QWheelEvent* event) {
    if (m_pWaveformWidget) {
        if (event->angleDelta().y() > 0) {
            onZoomChange(m_pWaveformWidget->getZoom() / 1.05);
        } else if (event->angleDelta().y() < 0) {
            onZoomChange(m_pWaveformWidget->getZoom() * 1.05);
        }
    }
}"""
    new = f"""void WWaveformViewer::wheelEvent(QWheelEvent* event) {{
    if (m_pWaveformWidget) {{
        const double zoom = m_pWaveformWidget->getZoom();
        if (event->angleDelta().y() > 0) {{
            // Zoom in: retain fine steps at 10x and below.
            double nextZoom = zoom > 10.0 ? zoom / 1.25 : zoom / 1.05;
            if (zoom > 10.0 && nextZoom < 10.0) {{
                nextZoom = 10.0;
            }}
            onZoomChange(nextZoom);
        }} else if (event->angleDelta().y() < 0) {{
            // Zoom out: accelerate only in the extended range.
            double nextZoom = zoom * (zoom >= 10.0 ? 1.25 : 1.05);
            if (nextZoom > {MAX_ZOOM:.1f}) {{
                nextZoom = {MAX_ZOOM:.1f};
            }}
            onZoomChange(nextZoom);
        }}
    }}
}}"""
    replace_exact(root, "src/widget/wwaveformviewer.cpp", old, new)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source_dir", type=Path, help="Path to the Mixxx 2.6 source tree")
    args = ap.parse_args()
    patch(args.source_dir.resolve())
    print(f"Waveform zoom-out ready: 1.0 .. {MAX_ZOOM:.1f}")
