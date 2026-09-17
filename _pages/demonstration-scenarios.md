---
layout: default
title: "Demonstration Scenarios"
permalink: /demonstration-scenarios/
nav_order: 6
---

# Demonstration Scenarios

The demonstration environment provided for you after provisioning is configured as follows:
- IBM Storage Scale cluster is already deployed.
- Red Hat OpenShift Container Platform (OCP) cluster is already deployed.
- RH OCP cluster has been setup with all the prerequisites for installing IBM Fusion.
- The Pull Secret for Fusion has been created and added to the OpenShift Cluster
- The IBM Operator Catalog has been added to the OpenShift Cluster
- The Machine Config Operator (MCO) has been applied to the OpenShift Cluster
- The SecurityContextContraints have been validated.
- The IBM Storage Scale Cluster has been configured for the Remote Cluster Mount via Storage Scale CNSA
## Access the Environment
### OpenShift Web Console
1. To access the OpenShift console, click on the blue Desktop button (A) or click on the the Desktop url link (B). The login credentials needed are the Username “kubeadmin” (C) and the Password (D) provided. (The actual connection information will be specific to your cluster.)

![Screenshot]({{ site.baseurl }}/assets/images/openshift-web-console-01.png)

1. When your browser connects to the OpenShift Container Platform web user interface (UI), select kube:admin (A) to bring up the login screen. (The IBMid option will use your IBM account to login and is not the recommended method to use for authentication to the environment.)

![Screenshot]({{ site.baseurl }}/assets/images/openshift-web-console-02.png)

1. Enter Username (A) and Password (B) as found in your TechZone reservation.

![Screenshot]({{ site.baseurl }}/assets/images/openshift-web-console-03.png)


![Screenshot]({{ site.baseurl }}/assets/images/openshift-web-console-04.png)

1. Once you have logged in, you will be presented with the OpenShift home page.
### OpenShift Command Line Access
1. To get command line access, find the Bastion SSH Connection (A) information on your IBM Technology Zone reservation details page. The Bastion Password (B) is used to access the remote shell environment. Here is an image of what you will see – the connection data will be specific to your cluster. The API URL (C) will be used in a later step to connect to the OpenShift cluster with the ‘oc’ command.

![Screenshot]({{ site.baseurl }}/assets/images/openshift-command-line-access-01.png)

1. To connect via SSH, open a terminal on a Mac or Linux system and enter a command that looks something like this:

```
`ssh itzuser@apps.ocp-50t6fjgae-droi.cloud.techzone.ibm.com -p ``10022 -``i`` ``sshkey.prv`
```

> Note: On Windows you can use PowerShell or an SSH utility like ‘putty’.
NOTE: the password does NOT work for SSH, you MUST use the private sshkey

NOTE: Once you log in as itzuser, you can run “sudo -i” for root access
1. Once you are in the bastion host, connect to the cluster with the API URL and the kubeadmin user and kubeadmin password by executing a command that looks like this:

```
`oc`` login -u ``kubeadmin`` [API_URL]`
```

where `API_URL` is the API URL value obtained from your reservation page of your environment details. For example:

```
`oc`` login -u ``kubeadmin`` `[https://api.ocp-50t6fjkgae-droi.cloud.techzone.ibm.com:6443](https://api.ocp-50t6fjkgae-droi.cloud.techzone.ibm.com:6443)
```

(When prompted, enter the kubeadmin “Cluster Admin Password”)

![Screenshot]({{ site.baseurl }}/assets/images/openshift-command-line-access-02.png)

1. Now, that you can access the cluster, run a couple of OpenShift commands from the ‘oc’ command line:

```
`oc`` get nodes`
`oc`` get ``clusterversion`
```

![Screenshot]({{ site.baseurl }}/assets/images/openshift-command-line-access-03.png)
