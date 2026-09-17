---
layout: default
title: "Getting help and troubleshooting"
permalink: /getting-help-and-troubleshooting/
nav_order: 12
---

# Getting help and troubleshooting

This section provides information about getting help with your demo and some common troubleshooting topics.
## Pmcollector pod not running
Due to the limited number of resources created for this lab environment, sometimes the Storage Scale pmcollector pod will not be in a “Running” state. The following steps will allow the user to free up enough resources on a particular node.
1. Start by determining whether the Storage Scale pmcollector pod is not being scheduled due to insufficient resources. In the OpenShift GUI, navigate to the Workloads screen by clicking on the Workloads (A) menu item shown in the left-hand side navigation pane and selecting Pods (B), sub-item. Select the ibm-spectrum-scale project (C) in the OpenShift projector selector. Check if the ibm-scale-pmcollector-0 or 1 pod is showing a status of “Pending.”

![Screenshot]({{ site.baseurl }}/assets/images/image152.png)

1. In the example shown below, there are nodes with insufficient memory.

![Screenshot]({{ site.baseurl }}/assets/images/image153.png)

1. To determine which node Storage Scale created a localVolume persistentVolume on, click on the Storage (A) menu item in the left-hand side navigation pane and select the PersistentVolumesClaims (B) sub-item. In the example shown below, (C) worker-3-pmcollector was bound to persistentVolumeClaim (PVC) datadir-ibm-spectrum-scale-pmcollector-0 which is attached to pod ibm-spectrum-scale-pmcollector-0. (D) persistentVolume storage-2-pmcollector has been bound to a persistentVolumeClaim, which will result in node storage-2 not having enough resources for the pod to come online.

![Screenshot]({{ site.baseurl }}/assets/images/image154.png)

1. Navigate to Nodes screen by clicking on the Compute (A) menu item shown in the left-hand side navigation pane and selecting the Nodes (B) sub-item. Click on the node that was determined to have the unattached persistentVolume (which in this example is storage-2 (C)).

![Screenshot]({{ site.baseurl }}/assets/images/image155.png)

1. On the storage-1 Node details screen, an error is being displayed that indicates the node’s memory is overcommitted. That’s why pod pmcollector-1 is not coming online. Click on the Pods (A) tab.

![Screenshot]({{ site.baseurl }}/assets/images/image156.png)

1. All pods that are currently “Scheduled” and “Running” on this node are displayed on this screen. The Owner column can be used to determine which pods can be “Deleted” to make room for the ibm-scale-pmcollector-1 pod. The example shown here is highlighting the Owner column.

![Screenshot]({{ site.baseurl }}/assets/images/image157.png)

1. The 2-letter acronym that appears before each name in the Owner column is used to indicate the type of Kubernetes object that is managing the pods. In this example, Pod (A) (iptables-alerter) is being managed by a DaemonSet as denoted by DS and is not a candidate for “Deleting” as DaemonSets are typically scheduled to run on every node in the cluster. Pod (B) (isf-application-operator-controller-manager-65cbf8bf55-7tnzr) is a good candidate for “Deleting” as it is being managed by a replicaSet, as denoted by RS. It is okay to “Delete” a pod being managed by a replicaSet, as it will be scheduled and started on another Node in the cluster that has more resources.

![Screenshot]({{ site.baseurl }}/assets/images/image158.png)

1. Now that we have determined which pods are candidates for “Deleting”, the next step is to click the Pod context menu (A) (denoted by 3 stacked dots) and select Delete Pod (B).

![Screenshot]({{ site.baseurl }}/assets/images/image159.png)

1. Check the status of the “Unscheduled” pod (in this example, the ibm-scale-pmollector-1 pod) by clicking on the Workloads (A) menu item shown in the left-hand side navigation pane, selecting the Pods (B) sub-item, and checking the Status of the pod in question (in this example, the ibm-spectrum-scale pod).

![Screenshot]({{ site.baseurl }}/assets/images/image160.png)

1. Finally check on the status of the persistent volume (in this case, storage-2-pmcollector) by clicking on the Storage (A) menu item shown in the left-hand side navigation pane and selecting the PersistentVolumeClaims (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/image161.png)


![Screenshot]({{ site.baseurl }}/assets/images/image162.png)
