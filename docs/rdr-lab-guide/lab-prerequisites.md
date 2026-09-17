---
layout: default
title: "Lab Prerequisites"
permalink: /rdr-lab-guide/lab-prerequisites/
nav_order: 5
parent: "IBM Fusion RDR Lab Guide"
---

# Regional Disaster Recovery Lab prerequisites

> **Note:** The steps in this section must be performed on **both** clusters (`local-cluster` and `ocp2`). To save time, you can run them in parallel.

The steps in this section will be performed on both clusters, “local-cluster” and “ocp2”. To save time, you can run them in parallel.
## Install the IBM Fusion Operator
Although a Red Hat OpenShift environment has been provisioned on IBM Technology Zone, IBM Fusion has not yet been installed. Therefore, the first step is to install the IBM Fusion Operator. (The IBM Catalog and the entitlement key have already been added.) This section of the lab walks you through the process of installing IBM Fusion operator.
1. In the OpenShift GUI, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word Fusion in the Search text entry field located below the All Items heading. Click on the IBM Storage Fusion (D) operator tile when it appears.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-02.png)

1. Keep all the default settings and click on the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-03.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-04.png)

1. This should cause an “Installing Operator” message to appear.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-05.png)

1. Sometime during the installation process, a “Web console update is available” popup will appear. When this happens, (A) click on the Refresh web console link to reload the OpenShift user interface.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-01.png)

1. Navigate to the Installed Operators screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the Installed Operators (B) sub-item. Wait for the status of the IBM Storage Fusion operator to change to “Succeeded” with a green checkmark before continuing.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-02.png)

## Connect to Fusion
IBM Fusion is fully containerized and designed to be an application in Red Hat OpenShift. Thus, the IBM Fusion GUI can be launched from the OpenShift console.
1. From the OpenShift Console (top right), click the Application menu (A) icon (the icon that looks like 9 squares) and then click IBM Storage Fusion (B). A new tab will be opened for the IBM Fusion GUI. If prompted, enter kubeadmin and your kubeadmin password from the reservation.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-03.png)

1. If the Red Hat OpenShift Container Platform logon screen appears, select kube:admin to bring up the login screen. Enter the kubeadmin credentials to continue to the IBM Fusion user interface. Othere, accept the license agreement by selecting, I have read and accept the license agreement (A) check box.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-04.png)

1. Click the Continue (A) button. This should redirect you to the Welcome to IBM Fusion page.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-05.png)

1. Click the View services (A) button to go directly to the Services page.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-06.png)

## Fusion Data Foundation install process
This section shows how to deploy the Fusion Data Foundation (FDF) configured for use in a Regional Disaster Recovery configuration.
> IMPORTANT: If the OCS/ODF size was set to 2 TiB or 5 TiB when the IBM Fusion on OCP environment was provisioned on IBM Technology Zone, ODF was deployed automatically and the steps outlined in this section have already been performed and this environment cannot be used for this lab.

### Allow VMDK disks to be used by FDF
Fusion Data Foundation being installed on OpenShift Container Platform 4.17 or later do not recognize the disk devices used in the Technology Zone environment as SSD/NVMe disks and will not use those disks for creating the FDF StorageSystem. The following steps will change the rotational flag from 1 to 0 on any unused block devices of the worker nodes to allow the FDF StorageSystem to be created in this lab environment.
> IMPORTANT: Complete this section only if you are deploying on OpenShift version 4.17 or later. If the OpenShift cluster is running 4.16 or earlier, skip this section and proceed to the next section to install and configure Fusion Data Foundation.
> NOTE: The following process can take 25-30 minutes to complete after creation of the MachineConfig.

The udev rule file, /etc/udev/rules.d/99-ibm.rules, is created using a MachineConfig with the following contents to change the queue/rotational flag from 1 to 0 for any devices that do not currently have a partition table.
```bash
ACTION=="add|change", SUBSYSTEM=="block", KERNEL=="sd[a-z]", ENV{ID_PART_TABLE_TYPE}=="", ATTR{queue/rotational}="0"
ACTION=="add|change", SUBSYSTEM=="block", KERNEL=="dm-[0-9]*", ENV{ID_PART_TABLE_TYPE}=="", ATTR{queue/rotational}="0"
```

1. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-07.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-08.png)

1. Navigate to the 99-worker-udev-configuration.yaml file hosted in GitHub, https://github.com/matt-levan/fusion-l4-material/blob/main/all-labs/99-worker-udev-configuration.yaml. Click the Copy raw file (A) (the icon that looks like 2 overlapping windows) button to copy the contents of the file to the clipboard.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-09.png)

1. Navigate back to the OpenShift GUI and Use Ctrl-V (windows), CMD-V (Mac) or the browser Edit -> Paste function to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the recipe.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-ocp2-01.png)

1. The 99-worker-udev-configuration MachineConfig Details page will be displayed.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-ocp2-02.png)

1. In the OpenShift GUI, navigate to the MachineConfigPools screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. Wait for the worker machindConfigurationPool (C) to go from Updating to Up to date before proceeding.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-ocp2-03.png)

### Install Fusion Data Foundation service
The following steps walk you through the installation of Data Foundation using Local storage.
1. In the Fusion GUI, navigate to the Services page by clicking on the Services (A) menu item shown in the left-hand side navigation pane and then clicking on the Data Foundation (B) tile.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-ocp2-04.png)

1. From the Data Foundation overview page, click on the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-ocp2-05.png)

1. From the Data Foundation Install service page, select the Local (A) tile and then click the Install (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-01.png)

1. Wait for the Data Foundation installation process to display an “Install complete!” message and a Healthy status.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-02.png)

### Configuring Data Foundation service
Now that the supporting components for Data Foundation have been installed, it is time to configure the Container Native Storage (CNS) component of Data Foundation.
1. Click the Get Started (A) link on the Fusion services page.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-03.png)

1. Once the Local storage page in Fusion appears, click the Configure storage (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/addressing-plan-and-credentials-01.png)

1. A new window will open to the OpenShift Console to Create StorageSystem for Fusion Data Foundation. Select the Create a new StorageClass using local storage devices and select Use Ceph RBD as the default StorageClass. Click on the Next (C) button to continue to the Create local volume set step.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-01.png)

1. (A) Enter ibm-spectrum-fusion-local in the LocalVolumeSet name text entry field. Verify that 3 Node and 3 Disk appear on the right-hand side of the screen and click on the Next (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-02.png)

1. Click on Yes (A) to Create VolumeSet.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-03.png)

1. PersistentVolumes are being provisioned on the selected nodes loading screen will be displayed until the PVs have been discovered and created.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-04.png)

1. Wait for the Local Volume Set to be created and click on the Next (A) button.
> A taint applied to a node advises the scheduler about its suitability for hosting certain pods. A taint marks a node to repel pods unless those pods explicitly express tolerance for one or more of the node’s taints.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-01.png)

1. Click on the Next (A) button.
> As of Data Foundation 4.12, Hashicorp Vault Key/Value (KV) secret engine API, version 1 and 2 and Thales CipherTrust Manager are supported for cluster-wide and Persistent Volume encryption.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-02.png)

1. Click on the Create StorageSystem (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-03.png)

1. The process will take about 10-15 minutes on average to complete as the components that comprise a Data Foundation cluster are installed and configured. Wait for the ocs-storagecluster-storagesystem to report status as Conditions: Available, VendorCsvReady, VendorSystemPresent and reports the correct Raw Capacity.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/getting-help-01.png)

1. Return to the Fusion GUI, the Data Foundation summary screen will show the following until the process is complete.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configuring-data-foundation-service-01.png)

1. Once all the components have come online, the Data Foundation screen should show a positive Health status for Data Foundation (service), storage cluster, and data resiliency.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configuring-data-foundation-service-02.png)

### Configure default storageClass
It is recommended to use Fusion Data Foundation RADOS Block Devices (RBDs) for this lab. In this section, we will configure a default storageClass using the following annotation, storageclass.kubernetes.io/is-default-class=="true", if not set during the Create StorageSystem wizard.
1. Navigate to the StorageClasses screen by clicking on the Storage (A) menu item shown in the left-hand side navigation pane and selecting the StorageClasses (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-01.png)

1. Check which storageClass has Default listed next to it. In the example below, ocs-storagecluster-cephfs has Default next to it. Note: Only one storageClass should have the is-default-class annotation at a time.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-02.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the Default storageClass line. Click on the Edit annotations (B) item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-03.png)

1. Click the Remove (A) button, looks like a circle with a dash inside, next to the storageclass.kubernet.io/is-default-class line.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-04.png)

1. Click on the Save (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-05.png)

> Note: Continue to the next section if “Use Ceph RBD as the default StorageClass” was set during the Create StorageSystem wizard.

1. Click on the action menu (A) button, looks like 3 stacked dots, on the ocs-storagecluster-ceph-rbd line. Click on the Edit annotations (B) item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-06.png)

1. Click on the + Add more (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-07.png)

1. Enter storageclass.kubernetes.io/is-default-class in the Key (A) text entry field and enter true in the Value (B) text entry field. Click Save (C).

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-08.png)

## Openshift Application Data Protection
1. In the OpenShift GUI, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word OADP in the Search text entry field below the All Items heading. Click on the OADP Operator (D) operator tile when it appears.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-01.png)

1. Click on the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-02.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-03.png)

1. Wait for the OADP Operator to complete installing.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-04.png)

1. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-05.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-08.png)

1. Navigate to the DataProtectionApplication.yaml file hosted in GitHub, https://github.com/matt-levan/fusion-l4-material/blob/main/rdr-lab/DataProtectionApplication.yaml. Click the Copy raw file (A) button (the icon that looks like 2 overlapping windows) to copy the contents of the file to the clipboard.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-06.png)

1. Return to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the filebrowser resources.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-07.png)

1. A DataProtectionApplication will be created in the openshift-adp project that will be used by Regional Disaster Recovery to replicate Kubernetes objects.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-application-data-protection-08.png)

## Configure default storageClass
It is recommended to use Fusion Data Foundation RADOS Block Devices (RBDs) for this lab. In this section, we will configure a default storageClass using the following annotation, storageclass.kubernetes.io/is-default-class=="true".
1. Navigate to the StorageClasses screen by clicking on the Storage (A) menu item shown in the left-hand side navigation pane and selecting the StorageClasses (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-01.png)

1. Check which storageClass has Default listed next to it. In the example below, ocs-storagecluster-cephfs has Default next to it. Note: Only one storageClass should have the is-default-class annotation at a time.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-02.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the Default storageClass line. Click on the Edit annotations (B) item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-03.png)

1. Click the Remove (A) button, looks like a circle with a dash inside, next to the storageclass.kubernet.io/is-default-class line.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-04.png)

1. Click on the Save (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-05.png)

1. Click on the action menu (A) button, looks like 3 stacked dots, on the ocs-storagecluster-ceph-rbd line. Click on the Edit annotations (B) item.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-06.png)

1. Click on the + Add more (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-07.png)

1. Enter storageclass.kubernetes.io/is-default-class in the Key (A) text entry field and enter true in the Value (B) text entry field. Click Save (C).

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-default-storageclass-08.png)

## Configure second cluster storage
1. Repeat Sections Install the IBM Fusion Operator through Section Configure default storageClass on cluster ocp2, if not done so already.