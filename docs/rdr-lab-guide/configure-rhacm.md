---
layout: default
title: "Configure RHACM"
permalink: /rdr-lab-guide/configure-rhacm/
nav_order: 6
parent: "IBM Fusion RDR Lab Guide"
---

# Configure RHACM

In this section, Red Hat Advanced Cluster Management (RHACM) will be configured to enable centralized control and coordination of OpenShift clusters, a critical step in setting up regional disaster recovery with IBM Fusion.
## Red Hat Advanced Cluster Manager
1. In the OpenShift GUI of local-cluster, navigate to the OperatorHub screen by clicking on the Operators (A) menu item shown in the left-hand side navigation pane and selecting the OperatorHub (B) sub-item. (C) Next, type the word Advanced Cluster Management for Kubernetes in the Search text entry field below the All Items heading. Click on the Advanced Cluster Management for Kubernetes (D) operator tile when it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-01.png)

1. Click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-02.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-03.png)

1. Wait for the Create MulticlusterHub button to change from gray to blue like the one shown below. Click on the Create MulticlusterHub (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-04.png)

1. Keep all the default settings as shown. Scroll down until the Create (A) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-05.png)

1. The Advanced Cluster Manager for Kubernetes Deployment multiclusterhub status will progress from Progressing, Degraded to Reconcile Complete, Progressing or Running. A “Web console update is available” popup will appear at some point. When this happens (A) click on the Refresh web console link to reload the OpenShift user interface.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-06.png)

1. After the user interface has been reloaded, a new local-cluster menu item will be available on the masthead. Advanced Cluster Manager for Kubernetes has been installed.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/red-hat-advanced-cluster-manager-07.png)

## Multicluster Orchestrator
1. In the OpenShift GUI of local-cluster, navigate to the OperatorHub screen by clicking on the **Operators** (A) menu item shown in the left-hand side navigation pane and selecting the **OperatorHub** (B) sub-item. (C) Next, type the word Multicluster Orchestrator in the Search text entry field below the All Items heading. Click on the Multicluster Orchestrator (D) operator tile when it appears.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/multicluster-orchestrator-01.png)

1. Click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/multicluster-orchestrator-02.png)

1. When the Install Operator screen appears, click the Enable (A) button under the Console plugin section, and scroll down until the Install (B) button appears. Then, click on the button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/multicluster-orchestrator-03.png)

1. The deployment of the Multicluster Orchestrator will occur and no further configuration is required. A “Web console update is available” popup will appear at some point. When this happens (A) click on the Refresh web console link to reload the OpenShift user interface.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/multicluster-orchestrator-04.png)

## Import Second cluster
1. Connect to the IBM Technology Zone My Reservations page (https://techzone.ibm.com/my-reservations) and select the reservation named ocp2.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-01.png)

1. Scroll down to the bottom of the screen and click on the Download kubeconfig (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-02.png)

1. Open a Terminal window or File Browser (Finder on a Mac or Windows Explorer on Windows) and navigate to the Downloads folder. Select the conf_kubeconfig_download.conf and rename it to ocp2_kubeconfig.conf.
1. Open the ocp2_kubeconfig.conf file in a text editor and copy all the contents in the file to the clipboard. CMD-A (Mac) or CTRL-A (Windows/Linux) can be used to select all.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-03.png)

1. In the OpenShift GUI of local-cluster, navigate to the Advanced Cluster Manager by clicking on the local-cluster drop-down list (A) in the masthead and click on All clusters (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-04.png)

1. Click on the Import an existing cluster (A) button of the getting started popup.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-05.png)

1. Alternatively, if the popup window was closed, navigate to the Clusters page and click on the Import cluster (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-06.png)

1. (A) Enter ocp2 in the Name field and click on the Cluster set dropdown (B). Select the default (C) item from the Cluster set dropdown.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-07.png)

1. Click on the Import mode dropdown (A) item and select the Kubeconfig (B) item from the list.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-08.png)

1. Paste the contents of the Clipboard—containing the contents of the ocp2_kubeconfig.conf file—into the Kubeconfig (A) text entry field and click on the Next (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-09.png)

1. Click on the Next (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-10.png)

1. Click on the Import (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-11.png)

1. Wait for the Status to show as Ready with a green checkmark.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-12.png)

## Configure submariner
1. In the OpenShift GUI, navigate to the Nodes screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. Select worker-1 (C) from the Nodes list.

   > IMPORTANT: The IBM Technology Zone environment has been configured to forward submariner traffic exclusively to worker-1. If another worker node is used, submariner will fail to establish a connection.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-01.png)

1. Select Details (A) on the worker-1 Node details screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-02.png)

1. Scroll down until the Labels section appears and select Edit (A) (appears with a pencil).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-03.png)

1. (A) Enter submariner.io/gateway=true in the Labels for worker-1 text entry field click on the Save (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-04.png)

1. Complete Steps 1 through 4 again on the second cluster (ocp2).


   > IMPORTANT: Before proceeding, ensure that the submariner.io/gateway=true label is applied to the worker-1 nodes in both the local-cluster and ocp2 clusters. This step is critical for submariner connectivity.

1. In the OpenShift GUI of local-cluster, navigate to the Advanced Cluster Manager by clicking on the local-cluster drop-down list (A) in the masthead and click on All clusters (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-04.png)

1. In the OpenShift GUI, navigate to the Clusters screen by clicking on the Infrastructure (A) menu item shown in the left-hand side navigation pane and selecting the Clusters (B) sub-item. Click on the Cluster sets (C) tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-05.png)

1. Click on the default (A) cluster set to open the Overview screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-06.png)

1. Click on the Submariner add-ons (A) tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-07.png)

1. Click on the Install Sumbariner add-ons (A) button at the bottom of the screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-08.png)

1. Add the OpenShift clusters by selecting the Select clusters (A) selection box to open the Target clusters list. Then, from the dropdown, select both local-cluster (B) and ocp2 (C) to include them as target clusters.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-09.png)

1. Confirm that both local-cluster and ocp2 are listed in the Target clusters selection box. Once verified, click on the Next (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-10.png)

1. Click on the Install (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-11.png)

1. The status of the submariner connection should show the following after installation.

   > NOTE: 'Connection status' may show degraded for a short period of time until the links are established and 'Healthy'.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/configure-submariner-12.png)

## Create Disaster Recovery Policy
1. In the OpenShift GUI of local-cluster, navigate to the Advanced Cluster Manager by clicking on the local-cluster drop-down list (A) in the masthead and click on All clusters (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-04.png)

1. In the OpenShift GUI, navigate to the Disaster Recovery screen by clicking on the Data Services (A) menu item shown in the left-hand side navigation pane and selecting the Disaster Recovery (B) sub-item. Click on the Create a disaster recovery policy (C).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-disaster-recovery-policy-01.png)

1. (A) Enter ocp1-ocp2-dr in the Policy name text entry field. Then, in the Connect clusters selection box, check the boxes next to both local-cluster (B) and ocp2 (B) to include them in the policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-disaster-recovery-policy-02.png)

1. Scroll down until the Create button appears and click on the Create (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-disaster-recovery-policy-03.png)

1. Wait for the status to update from Not validated to Validated.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-disaster-recovery-policy-04.png)
