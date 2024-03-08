#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the MIT License. See the LICENSE accompanying this file
# for the specific language governing permissions and limitations under
# the License.

# called by dracut
check() {
  # don't install this module unless the configuration explicitly requests it
  return 255
}

# called by dracut
depends() {
  echo bash udev-rules
  return 0
}

# called by dracut
install() {
  # Install udev rules
  inst_rules \
    51-ec2-hvm-devices.rules \
    51-ec2-xen-vbd-devices.rules \
    53-ec2-read-ahead-kb.rules \
    70-ec2-nvme-devices.rules

  # Install scripts
  inst_multiple \
    ebsnvme-id \
    ec2nvme-nsid \
    ec2udev-vbd

  # Install nvme-cli and its dependencies
  inst_multiple \
    /usr/sbin/nvme \
    /lib64/libcrypto.* \
    /lib64/libjson-c.* \
    /lib64/libnvme.* \
    /lib64/libnvme-mi.* \
    /lib64/libz.*
}
