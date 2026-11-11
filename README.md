# Mixxx Waveform ZoomOut

An **experimental, unofficial Mixxx 2.6 build** with a much larger waveform zoom-out range.

The project uses [Mixxx's official source code](https://github.com/mixxxdj/mixxx/tree/2.6) and produces an **unsigned Windows x64 installer** using GitHub Actions. No local development tools are required.

## What changes?

- Maximum waveform zoom-out: **10 → 1000** (a finite safety limit, not literally infinite).
- Mouse wheel: normal fine 5% increments through zoom 10, faster 25% increments above 10.
- Initial/default zoom presets remain the original 1–10.
- No changes to the audio engine, track analysis, library/database, cues, playlists, or skins.
- Suitable for testing alongside the custom **LateNight Full Height v6** vertical-waveform skin.

The upstream Mixxx 2.6 source revision is pinned for reproducible builds.

## Build Windows installer

1. Open the [Actions tab](https://github.com/mayuta212/Mixxx-Waveform-ZoomOut/actions).
2. If prompted by GitHub, enable workflows for this repository.
3. Select **Mixxx Waveform ZoomOut - Windows x64**.
4. The first build is configured to run once automatically when the workflow file is added. To rebuild later, choose **Run workflow**.
5. Open the completed run and download the installer from **Artifacts** at the bottom of the page: `mixxx-waveform-zoomout-windows-x64-unsigned`.
6. Extract the artifact ZIP to access the `.msi` installer.

GitHub-hosted runners, not your computer, compile Mixxx. The first build may be slow because the Mixxx dependencies are large. If it fails, inspect the **Build** run logs before retrying.

## Safety and compatibility

**Back up `%LOCALAPPDATA%\Mixxx` before testing**, especially `mixxxdb.sqlite`, keyboard shortcuts, and custom skins. A custom MSI may replace an existing installation; use a separate test environment if possible. Do not test an experimental DJ build during a live performance.

- The installer is **not signed** and may trigger Windows SmartScreen.
- GPU acceleration OFF with RGB waveform is recommended when testing vertical beat grids in the legacy skin because of observed rendering glitches with the accelerated backend.
- High zoom values can hide individual beats or make beat-grid lines overlap. Test progressively (20 → 40 → 80) before using 1000.
- This software has **not yet been verified by an actual Windows build or runtime test**. CI must succeed first.

## Source changes

The script `scripts/patch_zoom.py` applies three exact-match, guarded changes to Mixxx's source:

1. `src/waveform/renderers/waveformwidgetrenderer.cpp`: raise zoom limit.
2. `src/preferences/dialog/dlgprefwaveform.cpp`: keep default zoom dropdown compact.
3. `src/widget/wwaveformviewer.cpp`: accelerate mouse wheel at wide zoom.

If the source files no longer match, the script stops rather than applying an incorrect patch.

Mixxx is open-source software. See the [Mixxx upstream repository](https://github.com/mixxxdj/mixxx) for its source code and license. This repository contains only customization scripts and workflow configuration.
