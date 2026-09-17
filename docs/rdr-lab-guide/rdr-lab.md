---
layout: default
title: "Regional Disaster Recovery Lab"
permalink: /rdr-lab-guide/rdr-lab/
nav_order: 7
parent: "IBM Fusion RDR Lab Guide"
---

# Regional Disaster Recovery Lab

This section guides you through the essential steps to implement and validate a regional disaster recovery (DR) strategy using OpenShift. These exercises simulate real-world DR scenarios to help ensure applications remain resilient and recoverable across regions.
## Create sample application
1. In the OpenShift GUI of local-cluster, navigate to the Projects screen by clicking on the Home (A) menu item in the left-hand side navigation pane and selecting the Projects (B) sub-item. When the Projects screen is shown, click the Create Project (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-01.png)

1. (A) Enter the value filebrowser in the Name text entry field and click the Create (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-02.png)

1. Verify that the project listed is set to the newly created filebrowser namespace. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-03.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-08.png)

1. Navigate to the filebrowser-all.yaml file hosted in GitHub, https://github.com/matt-levan/fusion-l4-material/blob/main/backuprestore-lab/filebrowser-all.yaml. Click the Copy raw file (A) button (the icon that looks like 2 overlapping windows) to copy the contents of the file to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-04.png)

1. Return to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the filebrowser resources.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-05.png)

1. The following information will be displayed listing all resources that were created and Creation status.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-06.png)

1. Navigate to the Route screen by clicking on the Network (A) menu item shown in the left-hand side navigation pane and selecting the Routes (B) sub-item. When the Routes screen is shown, click the URL Location (C) for the filebrowser route to open a new tab/window to the filebrowser application.
   > NOTE: It may take a minute or two for the filebrowser application to become fully online and accessible from the route screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-07.png)

1. Login to the File Browser application with Username (A): admin and Password (B): admin. Click the Login (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-08.png)

1. No files will be listed in the Filebrowser application.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-09.png)

1. Use New folder (A) and Upload file (B) to create some directories and upload a couple files. In the example shown, 2 directories were created, and 3 files were uploaded.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/create-sample-application-10.png)

## Assign DRPolicy to sample application
1. In the OpenShift GUI of local-cluster, navigate to the Advanced Cluster Manager by clicking on the local-cluster drop-down list (A) in the masthead and click on All clusters (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/import-second-cluster-04.png)

1. In the OpenShift GUI, navigate to the Disaster Recovery screen by clicking on the Data Services (A) menu item shown in the left-hand side navigation pane and selecting the Disaster Recovery (B) sub-item. Click on the Protected applications (C) tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-01.png)

1. Click on the Enroll application (A) button to open the application type list, and then selecting the value ACM discovered applications (B) from the drop-down list.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-02.png)

1. Click on the DR cluster (A) button to open the cluster list and then selecting the value local-cluster (B) from the drop-down list.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-03.png)

1. Scroll down until the Namespaces selection box appears and scroll through the list of applications or use the search box and select the filebrowser (A) namespace. Scroll down again until the Name field appears, (B) enter filebrowser in the Name text-entry field and click on the Next (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-04.png)

1. Click on the Add label expression (A) and the Add PVC label selector (B) to reveal the label selector expressions.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-05.png)

1. For BOTH the Label expressions and PVC label selectors, click on the Label (A) button to open the list of available labels. Then, from the drop-down list, select the value app (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-06.png)

1. For BOTH the Label expressions and PVC label selectors, click on the Values (A) button to open the list of available values. Then, from the drop-down list,  select the value filebrowser (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-07.png)

1. Click on the Next (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-08.png)

1. Click on the Disaster Recovery policy (A) button to open the policy list and then selecting the value ocp1-ocp2-dr (B) from the drop-down list. Click on the Next (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-09.png)

1. Click on the Save (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-10.png)

1. A DRPlacementControl (DRPC) custom resource has been created to protect the filebrowser application.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-11.png)

1. Click on the Overall sync status (A), in this example it is shown as Critical, to display the Sync status of the Application volumes (PVCs) and Kubernetes objects.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-12.png)

1. Within a few minutes the first asynchronous replication will occur for the Application volumes (PVCs) and the overall sync status will report as Healthy.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/assign-drpolicy-to-sample-application-13.png)

## Prepare secondary cluster for Failover/Relocate
This section prepares the secondary cluster for failover or relocation by creating a project with matching security settings to ensure seamless application transition.
1. In the OpenShift GUI on local-cluster, navigate to the Projects screen by clicking on the Home (A) menu item in the left-hand side navigation pane and selecting the Projects (B) sub-item. When the Projects screen is shown, click the filebrowser (C) project button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-01.png)

1. Click on the YAML (C) tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-02.png)

1. (A) Select all the text displayed in the YAML editor with CTRL-A (Windows/Linux) or CMD-A (Mac) and copy the contents to the clipboard with CTRL-C (Windows/Linux) or CMD-C (Mac) or browser Edit -> Copy button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-03.png)

1. In the OpenShift GUI on the ocp2 cluster, click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-04.png)

1. Click on the Import YAML (A) button from the drop-down list provided.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/reserve-cluster-local-cluster-08.png)

1. In the Import YAML screen use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the editor text entry field. Click the Expand (A) (looks like a > when collapsed) action for the managedFields associative array.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-05.png)

1. (A) Select all the lines associated with the managedFields associative array, (listed as lines 21 through 68 in the example shown), and delete them.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-06.png)

1. (A) In the metadata section, delete the lines for uid, resourceVersion, and creatitionTimestamp (listed as lines 5 through 7 in the example shown). (B) Finally delete everything from finalizers to the end of the file (listed as lines 22 through 25 in the example shown).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-07.png)

1. Click on the Create (A) button after all unneeded sections have been deleted to recreate the project from cluster local-cluster on cluster ocp2.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-secondary-cluster-for-failover-relocate-08.png)

## Failover application
1. Click on the Kebab (A) (displayed as three stacked dots) button to open the action menu.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/failover-application-01.png)

1. Click on the Initiate (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/failover-application-02.png)

1. Click on the View activity (A) button to display the activity status.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/failover-application-03.png)

1. In the OpenShift GUI of ocp2, navigate to the PersistenVolumeClaims screen by clicking on the Storage (A) menu item in the left-hand side navigation pane and selecting the PersistentVolumeClaims (B) sub-item. Verify that the PVCs have been failed over.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/failover-application-04.png)

1. In the OpenShift GUI of ocp2, navigate to the Pods screen by clicking on the Workloads (A) menu item in the left-hand side navigation pane and selecting the Pods (B) sub-item. Verify that the applications pods have been failed over and are running.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/failover-application-05.png)

## Prepare for failback
1. Once the failover has completed the following message will be displayed in the Activity description, “Clean up application resources on the failed cluser local-cluster to start the replication.” This is to enable replication from cluster ocp2 to cluster local-cluster.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-for-failback-01.png)

1. Open a new terminal window and connect to the cluster local-cluster bastion node via SSH. Run the following commands to delete all resources associated with the filebrowser application.
   ```bash
   export NS=filebrowser
   oc -n $NS delete all -l app=filebrowser
   oc -n $NS delete cm -l app=filebrowser
   oc -n $NS delete pvc -l app=filebrowser
   ```


   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-for-failback-02.png)

1. Once all resources have been deleted, check on the status of the replication of Application volumes (PVCs) and verify the active cluster is listed as cluster ocp2.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/prepare-for-failback-03.png)

Congratulations! You have just learned how to work with IBM Fusion Regional Disaster Recovery. This concludes the exercises in this lab guide.