---
layout: default
title: "Demonstration Infrastructure"
permalink: /fusion-demo-guide/demonstration-infrastructure/
nav_order: 5
parent: "IBM Fusion Demo Guide"
---

# Demonstration infrastructure

## Platform overview
The platform for this lab is a VMware-based Red Hat OpenShift Container Platform cluster, into which you will install and use Fusion.  See the diagram below.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/platform-overview-01.png)

The lab environment is composed of 9 or more Virtual Machines (VMs), hosted on a VMware vSphere cluster.
Six of these VMs form a Red Hat OpenShift Container Platform (OCP) cluster, running Kubernetes. This cluster is a mixed cluster with different kinds of workers nodes. It is composed of:
- 3 Master nodes, running Red Hat CoreOS
- 3 Storage nodes for Fusion Data Foundation (with local storage)
- 3 or more are Worker nodes
A single VM, the IBM Storage Scale node, provides the remote Storage Scale File System (for files) and another VM, the IBM Storage Ceph node, provides the object storage.
The default installation does not include the IBM Fusion operator. You will need to complete the installation of the Fusion operator and the Fusion data services.
> Note: OCP nodes (master & worker) won’t be accessed directly, but through the OpenShift command line interface (oc) or the GUI.
## Addressing plan and credentials
Access to the lab environment is provided through your desktop web browser. The access information needed is provided in the Technology Zone Reservations page.
1. Navigate to your “Reservations” page on IBM Technology Zone using either the “View My Reservations” button on your IBM Technology Zone email notification or log into IBM Technology Zone and use the “My reservations” link. Select your reservation by clicking on the corresponding tile.
1. Note the username and password credentials (the information highlighted in the red rectangle in the previous screen shot).
The table below is a summary of the reservation detail information you will use. This information is listed on the environment reservation page.

|  | IP Address | User | Password |
| --- | --- | --- | --- |
| Cluster URL | https://console-openshift-console.apps.fusion.Storage.lan | kubeadmin | Provided by IBM Technology Zone |
| IBM Storage Scale | 10.10.100.202 | itzuser | <check vm console> |
| IBM Storage Scale GUI | [https://10.10.100.202](https://192.168.252.5) | admin | Passw0rd! |
| IBM Storage Scale GUI |  | csi-storage-gui-user | csi-storage-gui-password |
