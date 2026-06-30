# RPM packaging for the Gprinter GP-1324D CUPS driver (filter + PPD).
# Built by .github/workflows/release-rpm.yml on a `v*` tag push.
#
# rastertotspl is an UPSTREAM PREBUILT x86_64 binary (no source published), so
# this package just places it. Auto dependency generation is disabled because
# the binary was built on Ubuntu and dlopens Ghostscript optionally.

%global debug_package %{nil}
%global __os_install_post %{nil}

Name:           gprinter-1324d-driver
Version:        %{?_version}%{!?_version:1.1.0}
Release:        1%{?dist}
Summary:        CUPS filter and PPD for the Gprinter GP-1324D thermal label printer

License:        MIT
URL:            https://github.com/TheGU/ubuntu_thermal_printer_setup
BuildArch:      x86_64

AutoReqProv:    no
Requires:       cups
Requires:       bluez-cups

Source0:        rastertotspl
Source1:        gprinter_1324D.ppd

%description
Packages the upstream rastertotspl CUPS raster filter and the Gprinter GP-1324D
PPD so the printer works through CUPS on Fedora (e.g. the pack_server Kinoite
image). The PPD's cupsFilter line points at
/usr/lib/cups/filter/rastertotspl, which is where this package installs it.

NOTE (verify on hardware): rastertotspl is a prebuilt x86_64 binary from the
upstream Ubuntu project. It dlopens libgs.so.8/9 (Ghostscript) while Fedora
ships libgs.so.10; the CUPS-raster to TSPL path does not normally invoke
Ghostscript, so it is expected to work, but it must be print-tested on Fedora.
If it fails to load or render, rebuild the filter from source against Fedora's
cups-devel/ghostscript and ship that instead.

%prep
# Sources are single files; nothing to unpack.

%install
install -D -m 0755 %{SOURCE0} %{buildroot}%{_prefix}/lib/cups/filter/rastertotspl
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/cups/model/gprinter-1324d.ppd

%files
%{_prefix}/lib/cups/filter/rastertotspl
%{_datadir}/cups/model/gprinter-1324d.ppd

%changelog
* Tue Jun 30 2026 TheGU <pattapongj@gmail.com> - 1.1.0-1
- Initial RPM packaging of the prebuilt rastertotspl filter and GP-1324D PPD.
