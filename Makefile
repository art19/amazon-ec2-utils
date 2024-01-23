RPM_BUILD_DIR = $(shell mktemp -d /tmp/amazon-linux-utils.rpm-XXXXXXXX)

.PHONY: rpm
rpm:
	git archive --format=tar HEAD > amazon-ec2-utils.tar
	gzip -f -9 amazon-ec2-utils.tar
	rpmbuild --define "%_topdir $(RPM_BUILD_DIR)" -ta amazon-ec2-utils.tar.gz -v
	cp -fv $(RPM_BUILD_DIR)/RPMS/*.rpm $(RPM_BUILD_DIR)/SRPMS/*.rpm .
