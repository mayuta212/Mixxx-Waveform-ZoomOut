# Mixxx Waveform ZoomOut

Unofficial, experimental Mixxx builds with a much larger waveform zoom-out range, offered in **two separate versions**: the official **2.5.6 stable** release and **2.6 beta**.

The project uses [Mixxx's official source code](https://github.com/mixxxdj/mixxx/tree/2.6) and produces an **unsigned Windows x64 installer** using GitHub Actions. No local development tools are required.

## What changes?

- Maximum waveform zoom-out: **10 → 1000** (a finite safety limit, not literally infinite).
- Mouse wheel: normal fine 5% increments through zoom 10, faster 25% increments above 10.
- Initial/default zoom presets remain the original 1–10.
- No changes to the audio engine, track analysis, library/database, cues, playlists, or skins.
- Suitable for testing alongside the custom **LateNight Full Height v6** vertical-waveform skin.

Both upstream source revisions are pinned to exact commits for reproducible builds.

## Choose a version

| Version | Base | Workflow | Installer artifact |
| --- | --- | --- | --- |
| **2.5.6 Stable ZoomOut** | Mixxx 2.5.6 official release | `build-windows-stable-2_5_6.yml` | `mixxx-2.5.6-stable-waveform-zoomout-win64-unsigned` |
| **2.6 Beta ZoomOut** | Mixxx 2.6 beta branch | `build-windows.yml` | `mixxx-waveform-zoomout-windows-x64-unsigned` |

The stable-based build uses its own source patch at `scripts/patch_zoom_2_5_6.py`; the beta build uses `scripts/patch_zoom.py`. Neither build changes or replaces the source of the other.

## Build Windows installer

1. Open the [Actions tab](https://github.com/mayuta212/Mixxx-Waveform-ZoomOut/actions).
2. If prompted by GitHub, enable workflows for this repository.
3. Select **Mixxx 2.5.6 Stable ZoomOut - Windows x64** or **Mixxx Waveform ZoomOut - Windows x64** (2.6).
4. The first build is configured to run once automatically when the workflow file is added. To rebuild later, choose **Run workflow**.
5. Open the completed run and download the appropriate ZIP from **Artifacts** at the bottom of the page, using the artifact names in the table above.
6. Extract the artifact ZIP to access the `.msi` installer.

GitHub-hosted runners, not your computer, compile Mixxx. The first build may be slow because the Mixxx dependencies are large. If it fails, inspect the **Build** run logs before retrying.

## Safety and compatibility

**Back up `%LOCALAPPDATA%\Mixxx` before testing**, especially `mixxxdb.sqlite`, keyboard shortcuts, and custom skins. A custom MSI may replace an existing installation; use a separate test environment if possible. Do not test an experimental DJ build during a live performance.

- The installer is **not signed** and may trigger Windows SmartScreen.
- GPU acceleration OFF with RGB waveform is recommended when testing vertical beat grids in the legacy skin because of observed rendering glitches with the accelerated backend.
- High zoom values can hide individual beats or make beat-grid lines overlap. Test progressively (20 → 40 → 80) before using 1000.
- This software has **not yet been verified by an actual Windows build or runtime test**. CI must succeed first.

## Source changes

The scripts `scripts/patch_zoom.py` (2.6) and `scripts/patch_zoom_2_5_6.py` (2.5.6) apply three exact-match, guarded changes to their corresponding Mixxx sources:

1. `src/waveform/renderers/waveformwidgetrenderer.cpp`: raise zoom limit.
2. `src/preferences/dialog/dlgprefwaveform.cpp`: keep default zoom dropdown compact.
3. `src/widget/wwaveformviewer.cpp`: accelerate mouse wheel at wide zoom.

If the source files no longer match, the script stops rather than applying an incorrect patch.

Mixxx is open-source software. See the [Mixxx upstream repository](https://github.com/mixxxdj/mixxx) for its source code and license. This repository contains only customization scripts and workflow configuration.
