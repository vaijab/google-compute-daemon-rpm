# define upstream specific release versions
%global         upstream_source_name google-daemon
%global         upstream_release 1
%global         upstream_pkg_release 3

Name:           google-compute-daemon
Version:        1.1.0
Release:        1%{?dist}
Summary:        Google Compute Engine instance daemon

Group:          System Environment/Base
License:        Apache Software License
URL:            https://github.com/GoogleCloudPlatform/compute-image-packages/tree/master/google-daemon
Source0:        https://github.com/GoogleCloudPlatform/compute-image-packages/releases/download/%{version}.%{upstream_release}/%{upstream_source_name}-%{version}-%{upstream_pkg_release}.tar.gz
Source1:        google-accounts-manager.service
Source2:        google-address-manager.service

BuildArch:      noarch

BuildRequires:  systemd
Requires:       python
Requires:       policycoreutils
Requires:       shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd


%description
A service that manages user accounts, maintains ssh login keys, and syncs
public endpoint IP addresses.


%prep
%setup -q -n %{upstream_source_name}


%build


%install
# Install daemon files
mkdir -p -m 0755 %{buildroot}%{_datarootdir}/google
cp -rp usr/share/google/* %{buildroot}%{_datarootdir}/google

# Install systemd units
mkdir -p %{buildroot}%{_unitdir}
cp -p %{SOURCE1} %{buildroot}%{_unitdir}
cp -p %{SOURCE2} %{buildroot}%{_unitdir}

# Install docs
mkdir -p -m 0755 %{buildroot}%{_defaultdocdir}/%{name}
cp README.md %{buildroot}%{_defaultdocdir}/%{name}


%clean

%post
%systemd_post google-accounts-manager.service
%systemd_post google-address-manager.service

%preun
%systemd_preun google-accounts-manager.service
%systemd_preun google-address-manager.service

%postun
%systemd_postun_with_restart google-accounts-manager.service
%systemd_postun_with_restart google-address-manager.service


%files
%doc README.md
%{_unitdir}/google-accounts-manager.service
%{_unitdir}/google-address-manager.service
%{_datarootdir}/google/*


%changelog
* Tue Jan 21 2014 Vaidas Jablonskis <jablonskis@gmail.com> - 1.1.0-1
- Initial build
