---
layout: default
title: "LVM Storage"
permalink: /hcp-lab-guide/lvm-storage/
nav_order: 5
parent: "IBM Fusion HCP Lab Guide"
---

# LVM Storage

This section takes advantage of a new configMap that was made available in IBM Fusion 2.10 to automatically install and configure the Red Hat LVM Operator and associated lvmCluster custom resource after the IBM Fusion Operator is installed.
> IMPORTANT: When you configure storage for hosted control planes, consider the recommended etcd best practices. To ensure that you meet the latency requirements, dedicate a fast storage device to all hosted control plane etcd instances that run on each control-plane node. It is a recommended best practice to use LVM storage to configure a local storage class for hosted etcd pods.
## Label Infra nodes
The three (3) infrastructure nodes were provisioned with 2 Terabyte (TB) of internal storage to be used as etcd storage of hosted clusters.
1. In the OpenShift GUI, navigate to the Nodes screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. (C) Next, type the word infra in the Search text entry field. Click on the infra-1 (D) node link when it appears.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/label-infra-nodes-01.png)

1. Select the Details (A) tab.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/label-infra-nodes-02.png)

1. Click on the Edit (A) Labels (shown with a pencil) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/label-infra-nodes-03.png)

1. (A) Enter node-role.kubernetes.io/infra in the labels text entry box and click on the Save (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/label-infra-nodes-04.png)

1. Repeat steps 1-4 for Node infra-2
1. Repeat steps 1-4 for Node infra-3
## LVM Disk Path
In this section, the unused disk devices on the infrastructure (infra) nodes will be discovered and saved in a text file for use later as part of the lvm-config configMap.
1. In the OpenShift GUI, navigate to the Nodes screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. (C) Next, type the word infra in the Search text entry field. Click on the infra-1 (D) node link when it appears.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/label-infra-nodes-01.png)

1. Click on the Terminal (A) in the infra-1 Node details page.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/lvm-disk-path-01.png)

1. Enter chroot /host (A) in the Terminal window once it is displayed.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/lvm-disk-path-02.png)

1. Enter the following command in the Terminal window to display the disk device that will be used to create a Volume Group via the LVM Operator.
```bash
lsblk -r --output NAME,MOUNTPOINT | awk -F \/ '/sd/ { dsk=substr($1,1,3);dsks[dsk]+=1 } END { for ( i in dsks ) { if (dsks[i]==1) print i } }'
```


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/lvm-disk-path-03.png)

1. Enter the following command replacing DISK_DEVICE with the value found in the previous command. In this example, sdb would be used.
```bash
ls -l /dev/disk/by-path/pci* | grep DISK_DEVICE
```

Example:
```bash
ls -l /dev/disk/by-path/pci* | grep sdb
```


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/lvm-disk-path-04.png)

1. Copy the value listed as /dev/disk/by-path/pci- to a text document as it will be used during the creation of an LVM Volume Group (VG) in the Install and Configure LVM Storage section.
## Install and Configure LVM Storage
In this section, a `lvm-config` configMap will be generated. This configMap is used by the Fusion operator to automatically install and configure the Red Hat LVM Operator.
1. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-01.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-02.png)

1. Copy the following lvm-config configMap to your clipboard and modify the drives line with the /dev/disk/by-path/pci* value saved in the previous section.
```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: lvm-config
  namespace: ibm-spectrum-fusion-ns
data:
  computeNodes: |
    - infra-1
    - infra-2
    - infra-3
  drives: '- /dev/disk/by-path/pci-0000:03:00.0-scsi-0:0:1:0'
  nodeType: compute
```

1. Use Ctrl-V (windows), CMD-V (Mac) or the browser Edit -> Paste function to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the configMap.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-03.png)

1. The `lvm-config` configMap Details page will be displayed after creation.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-04.png)
