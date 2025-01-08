%define dracutlibdir %{_prefix}/lib/dracut

Name:      amazon-ec2-utils
Summary:   A set of tools for running in EC2
Version:   2.3.1
Release:   1%{?dist}
License:   MIT
Group:     System Tools
Source:    amazon-ec2-utils.tar.gz
URL:       https://github.com/aws/amazon-ec2-utils
BuildArch: noarch
Provides:  ec2-utils = %{version}-%{release}
Obsoletes: ec2-utils < 2.2
Provides:  ec2-metadata = %{version}-%{release}
Obsoletes: ec2-metadata <= 0.1.3
Requires:  curl
Requires:  nvme-cli >= 1.13
BuildRequires: gzip systemd-rpm-macros
BuildRoot: %{_tmppath}/%{name}-root

%description
amazon-ec2-utils contains a set of utilities for running in EC2.

%prep
%autosetup -c

%build
# compress manpages
gzip -f -9 doc/*.8

%install
# Directories
%{__install} -d -pm 755 %{buildroot}%{_bindir}
%{__install} -d -pm 755 %{buildroot}%{_mandir}/man8
%{__install} -d -pm 755 %{buildroot}%{_sbindir}
%{__install} -d -pm 755 %{buildroot}%{_sysconfdir}/dracut.conf.d
%{__install} -d -pm 755 %{buildroot}%{_sysconfdir}/udev/rules.d
%{__install} -d -pm 755 %{buildroot}%{_udevrulesdir}
%{__install} -d -pm 755 %{buildroot}%{dracutlibdir}/modules.d/96ec2-utils

# Scripts
%{__install} -pm 755 ebsnvme-id %{buildroot}%{_sbindir}/ebsnvme-id
%{__install} -pm 755 ec2-metadata %{buildroot}%{_bindir}/ec2-metadata
%{__install} -pm 755 ec2nvme-nsid %{buildroot}%{_sbindir}/ec2nvme-nsid
%{__install} -pm 755 ec2udev-vbd %{buildroot}%{_sbindir}/ec2udev-vbd

# man pages
%{__install} -pm 644 doc/ebsnvme-id.8.gz %{buildroot}%{_mandir}/man8/ebsnvme-id.8.gz
%{__install} -pm 644 doc/ec2-metadata.8.gz %{buildroot}%{_mandir}/man8/ec2-metadata.8.gz

# udev rules
%{__install} -pm 644 51-ec2-ena-ptp-device.rules %{buildroot}%{_udevrulesdir}/51-ec2-ena-ptp-device.rules
%{__install} -pm 644 51-ec2-hvm-devices.rules %{buildroot}%{_udevrulesdir}/51-ec2-hvm-devices.rules
%{__install} -pm 644 51-ec2-xen-vbd-devices.rules %{buildroot}%{_udevrulesdir}/51-ec2-xen-vbd-devices.rules
%{__install} -pm 644 53-ec2-read-ahead-kb.rules %{buildroot}%{_udevrulesdir}/53-ec2-read-ahead-kb.rules
%{__install} -pm 644 70-ec2-nvme-devices.rules %{buildroot}%{_udevrulesdir}/70-ec2-nvme-devices.rules

# Install 60-cdrom_id.rules to /etc rather than %{_udevrulesdir}
# because it is intended as an override of a systemd-provided rules
# file:
%{__install} -pm 644 60-cdrom_id.rules %{buildroot}%{_sysconfdir}/udev/rules.d/60-cdrom_id.rules

# Dracut module
%{__install} -pm 644 dracut/dracut.conf %{buildroot}%{_sysconfdir}/dracut.conf.d/ec2-utils.conf
%{__install} -pm 755 dracut/module-setup.sh %{buildroot}%{dracutlibdir}/modules.d/96ec2-utils/module-setup.sh

%files
%license LICENSE
%doc README.md
%{_bindir}/ec2-metadata
%{_mandir}/man8/ebsnvme-id.8.gz
%{_mandir}/man8/ec2-metadata.8.gz
%{_sbindir}/ec2nvme-nsid
%{_sbindir}/ebsnvme-id
%{_sbindir}/ec2udev-vbd
%{_udevrulesdir}/51-ec2-ena-ptp-device.rules
%{_udevrulesdir}/51-ec2-hvm-devices.rules
%{_udevrulesdir}/51-ec2-xen-vbd-devices.rules
%{_udevrulesdir}/53-ec2-read-ahead-kb.rules
%{_udevrulesdir}/70-ec2-nvme-devices.rules
%{_sysconfdir}/udev/rules.d/60-cdrom_id.rules

%package dracut
Summary:   Dracut module providing early boot support for EC2 devices
Requires:  amazon-ec2-utils = %{version}-%{release}
Requires:  dracut

%description dracut
This subpackage contains the Dracut module that provides early boot support for EC2
devices, like making EBS NVMe devices have names in /dev that match their EC2 block
device mapping names.

%files dracut
%license LICENSE
%doc README.md
%{_sysconfdir}/dracut.conf.d/ec2-utils.conf
%{dracutlibdir}/modules.d/96ec2-utils/module-setup.sh

%changelog
* Wed Jan 17 2024 Christi Toa <toachris@amazon.com> - 2.3.2-1
- Add support for --availability-zone-id to ec2-metadata

* Thu Dec 19 2024 Keith Gable <gablk@amazon.com> - 2.3.1-1
- Update from upstream (2.2.1)

* Tue Dec 17 2024 Keith Gable <gablk@amazon.com> - 2.2.1-1
- Add support for --aws-domain to ec2-metadata

* Wed May 29 2024 Kuniyuki Iwashima <kuniyu@amazon.com> - 2.2.1
- Add symlink for ENA PTP device.

* Fri Mar 8 2024 Keith Gable <gablk@amazon.com> - 2.3.0-1
- Copy nvme-cli in the Dracut module

* Thu Jan 18 2024 Keith Gable <gablk@amazon.com> - 2.3.0-1
- Rewrite ebsnvme-id in Bash so it is usable in early boot
- Add Dracut module to support block device naming in early boot

* Thu Jan 18 2024 Keith Gable <gablk@amazon.com> - 2.2.0-1
- Corrected issue where an ec2-metadata error was written to stdout
- Change ec2nvme-nsid to use Bash string manipulation to improve
  performance and reliability

* Mon Jun 5 2023 Guillaume Delacour <delacoug@amazon.com> - 2.2.0-1
- Add `--quiet` option to `ec2-metadata --help` output
- Add `-R`/`--region` option to `ec2-metadata` to discover the EC2 instance's region

* Thu Apr  6 2023 Noah Meyerhans <nmeyerha@amazon.com> - 2.1.0-1
- Add --quiet option to ec2-metadata
- Add --partition support to ec2-metadata

* Fri Feb 11 2022 Noah Meyerhans <nmeyerha@amazon.com> 2.0.1-1
- Don't lose NVME symlinks on udev change events

* Thu Jan 20 2022 Noah Meyerhans <nmeyerha@amazon.com> 2.0-1
- Update to 2.0
- Update python dependencies to python3
- Install udev rules to %{_udevrulesdir} rather than a hardcoded /etc/udev
  location.
- Install binaries to %{_sbindir} rather than hardcoded /sbin
- Move ec2nvme-nsid to /usr/sbin rather than /usr/lib/udev
- Drop ec2udev-vpcu and related udev rules
- Fix an invalid substitution in 53-ec2-read-ahead-kb.rules
- Drop the /opt/aws/bin/ec2-metadata symlink

* Wed Nov 17 2021 Noah Meyerhans <nmeyerha@amazon.com> 1.3-5
- Restrict NVME udev rules to "add" events

* Wed Nov 17 2021 Hailey Mothershead <hailmo@amazon.com> 1.3-4
- Add udev rule to increase read_ahead_kb when an NFS share is mounted

* Wed Jul 14 2021 Sai Harsha <ssuryad@amazon.com> 1.3-3
- Disable timeout on EBS volumes

* Thu Oct 29 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-2
- Add testing of python syntax to spec file

* Mon May 18 2020 Suraj Jitindar Singh <surajjs@amazon.com> 1.3-1
- Add udev rule to add by-path links for xen vbd devices

* Tue Apr 28 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-1
- Rename the project to amazon-ec2-utils
- Add README file

* Tue Feb 25 2020 Frederick Lefebvre <fredlef@amazon.com> 1.2-1
- Fix output of multi-line fields

* Wed Jan 15 2020 Frederick Lefebvre <fredlef@amazon.com> 1.1-1
- Add IMDSv2 support

* Tue Aug 27 2019 Anchal Agarwal <anchalag@amazon.com> 1.0-2
- Add udev rule to define lower timeout for instance storage volumes

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
