---
layout: default
title: "FDF Provider Mode Install"
permalink: /hcp-lab-guide/fusion-data-foundation-provider-mode-install/
nav_order: 6
parent: "IBM Fusion HCP Lab Guide"
---

# Fusion Data Foundation Provider Mode Install

Fusion Data Foundation provider mode is a deployment configuration within IBM Storage Fusion that enables robust, scalable storage services for Red Hat OpenShift environments. Built on bare metal infrastructure, this mode leverages a minimum of three worker nodes to deliver high-availability storage by replicating data across nodes. It is specifically designed for hosted clusters, offering a resilient foundation for modern containerized workloads.
In provider mode, the architecture is divided into two key components: the Provider, which hosts the core storage services and manages data replication, and the Client, which connects to the provider using a managed Container Storage Interface (CSI). This setup allows external OpenShift clusters to access and utilize the storage services seamlessly, ensuring consistent performance and fault tolerance across environments.
## Allow VMDK disks to be used by FDF
Fusion Data Foundation being installed on OpenShift Container Platform 4.17 or later do not recognize the disk devices used in the Technology Zone environment as SSD/NVMe disks and will not use those disks for creating the FDF StorageSystem. The following steps will change the rotational flag from 1 to 0 on any unused block devices of the worker nodes to allow the FDF StorageSystem to be created in this lab environment.
> IMPORTANT: Complete this section only if you are deploying on OpenShift version 4.17 or later. If the OpenShift cluster is running 4.16 or earlier, skip this section and proceed to the next section to install and configure Fusion Data Foundation.
> NOTE: The following process can take 25-30 minutes to complete after creation of the MachineConfig.

The udev rule file, /etc/udev/rules.d/99-ibm.rules, is created using a MachineConfig with the following contents to change the queue/rotational flag from 1 to 0 for any devices that do not currently have a partition table.
```bash
ACTION=="add|change", SUBSYSTEM=="block", KERNEL=="sd[a-z]", ENV{ID_PART_TABLE_TYPE}=="", ATTR{queue/rotational}="0"
ACTION=="add|change", SUBSYSTEM=="block", KERNEL=="dm-[0-9]*", ENV{ID_PART_TABLE_TYPE}=="", ATTR{queue/rotational}="0"
```

1. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-01.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-and-configure-lvm-storage-02.png)

1. Copy the following 99-worker-udev-configuration MachineConfig to your clipboard.
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  annotations:
    kubernetes.io/description: "udev rule to modify the queue/rotational attribute on unused block devices"
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 99-worker-udev-configuration
spec:
  config:
    ignition:
      config: {}
      security:
        tls: {}
      timeouts: {}
      version: 3.2.0
    networkd: {}
    passwd: {}
    storage:
      files:
      - contents:
          source: data:text/plain;charset=utf-8;base64,QUNUSU9OPT0iYWRkfGNoYW5nZSIsIFNVQlNZU1RFTT09ImJsb2NrIiwgS0VSTkVMPT0ic2RbYS16XSIsIEVOVntJRF9QQVJUX1RBQkxFX1RZUEV9PT0iIiwgQVRUUntxdWV1ZS9yb3RhdGlvbmFsfT0iMCIKQUNUSU9OPT0iYWRkfGNoYW5nZSIsIFNVQlNZU1RFTT09ImJsb2NrIiwgS0VSTkVMPT0iZG0tWzAtOV0qIiwgRU5We0lEX1BBUlRfVEFCTEVfVFlQRX09PSIiLCBBVFRSe3F1ZXVlL3JvdGF0aW9uYWx9PSIwIgo=
          verification: {}
        filesystem: root
        mode: 420
        path: /etc/udev/rules.d/99-ibm.rules
```

1. Use Ctrl-V (windows), CMD-V (Mac) or the browser Edit -> Paste function to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the recipe.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/allow-vmdk-disks-to-be-used-by-fdf-01.png)

1. The 99-worker-udev-configuration MachineConfig Details page will be displayed.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/allow-vmdk-disks-to-be-used-by-fdf-02.png)

1. In the OpenShift GUI, navigate to the Nodes screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. Wait for the worker machindConfigurationPool (C) to go from Updating to Up to date before proceeding.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/allow-vmdk-disks-to-be-used-by-fdf-03.png)

## Fusion Data Foundation install process
This section shows how to deploy the Fusion Data Foundation (FDF) in Provider mode.
> IMPORTANT: If the OCS/ODF size was set to 2 TiB or 5 TiB when the IBM Fusion on OCP environment was provisioned on IBM Technology Zone, ODF was deployed automatically and the steps outlined in this section have already been performed and this environment cannot be used for this lab.

### Install Data Foundation service
The following steps walk you through the installation of Data Foundation using Local storage.
1. In the Fusion GUI, navigate to the Services page by clicking on the Services (A) menu item shown in the left-hand side navigation pane and then clicking on the Data Foundation (B) tile.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-data-foundation-service-01.png)

1. From the Data Foundation overview page, click on the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-data-foundation-service-02.png)

1. From the Data Foundation Install service page, select the Local (A) tile and then click the Install (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-data-foundation-service-03.png)

1. Wait for the Data Foundation installation process to display an “Install complete!” message and a Healthy status before continueing.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-data-foundation-service-04.png)

### Install FDF in Provider mode
In this section, Fusion Data Foundation StorageSystem custom resource will be created using local-storage and configured in Provider mode.
1. In the OpenShift GUI, navigate to the Installed Operators screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the Installed Operators (B) sub-item. (C) Next, type the word Fusion Data Foundation in the Search text entry field. Click on the IBM Storage Fusion Data Foundation (D) operator tile when it appears.
> NOTE: The Project selector should be set to “All Projects” or the openshift-storage namespace.
> NOTE: Select the “IBM Storage Fusion Data Foundation” and not the “IBM Storage Fusion Data Foundation Client.”
> IMPORTANT: When returning to the OpenShift GUI, a “Web console update is available” popup may appear. When this happens, click on the Refresh web console link to reload the OpenShift user interface. If the GUI is not reloaded, then the Create StorageSystem wizard will not load and instead a generic form view will be displayed.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-01.png)

1. Click on the Create StorageSystem (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-02.png)

1. Open the drop-down list associated with “Deployment type” (A) field and select the Provider Mode (B) item from the list.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-03.png)

1. Select the radial button next to the Create a new StorageClass using local storage devices (A) and then click on the Next (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-04.png)

1. (A) Enter ibm-spectrum-fusion-local in the LocalVolumeSet name text entry field and click on the Next (B) button.
> NOTE: If the lvm-config configMap had not been created, configuration of the LocalVolumeSet would require selecting the Disks on selected nodes radial button and manually selecting the nodes named, storage-1, storage-2, and storage-3.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-05.png)

1. Click on the Yes (A) button to create a new LocalVolumeSet.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-06.png)

1. Wait for the PersistentVolumes are being provisioned on the selected nodes process to complete and click on the Next (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-07.png)

1. Click on the Next (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-08.png)

1. Click on the Create StorageSystem (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-09.png)

1. The Fusion Data Foundation Deployment ocs-storagecluster-storagesystem status will progress from Progressing, Degraded to Reconcile Complete, Progressing or Available.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-fdf-in-provider-mode-10.png)

## Configure default storageClass
It is recommended to use OpenShift Data Foundation RADOS Block Devices (RBDs) for OpenShift Virtualization. In this section, we will configure the default storageClass using the following annotation, storageclass.kubernetes.io/is-default-class=="true".
> NOTE: When the IBM Fusion on OCP environment was provisioned in IBM Technology Zone with OCS/ODF size was set to None, ODF was not deployed automatically. A managed-nfs-storage storageClass was created to host the image-registry-storage PVC and was configured as the Default storageClass.

1. Navigate to the StorageClasses screen by clicking on the Storage (A) menu item shown in the left-hand side navigation pane and selecting the StorageClasses (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-01.png)

1. Check which storageClass has Default listed next to it. In the example below, managed-nfs-storage has Default next to it.
> NOTE: It is recommended to have only one storageClass withthe is-default-class annotation at a time. If more than one StorageClass is marked as default, a PersistentVolumeClaim without an explicitly defined storageClassName will be created using the most recently created default StorageClass.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-02.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the Default storageClass line. Click on the Edit annotations (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-03.png)

1. Click the Remove (A) button, looks like a circle with a dash inside, next to the storageclass.kubernet.io/is-default-class line.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-04.png)

1. Click on the Save (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-05.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the ocs-storagecluster-ceph-rbd line. Click on the Edit annotations (B) item.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-06.png)

1. Click on the + Add more (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-07.png)

1. Enter storageclass.kubernetes.io/is-default-class in the Key (A) text entry field and enter true in the Value (B) text entry field.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-08.png)

1. Click on the Save (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-09.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the ocs-storagecluster-ceph-rbd-virtualization line. Click on the Edit annotations (B) item.
> IMPORTANT: The ocs-storagecluster-ceph-rbd-virtualization storageClass is not always created by the Fusion Data Foundation and may not be available.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-10.png)

1. Click on the + Add more (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-11.png)

1. Enter storageclass.kubevirt.io/is-default-virt-class in the Key (A) text entry field and enter true in the Value (B) text entry field.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-12.png)

1. Click on the Save (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/configure-default-storageclass-13.png)
