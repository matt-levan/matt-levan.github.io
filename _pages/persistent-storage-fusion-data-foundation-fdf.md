---
layout: default
title: "Persistent Storage – Fusion Data Foundation – FDF"
permalink: /persistent-storage-fusion-data-foundation-fdf/
nav_order: 10
---

# Persistent Storage – Fusion Data Foundation – FDF


![Screenshot]({{ site.baseurl }}/assets/images/image60.png)

Select Storage  Local storage and Click “Getting Started”

![Screenshot]({{ site.baseurl }}/assets/images/image61.png)

The screen will go to the OpenShift Console and bring up the create storage menu

![Screenshot]({{ site.baseurl }}/assets/images/image62.png)

“create a new StorageClass using local storage devices” will be pre-selected. And check “Next”
We only need to enable the default storage class of Ceph RBD and set the default storage class for Virtualization (if you plan to setup Virtualization)

![Screenshot]({{ site.baseurl }}/assets/images/image63.png)


![Screenshot]({{ site.baseurl }}/assets/images/image64.png)

We need the local operator for the local system, click install to install the local storage operator

![Screenshot]({{ site.baseurl }}/assets/images/image65.png)

Install the local storage operator

![Screenshot]({{ site.baseurl }}/assets/images/image66.png)


![Screenshot]({{ site.baseurl }}/assets/images/image67.png)

When complete, select view operator

![Screenshot]({{ site.baseurl }}/assets/images/image68.png)

## Create local Storage Cluster – FDF

![Screenshot]({{ site.baseurl }}/assets/images/image69.png)

Now navigate back to Storage  Data Foundation  Storage Cluster
and “select configure data foundation”
Then Select Create Storage Cluster

![Screenshot]({{ site.baseurl }}/assets/images/image70.png)


![Screenshot]({{ site.baseurl }}/assets/images/image71.png)


![Screenshot]({{ site.baseurl }}/assets/images/image72.png)

Continue the installation and configuration

![Screenshot]({{ site.baseurl }}/assets/images/image73.png)


![Screenshot]({{ site.baseurl }}/assets/images/image74.png)

After the local storage is discovered, you can select where and how to install Data foundation

You can either use all of the nodes and disks, or use a subset.

![Screenshot]({{ site.baseurl }}/assets/images/image75.png)

Use the infra nodes for data foundation.

![Screenshot]({{ site.baseurl }}/assets/images/image76.png)


![Screenshot]({{ site.baseurl }}/assets/images/image77.png)


![Screenshot]({{ site.baseurl }}/assets/images/image78.png)

Then select if you want to enable provider mode or not

![Screenshot]({{ site.baseurl }}/assets/images/image79.png)

Selecting Default, will only enable local use. Selecting Host will enable provider mode for hosted clusters.
It will now create a storage cluster, this will take some time.

![Screenshot]({{ site.baseurl }}/assets/images/image80.png)

Wait for the cluster to become healthy
Validate the storage classes where created

![Screenshot]({{ site.baseurl }}/assets/images/image81.png)

## Remote File Systems – External Mount of Storage Scale Cluster
This section will demonstrate how to connect IBM Fusion to a remote IBM Storage Scale cluster. The remote Storage Scale cluster will provide persistent storage for OpenShift workloads.
Without IBM Fusion, an OpenShift administrator who wanted to use Storage Scale for OpenShift had to install Storage Scale Container Native Scale Access (CNSA) and manage all the configurations needed to connect CNSA with the remote Storage Scale cluster.
With Fusion, all these steps can be done through a simple GUI and the installation and connection to the remote Storage Scale cluster is handled automatically.
If you had selected Data Foundation External when install the Data Foundation service, you will see 
“external systems” on the menu

![Screenshot]({{ site.baseurl }}/assets/images/image82.png)


![Screenshot]({{ site.baseurl }}/assets/images/image83.png)

Select “Connect to external Systems”
Then select
IBM Scale

![Screenshot]({{ site.baseurl }}/assets/images/image84.png)


![Screenshot]({{ site.baseurl }}/assets/images/image85.png)

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


![Screenshot]({{ site.baseurl }}/assets/images/image86.jpeg)


![Screenshot]({{ site.baseurl }}/assets/images/image87.png)


![Screenshot]({{ site.baseurl }}/assets/images/image88.png)


![Screenshot]({{ site.baseurl }}/assets/images/image89.png)

1. Wait for the cluster to show “ready”
1. Then check the “Storage Classes”, look for the ibm-spectrum-scale-sample class

![Screenshot]({{ site.baseurl }}/assets/images/image90.png)

### Logon to the Storage Scale command line and issue Storage Scale commands
> Note: For visual guidance, refer to the supplemental PowerPoint available at [https://ibm.box.com/v/TechzoneSpFusionScreenshots](https://ibm.box.com/v/TechzoneSpFusionScreenshots). Screenshots of this process can be found in the section titled “SSH to Storage Scale Node.”
In this section, you will be instructed to issue appropriate native IBM Storage Scale commands to obtain the required Storage Scale cluster and filesystem information.
The screenshots provided will also help you with more details about what is being requested with the “Add IBM Storage Scale file system” prompts.
Connect to the Bastion host via SSH by opening a terminal on a Mac or Linux system and entering a command that looks something like this:

```
`ssh itzuser@apps.ocp-50t6fjgae-droi.cloud.techzone.ibm.com -p 40222`` -``i`` <``ssh_private_key``>`
```

(Use the Bastion Password provided with your IBM Technology Zone reservation. Also, the hostname is an example; get the real host name from your reservation.)
Connect to the Scale node from the Bastion host by entering the following command in the terminal. The password for the itzuser of the Storage Scale node is in the console page of the reservation.

```
`ssh `[itzuser@10.10.10.202](mailto:itzuser@10.10.10.202)`
``sudo`` -``i`` `
```

List the Storage Scale cluster name, id, and nodes associated with the Storage Scale cluster by entering the following command in the terminal window.

```
`mmlscluster`
```

![Screenshot]({{ site.baseurl }}/assets/images/image91.png)

List the Storage Scale GUI users by entering the following command in the terminal window.

```
`/``usr``/``lpp``/``mmfs``/``gui``/cli/``lsuser`
```

![Screenshot]({{ site.baseurl }}/assets/images/image92.png)

List the Storage Scale file systems and their mount points by entering the following command in the terminal window.

```
`mmlsfs`` all -T`
```

![Screenshot]({{ site.baseurl }}/assets/images/image93.png)

### Use the Storage Scale REST API and the Linux curl command
You can use the representational state transfer (REST) method to issue commands in your SSH “Terminal” window if an IBM Storage Scale username and password have been provided for a user that has been granted the permissions necessary to access the IBM Storage Scale RESTful API.
In the terminal window, execute the following command:

```
`curl -u ``csi-storage-gui-``user:csi``-storage-gui-password`` -X GET -k \``
https://``10.10.10.202``/scalemgmt/v2/cluster `
```

![Screenshot]({{ site.baseurl }}/assets/images/image94.png)

[About the curl command](https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/)
[Documentation on Storage Scale REST API used with the curl command](https://www.ibm.com/docs/en/spectrum-scale/5.1.3?topic=api-list-spectrum-scale-management-commands)
## Data Encryption
In some cases, it is necessary to encrypt data stored with Fusion and the Global Data Platform. This can be configured directly through the Fusion GUI in the Remote file systems page.
> Note: The information provided in this section is for educational purposes to denote that only the IBM Security Guardium Key Lifecycle Manager (GKLM) is available for enabling encryption with IBM Fusion and the Global Data Platform.
To enable data encryption, you must first connect to IBM Security Guardium Key Lifecycle Manager (GKLM) by clicking on the Connect button.

![Screenshot]({{ site.baseurl }}/assets/images/image95.png)
