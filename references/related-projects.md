# Related projects and acknowledgements

**Special thanks to [Tiy / DoYitNow](https://github.com/DoYitNow/gr-custom-tool)** for
valuable prior work in firmware containers, local research, input provenance, rollback
thinking and filter exploration. This is inspiration, not a claim of collaboration,
endorsement or primacy. This repository is not a fork of those projects.

## Reviewed public snapshots (2026-10-11)

| Project | Scope and license | Snapshot |
|---|---|---|
| [Tiy / DoYitNow — gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool) | GR IV local editor; container/version/rollback/crop/shutdown resources; XMP import, local simulation/software-domain fitting and calibration, optional Windows Lightroom Classic target path and filter-resource writes. Its README says actual Lightroom rendering and device measurements are not completed. Original code/UI/docs GPL-2.0-only. | 549591db6ee7809fa7617c3637296ddc79b34f59 |
| [LiorMoment — Darkslide GR](https://github.com/LiorMoment/darkslide-gr) | GR III 2.10 local icon/name editing, explicitly no color-effect modification; exact official root and independent regeneration/checking workflow. GPL-2.0-only. | 794718a8d8aa1800c1c039ec75ec528970f4cbb8 |
| [idontknownihil — gr3-film-mods](https://github.com/idontknownihil/gr3-film-mods) | GR III image-pipeline research: new entries, matrices/curves/hue sectors, RAW and maker-note identity. Code/notes MIT; container codec submodule GPL-2.0; fitted data by part CC BY-SA / CC BY-NC-SA. | 6326986f23574e65996c8682f2c294ff0b7b0f2d |

Also thanks to LiorMoment for exact-firmware/local verification discipline and to
idontknownihil for important image-pipeline prior work. Each project retains its own
licenses and limitations; functionality may change after these pinned snapshots.

Our closest technical overlap is with gr3-film-mods. Historical mechanisms differ:
our documented namespaces are public 30..35 / processing 26..31 / DNG 0x010C..0x0111,
with their own persistence, Grain and Playback chain. Product form differs: v0.1 is a
coding-agent knowledge/evidence Skill, not a GUI editor, film pack, download site or
production builder. We claim neither first nor only.

## Inspiration ≠ Code Reuse

The available v0.1 review found no bundled source code, binaries or data copied from
these projects. This is not a universal legal determination of authorship. Those
projects remain subject to their own licenses. Any future reuse requires provenance
and license review before inclusion and must comply with the applicable license.
No license conclusion is inferred solely from inspiration, an independent repository
or the lack of a fork relationship.
