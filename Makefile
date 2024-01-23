.PHONY: rpm
rpm:
	git archive --format=tar HEAD > amazon-ec2-utils.tar
	gzip -f -9 amazon-ec2-utils.tar
	rpmbuild --define "%_topdir $$(mktemp -d /tmp/amazon-linux-utils.rpm-XXXXXXXX)" -ta amazon-ec2-utils.tar.gz -v
