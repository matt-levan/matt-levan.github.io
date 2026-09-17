---
layout: default
title: "Persistent Storage – FDF"
permalink: /fusion-demo-guide/persistent-storage-fdf/
nav_order: 2
parent: "Provide Persistent Storage"
grand_parent: "IBM Fusion Demo Guide"
---

# Persistent Storage – Fusion Data Foundation – FDF

Now install Fusion Data Foundation for local storage on the cluster.

1. Select **Storage → Local storage** and click **Getting Started**.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-01.png)

The screen will go to the OpenShift Console and bring up the Create Storage menu.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-02.png)

1. **"Create a new StorageClass using local storage devices"** will be pre-selected. Click **Next**.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-03.png)

1. Enable the default storage class of **Ceph RBD** and set the default storage class for **Virtualization** (if you plan to set up Virtualization).

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-04.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-05.png)

1. The local storage operator is required. Click **Install** to install it.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-06.png)

1. Complete the local storage operator installation.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-07.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-08.png)

1. When the installation is complete, click **View Operator**.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/persistent-storage-fusion-data-foundation-fdf-09.png)

## Create local Storage Cluster – FDF

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-01.png)

1. Navigate back to **Storage → Data Foundation → Storage Cluster** and select **Configure data foundation**.
1. Then select **Create Storage Cluster**.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-02.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-03.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-04.png)

Continue the installation and configuration.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-05.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-06.png)

After the local storage is discovered, you can select where and how to install Data Foundation. You can either use all of the nodes and disks, or use a subset.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-07.png)

Use the infra nodes for Data Foundation.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-08.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-09.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-10.png)

Select whether you want to enable provider mode or not.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-11.png)

- Selecting **Default** will only enable local use.
- Selecting **Host** will enable provider mode for hosted clusters.

It will now create a storage cluster — this will take some time.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-12.png)

Wait for the cluster to become healthy, then validate the storage classes were created.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-local-storage-cluster-fdf-13.png)

## Remote File Systems – External Mount of Storage Scale Cluster

This section demonstrates how to connect IBM Fusion to a remote IBM Storage Scale cluster. The remote Storage Scale cluster will provide persistent storage for OpenShift workloads.

Without IBM Fusion, an OpenShift administrator who wanted to use Storage Scale for OpenShift had to install Storage Scale Container Native Scale Access (CNSA) and manage all the configurations needed to connect CNSA with the remote Storage Scale cluster.

With Fusion, all these steps can be done through a simple GUI and the installation and connection to the remote Storage Scale cluster is handled automatically.

If you selected **Data Foundation External** when installing the Data Foundation service, you will see **External systems** in the menu.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-01.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-02.png)

1. Select **Connect to external Systems**, then select **IBM Scale**.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-03.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-04.png)

*Table  – Add file system details*

| Field name | Value |
| --- | --- |
| Host names | 10.10.10.202 |
| Cluster ID | 2610328468137304447 |
| Username | csi-storage-gui-user |
| Password | csi-storage-gui-password |
| Node 1 (optional) | scale01 |
| Node 1 IP address (optional) | 10.10.10.202 |
| File System Name | fs1 |
| Storage class name | fusionfs1 |


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-05.jpeg)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-06.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-07.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-08.png)

1. Wait for the cluster to show “ready”
1. Then check the “Storage Classes”, look for the ibm-spectrum-scale-sample class

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/remote-file-systems-external-mount-of-storage-scale-cluster-09.png)

### Logon to the Storage Scale command line and issue Storage Scale commands
> Note: For visual guidance, refer to the supplemental PowerPoint available at [https://ibm.box.com/v/TechzoneSpFusionScreenshots](https://ibm.box.com/v/TechzoneSpFusionScreenshots). Screenshots of this process can be found in the section titled “SSH to Storage Scale Node.”
In this section, you will be instructed to issue appropriate native IBM Storage Scale commands to obtain the required Storage Scale cluster and filesystem information.
The screenshots provided will also help you with more details about what is being requested with the “Add IBM Storage Scale file system” prompts.
Connect to the Bastion host via SSH by opening a terminal on a Mac or Linux system and entering a command that looks something like this:

```bash
ssh itzuser@apps.ocp-50t6fjgae-droi.cloud.techzone.ibm.com -p 40222 -i <ssh_private_key>
```

(Use the Bastion Password provided with your IBM Technology Zone reservation. Also, the hostname is an example; get the real host name from your reservation.)
Connect to the Scale node from the Bastion host by entering the following command in the terminal. The password for the itzuser of the Storage Scale node is in the console page of the reservation.

```bash
ssh [itzuser@10.10.10.202](mailto:itzuser@10.10.10.202)
sudo -i 
```

List the Storage Scale cluster name, id, and nodes associated with the Storage Scale cluster by entering the following command in the terminal window.

```bash
mmlscluster
```

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/logon-to-the-storage-scale-command-line-and-issue-storage-sc-01.png)

List the Storage Scale GUI users by entering the following command in the terminal window.

```bash
/usr/lpp/mmfs/gui/cli/lsuser
```

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/logon-to-the-storage-scale-command-line-and-issue-storage-sc-02.png)

List the Storage Scale file systems and their mount points by entering the following command in the terminal window.

```bash
mmlsfs all -T
```

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/logon-to-the-storage-scale-command-line-and-issue-storage-sc-03.png)

### Use the Storage Scale REST API and the Linux curl command
You can use the representational state transfer (REST) method to issue commands in your SSH “Terminal” window if an IBM Storage Scale username and password have been provided for a user that has been granted the permissions necessary to access the IBM Storage Scale RESTful API.
In the terminal window, execute the following command:

```bash
curl -u csi-storage-gui-user:csi-storage-gui-password -X GET -k \
https://10.10.10.202/scalemgmt/v2/cluster 

```

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/use-the-storage-scale-rest-api-and-the-linux-curl-command-01.png)

[About the curl command](https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/)
[Documentation on Storage Scale REST API used with the curl command](https://www.ibm.com/docs/en/spectrum-scale/5.1.3?topic=api-list-spectrum-scale-management-commands)
## Data Encryption
In some cases, it is necessary to encrypt data stored with Fusion and the Global Data Platform. This can be configured directly through the Fusion GUI in the Remote file systems page.
> Note: The information provided in this section is for educational purposes to denote that only the IBM Security Guardium Key Lifecycle Manager (GKLM) is available for enabling encryption with IBM Fusion and the Global Data Platform.
To enable data encryption, you must first connect to IBM Security Guardium Key Lifecycle Manager (GKLM) by clicking on the Connect button.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/data-encryption-01.png)
