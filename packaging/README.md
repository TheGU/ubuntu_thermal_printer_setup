# Fedora RPM packaging

This packages the existing `rastertotspl` filter + `gprinter_1324D.ppd` into a
Fedora RPM so an immutable host (Fedora Kinoite / bootc) can `dnf install` the
driver into `/usr` instead of copying loose files. Consumed by the `pack_server`
build (`image/Containerfile`).

## What it installs
- `/usr/lib/cups/filter/rastertotspl` (mode 0755)
- `/usr/share/cups/model/gprinter-1324d.ppd` (mode 0644)

These match the paths `pack_server`'s `phases/60-devices.sh` expects and the
PPD's own `*cupsFilter:` line.

## Cut a release
```
git tag v1.1.0
git push origin v1.1.0
```
The `Release gprinter RPM` workflow builds in a `fedora:43` container and attaches
`gprinter-1324d-driver-1.1.0-1.fc43.x86_64.rpm` to the release. The version comes
from the tag (`v1.1.0` -> `1.1.0`); the `.fc43` comes from the build container.

`pack_server` pins that exact URL in `image/Containerfile` (`GPRINTER_RPM_URL`).
Bump the tag and the build container's Fedora version together on a Fedora
upgrade, then bump the URL in `pack_server`.

## Known risk (prebuilt binary)
`rastertotspl` is an upstream **prebuilt Ubuntu 20.04 x86_64 binary** (stripped,
no source published). The RPM only packages it - it does not rebuild it. Its hard
library deps (`libc`, `libcups.so.2`, `libcrypt.so.1`, `libdl`) are satisfiable
on Fedora. It also references `libgs.so.8/9` (Ghostscript) via `dlopen`, while
Fedora ships `libgs.so.10`; the CUPS-raster to TSPL path does not normally call
Ghostscript, so it is expected to work - but **print-test on Fedora hardware**.
If the filter fails to load/render, the fix is to obtain `rastertotspl` source and
rebuild it against Fedora's `cups-devel`/`ghostscript`, then ship that binary.
