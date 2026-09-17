---
layout: default
title: "Create Hosted Cluster"
permalink: /hcp-lab-guide/create-hosted-cluster/
nav_order: 8
parent: "IBM Fusion HCP Lab Guide"
---

# Create Hosted Cluster

## Add Cloud Provider credentials
1. Navigate to the Multicluster Engine by clicking on the **local-cluster drop-down list** (A) in the masthead and click on **All clusters** (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-01.png)

1. Click on the **Connect your cloud provider** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-02.png)

1. Click on the **Red Hat OpenShift Virtualization** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-03.png)

1. (A) Enter **hcp-pull-secret** in the Credential name text entry field and select default from the **Namespace drop-down list** (B). Click on the **Next** (C) button to continue.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-04.png)

1. Leave all settings at their default and click on the **Next** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-05.png)

1. Paste the contents of the pull-secret text file that was created in the Save the cluster pull-secret section into the **Pull secret** (A) text entry box. Paste the contents of the SSH public key text file that was created in the Create SSH key for Hosted Control Planes section into the **SSH public key** (B) text entry box. Finally, click on the **Next** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-06.png)

1. Click on the **Add** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-07.png)

1. The `hcp-pull-secret` Red Hat OpenShift Virtualization credentials will be displayed on the following screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/add-cloud-provider-credentials-08.png)

## Create Cluster
1. In the multicluster Engine GUI, navigate to the Clusters screen by clicking on the **Infrastructure** (A) menu item shown in the left-hand side navigation pane and selecting the **Clusters** (B) sub-item. Next, click on the Create **cluster** (C) button.
   > NOTE: Close the “Managing clusters just got easier” pop-up box, if it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-01.png)

1. Click on the **Red Hat OpenShift Virtualization** (A) tile.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-02.png)

1. Click on the **Hosted** (A) tile.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-03.png)

1. Enter the Cluster details provided in Table 1 – Add Cluster details.

*Table  – Add Cluster details*

| Field name | Value | Callout |
| --- | --- | --- |
| Infrastructure provider credential: | hcp-pull-secret | (A) |
| Cluster name: | hcp-osv-cluster | (B) |
| Hosted cluster namespace | Clusters | (C) |
| Cluster set: | default | (D) |
| Release image: | OpenShift 4.18.x | (E) |
| Etcd storage class: | lvms-hcp-etcd | (F) |


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-04.png)

1. Enter the following labels in the **Additional labels** (A) text entry field separated by a , (when the , is entered the label will appear as a tag below the Additional labels field):
   ```bash
   isf.ibm.com/fusion-base=
   isf.ibm.com/fusion-fdf=
   isf.ibm.com/fusion-backup=
   ```

Click on the **Next** (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-05.png)

1. Enter the Node pool 1 details provided in Table 2 - Node pool 1 details.

*Table  - Node pool 1 details*

| Field name | Value | Callout |
| --- | --- | --- |
| Node pool name: | hcp-osv-nodepool01 | (A) |
| Node pool replicas: | 3 | (B) |
| Core: | 8 | (C) |
| Memory: | 16 | (D) |


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-06.png)

1. Scroll down until Root volume option is displayed and click on the Root volume option or > **dropdown carat** (A) to reveal the Root volume options section is displayed. Enter the Root volume details provided in Table 3 - Root volume options and click on the **Next** (E) button.

*Table  - Root volume options*

| Field name | Value | Callout |
| --- | --- | --- |
| Root volume Storage Class | ocs-storagecluster-ceph-rbd-virtualization | (B) |
| Access mode | ReadWriteMany | (C) |
| Volume mode | Block | (D) |


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-07.png)

1. Leave all defaults and click on the **Next** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-08.png)

1. Click on the **Create** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-09.png)

1. Creating cluster followed by Created cluster, redirecting to details will be displayed briefly before the cluster details will be displayed.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-10.png)

1. Scroll down until details is shown. Cluster API address, Console URL, Username & password, and more information for the hosted cluster are displayed here.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-cluster-11.png)

Congratulations! You have just learned how to work with Red Hat OpenShift Hosted Control Plane. This concludes the exercises in this lab guide.