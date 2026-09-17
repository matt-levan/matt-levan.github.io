---
layout: default
title: "HCP Prerequisites"
permalink: /hcp-lab-guide/hosted-control-plane-prerequisites/
nav_order: 7
parent: "IBM Fusion HCP Lab Guide"
---

# Hosted Control Plane Prerequisites

In this section the required operators will be installed and configured, if necessary, to support the other sections in the lab.
## OpenShift Virtualization Operator
1. In the OpenShift GUI, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word Openshift Virtualization in the Search text entry field below the All Items heading. Click on the OpenShift Virtualization (D) operator tile when it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-01.png)

1. Click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-02.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-03.png)

1. Wait for the Create Hyperconverged button to change from gray to blue like the one shown below. Click on the Create HyperConverged (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-04.png)

1. Scroll down until vmStateStorageClass is shown. (A) Enter ocs-storagecluster-cephfs in the text entry field.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-05.png)

1. Keep all the other default settings as shown. Scroll down until the Create (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-06.png)

1. The OpenShift Virtualization Deployment kubevirt-hyperconverged status will progress from Progressing, Degraded to Reconcile Complete, Progressing or Available. A “Web console update is available” popup will appear at some point. When this happens (A) click on the Refresh web console link to reload the OpenShift user interface.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-07.png)

1. After the user interface has been reloaded, a new Virtualization menu item will be available on the left-hand side navigation pane. OpenShift Virtualization has been installed.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/openshift-virtualization-operator-08.png)

## MetalLB Operator
MetalLB is a load balancer implementation which relies on L2 (Address Resolution Protocl (ARP) / Neighbor Discovery Protocol (NDP) or L3 (Border Gateway Protocol (BGP)) to advertise endpoints for Services with a type of LoadBalancer. MetalLB solves the problem for bare metal platforms using standard network protocols. The two modes (L2 and BGP) provide options for announcing reachability information for load balancer IP addresses.
For MetalLB to meet this need, you must configure your networking infrastructure to ensure that the network traffic for the external IP address is routed from clients to the host network for the cluster.
MetalLB can operate in two modes:
- MetalLB operating in layer2 mode provides support for failover by utilizing a mechanism like IP failover. However, instead of relying on the virtual router redundancy protocol (VRRP) and keepalived, MetalLB leverages a gossip-based protocol to identify instances of node failure. When a failure is detected, another node assumes the role of the leader node, and a gratuitous ARP (address resolution protocol) message is dispatched to broadcast this change.
- MetalLB operating in layer3 or border gateway protocol (BGP) mode delegates failure detection to the network. The BGP router or routers that the OpenShift Container Platform nodes have established a connection with will identify any node failure and terminate the routes to that node.
1. In the OpenShift GUI, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word MetalLB in the Search text entry field below the All Items heading Click on the MetalLB Operator (D) tile when it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-01.png)

1. Keep all the default settings and click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-02.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-03.png)

1. Wait for the install to complete, denoted by a green checkmark. Click on the View Operator (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-04.png)

1. Scroll down until the MetalLB tile is displayed and click on the Create instance (A) link.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-05.png)

1. The MetalLB Custom Resource configuration screen will be displayed.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-06.png)

1. Leave all settings at their default and scroll down until the Create button (A) is displayed. Click on this button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-07.png)

1. Scroll the tab bar until IPAddressPool is displayed. Click on the IPAddressPool (A) tab and click on the Create IPAddressPool (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-08.png)

1. (A) Enter techzone-ipaddresspool in the Name text entry field.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-09.png)

1. Expand addresses (A) by clicking the toggle (the icon that looks like a > when collapsed). Scroll down until 3 Value fields are displayed. (B) Enter 192.168.252.200-192.168.252.220 in the first Value text entry field. Click on Remove addresses (C) associated with the 2nd and 3rd Value text entry fields.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-10.png)

1. Scroll down and click on the Create (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-11.png)

1. Scroll the tab bar until L2Advertisement is displayed. Click on the L2Advertisement (A) tab and click on the Create L2Advertisement (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-12.png)

1. (A) Enter l2-adv-techzone in the Name text entry field.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-13.png)

1. Scroll down until ipAddressPools is displayed. Expand ipAddressPools (A) by clicking the toggle (the icon that looks like a > when collapsed). (B) Enter techzone-ipaddresspool in the first Value text entry field. Click the Create (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/metallb-operator-14.png)

1. Patch the ingress.
   ```bash
   oc patch ingresscontroller -n openshift-ingress-operator default --type=json -p '[{ "op": "add", "path": "/spec/routeAdmission", "value": {wildcardPolicy: "WildcardsAllowed"}}]'
   ```

## Red Hat multicluster engine for Kubernetes
1. In the OpenShift GUI, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word multicluster engine in the Search text entry field below the All Items heading. Click on the multicluster enginer for Kubernetes (D) operator tile when it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-01.png)

1. Click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-02.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-03.png)

1. Wait for the Create MulticlusterEngine button to change from gray to blue like the one shown below. Click on the Create MulticlusterEngine (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-04.png)

1. Keep all the default settings as shown. Scroll down until the Create (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-05.png)

1. The multicluster engine for Kubernetes Deployment multiclusterengine status will progress from Progressing, Degraded to Reconcile Complete, Progressing or Running. A “Web console update is available” popup will appear at some point. When this happens (A) click on the Refresh web console link to reload the OpenShift user interface.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-06.png)

1. After the user interface has been reloaded, a new local-cluster menu item will be available on the masthead. Multicluster engine for Kubernetes has been installed.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/red-hat-multicluster-engine-for-kubernetes-07.png)

## Install virtctl on Bastion host
1. Refer to the IBM Fusion - Install, Backup, and OSV Prep Guide v2.10.0.0 documentation (https://ibm.seismic.com/Link/Content/DCq6Hf6WGGjRW8FR64P7gh6h9DRP) for instructions on connecting to the Bastion host.
1. In the OpenShift GUI, click on the Help menu (A) drop-down button in the masthead and select Command Line Tools (B) item from the list.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-virtctl-on-bastion-host-01.png)

1. When the Command Line Tools screen appears, scroll down until the virtctl – KubeVirt command line interface appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-virtctl-on-bastion-host-02.png)

1. Right-click on the Download virtctl for Linux for x86_64 (A) link to open your browsers context menu. From the browser context menu, click on the Copy Link Address (B) to copy the URL to download the virtctl binary to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-virtctl-on-bastion-host-03.png)

1. In the terminal window connected to the bastion host, enter the following text and paste the contents of the clipboard after the text to download the virtctl.tar.gz compressed file.
   ```bash
   curl -L -O [PASTE CLIPBOARD CONTENTS]
   ```

where:
- -L informs the curl command follow any redirects returned
- -O informs curl to write the output returned to disk

Confirm the file was successfully downloaded by executing the command ls -al.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/install-virtctl-on-bastion-host-04.png)

1. Enter the command tar xzvf virtctl.tar.gz to extract the virtctl executable.

Output:
```bash
virtctl
```

1. Enter the command chmod u+x virtctl to make virtctl executable.
## Create SSH key for Hosted Control Planes
In this section of the lab, we will connect to the Linux Bastion host and generate a public and private SSH key for connecting to the Linux virtual machines.
1. Get the connection details from the lab reservation screen. The Bastion SSH connection (A) will be entered in the next step to connect to the Bastion host and the Bastion Password (B) will allow login to the machine.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-ssh-key-for-hosted-control-planes-01.png)

1. Open a Terminal (MacOS or Linux) or Windows Terminal (Windows). In the following example iTerm2 is being used as a terminal on MacOS. Enter the Bastion SSH connection and hit ENTER. Copy the Bastion Password and when asked for itzuser@bastion-hostname’s password, paste it and press Enter. If connection is successful, the command prompt will look something like this.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-ssh-key-for-hosted-control-planes-02.png)

1. Enter ssh-keygen in the terminal window and hit Enter. A series of questions will need to be answered. We will use the defaults.
   ```bash
   ssh-keygen
   ```

OUTPUT:
```bash
Generating public/private rsa key pair.
Enter file in which to save the key (/home/itzuser/.ssh/id_rsa): <ENTER>
Enter passphrase (empty for no passphrase): <ENTER>
Enter same passphrase again: <ENTER>
Your identification has been saved in /home/itzuser/.ssh/id_rsa.
Your public key has been saved in /home/itzuser/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:QNiIJjm3pdodaM9dA85Rz9pUA/6rJFuULaHXtbM/OAw itzuser@bastion
The key's randomart image is:
<randomart not displayed>
```


![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-ssh-key-for-hosted-control-planes-03.png)

1. Execute the following command to display the public key that was generated during the previous step.
   > NOTE: The below command assumes all defaults were used when creating the keys.

   ```bash
   cat /home/itzuser/.ssh/id_rsa.pub
   ```


   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/create-ssh-key-for-hosted-control-planes-04.png)

1. Copy the highlighted content above to your clipboard and save in a text file. The SSH public key will be used later in the “Add Cloud Provider credentials” section of the Create Hosted Cluster lab to configure the OpenShift Virtualization Credential.
## Save the cluster pull-secret
1. Navigate to the Secrets screen by clicking on the Workloads (A) menu item shown in the left-hand side navigation pane and selecting the Secrets (B) sub-item. To switch to the openshift-config project, click on the Project Selector (C) and (E) enter openshift-config in the Select project… text entry field. Finally, click on the openshift-config (F) project to select it.
   > NOTE: Show default projects (D) needs to be selected to display projects that begin with openshift-.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/save-the-cluster-pull-secret-01.png)

1. Click on the pull-secret (A) secret to open the Secret details screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/save-the-cluster-pull-secret-02.png)

1. Scroll down until the Data section is displayed. Click on the Copy to clipboard (A) (looks like a clipboard) button to copy the contents to your clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/save-the-cluster-pull-secret-03.png)

1. Paste the contents of the clipboard into a text file and save the file. The global pull-secret will be used later in the “Add Cloud Provider credentials” section of the Create Hosted Cluster lab to configure the OpenShift Virtualization Credential.