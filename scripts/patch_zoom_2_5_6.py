#!/usr/bin/env python3
"""Apply an exact-match, idempotent zoom-out patch to official Mixxx 2.5.6."""
import argparse
from pathlib import Path

MAX_ZOOM = 1000.0


def replace_exact(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    content = path.read_text(encoding="utf-8")
    if new in content and old not in content:
        print(f"ALREADY PATCHED: {relative}")
        return
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one original match in {relative}, got {count}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED: {relative}")


def patch(root: Path) -> None:
    replace_exact(
        root,
        "src/waveform/renderers/waveformwidgetrenderer.cpp",
        "const double WaveformWidgetRenderer::s_waveformMaxZoom = 10.0;",
        f"const double WaveformWidgetRenderer::s_waveformMaxZoom = {MAX_ZOOM:.1f};",
    )

    replace_exact(
        root,
        "src/preferences/dialog/dlgprefwaveform.cpp",
        "i <= static_cast<int>(WaveformWidgetRenderer::s_waveformMaxZoom);",
        "i <= 10; // Keep default zoom presets compact; wheel supports the extended range.",
    )

    # 2.5.6 uses m_waveformWidget/getZoomFactor, unlike the 2.6 branch.
    original = """void WWaveformViewer::wheelEvent(QWheelEvent* event) {
    if (m_waveformWidget) {
        if (event->angleDelta().y() > 0) {
            onZoomChange(m_waveformWidget->getZoomFactor() / 1.05);
        } else if (event->angleDelta().y() < 0) {
            onZoomChange(m_waveformWidget->getZoomFactor() * 1.05);
        }
    }
}"""
    replacement = f"""void WWaveformViewer::wheelEvent(QWheelEvent* event) {{
    if (m_waveformWidget) {{
        const double zoom = m_waveformWidget->getZoomFactor();
        if (event->angleDelta().y() > 0) {{
            // Zoom in: fine steps through 10x, faster steps above 10x.
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
    replace_exact(root, "src/widget/wwaveformviewer.cpp", original, replacement)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()
    patch(args.source_dir.resolve())
    print(f"Mixxx 2.5.6 ZoomOut ready: 1.0 .. {MAX_ZOOM:.1f}")
