---
layout: default
title: "Spoke Cluster Labs"
permalink: /backup-restore-guide/spoke-cluster-labs/
nav_order: 6
parent: "Fusion Backup and Restore Lab Guide"
---

# Spoke cluster labs

A hub and spoke model enable a single administrator to manage backups for multiple applications that exist on the different clusters. The “hub” is the single location from where the administrator can login and manage all the applications on all the spoke and hub clusters. The hub location hosts the server and facilitates the Backup & Restore administrator to run backup and restore jobs across all clusters.
The hub includes all the Backup & Restore server components and agent components for backing up components on its own cluster. The “spoke” has only the Backup & Restore agent installed in it.
> The Backup & Restore hub maintains all scheduling, retention, policy handling, location management, and everything else from a management point of view. The agent or spoke takes care of requests to facilitate Backup & Restore jobs on that cluster.

## Configure a second cluster as a spoke
For reference, the cluster installed with the Backup & Restore service (agent and server) will be referred to as the hub cluster. The second cluster deployed will be referred to as the spoke cluster. For ease of connecting to the correct cluster use the following table.

| Cluster type | Console URL |
| --- | --- |
| Hub |  |
| Spoke |  |

## Install Backup and Restore agent
1. In the Fusion GUI on the hub cluster, navigate to the Topology screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Topology (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-01.png)

1. Click the Connect cluster (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-02.png)

1. Click the Use Fusion UI (A) tile.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-03.png)

1. Click the Copy snippet (A) button to copy the connection snippet to the clipboard.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-04.png)

1. In the Fusion GUI on the spoke cluster, navigate to the Services screen by clicking on the Services (A) menu item shown in the left-hand side navigation pane.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-05.png)

1. Click the Backup & Restore Agent (A) tile.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-06.png)

1. Click the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-07.png)

1. Paste the connection snippet copied from the hub cluster into the Hub Connection Snippet (A) text entry field using Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste option in the browser menu.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-08.png)

1. Open the drop-down list associated with “Storage class to be used to deploy the service” field and select the value ocs-storagecluster-ceph-rbd (A) from the list.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-09.png)

1. Click the Install (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-10.png)

1. Installing Backup & Restore Agent service… header will be displayed and Installing… percentage will progress as the required service is deployed.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-11.png)

1. Wait for the Backup & Restore Agent service to report as Healthy.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-12.png)

1. In the Fusion GUI on the hub cluster, navigate to the Topology screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Topology (B) sub-item. Verify the spoke cluster is listed as Connected and Healthy.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/install-backup-and-restore-agent-13.png)

## Prepare for spoke backup and restore
The spoke cluster requires access to the object bucket used during a backup operation and the Ceph cluster used earlier is not accessible from the spoke cluster. A new application, backup location, and backup policy will be created to enable restoring an application to the spoke cluster.
> IMPORTANT: In a hub and spoke configuration, all OpenShift clusters participating in backup and restore operations need to be able to reach the object storage bucket used.

### Create FDF ObjectBucketClaim for S3 backup location
This section describes the steps to create a FDF ObjectBucketClaim for configuring an S3 compatible backup location.
1. In the OpenShift GUI for the hub, navigate Navigate to the Object Storage screen by clicking on the Storage (A) menu item shown in the left-hand side navigation pane and selecting the Object Storage (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-01.png)

1. On the Object Storage page, click the Object Bucket Claims (A) tab.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-02.png)

1. Change to the ibm-spectrum-fusion-ns project using the Project selector. Refer to section OpenShift project selector on how to use the project selector.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-03.png)

1. Click on the Create ObjectBucketClaim (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-04.png)

1. (A) Enter the value fusion-backup-target in the ObjectBucketClaim Name text entry field.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-05.png)

1. Open the drop-down list associated with the “StorageClass” field and select the value openshift-storage.noobaa.io (A) from the list.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-06.png)

1. Keep the default BucketClass shown and click on the Create (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-07.png)

1. An Object Bucket Claim and associated Object Bucket will be created and information on the bucket will be displayed.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-08.png)

1. Scroll to the bottom of the ObjectBucketClaim details page and click the Reveal Values (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-09.png)

1. The information displayed below will be used in Section Create a new backup location for hub/spoke restore, Step 3. It may be easiest to copy the information below into a text file for use later.
> IMPORTANT: The Endpoint listed here will not be used during creation of the Backup location as it is internal to the cluster. The object bucket used for hub and spoke must be accessible by both clusters. Refer to the S3 Route section for instructions on identifying the external S3 endpoint.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-fdf-objectbucketclaim-for-s3-backup-location-10.png)

### Create a new backup location for hub/spoke restore
In this section a new backup location will be created on the hub cluster that is accessible by both clusters.
1. In the Fusion GUI for the hub, navigate to the Locations screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Locations (B) sub-item. When the Locations screen is shown, click the Add location + (C) button and follow the wizard to provide the S3 endpoint information and credentials.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-location-for-hub-spoke-restore-01.png)

1. (A) Enter hubspoke-bucket in the Location name text entry field and click the S3 Compliant (B) tile. Click Next (C) to enter connection details.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-location-for-hub-spoke-restore-02.png)

1. Enter the S3 endpoint and connection information from the Object Bucket Claim created in Section Create ODF ObjectBucketClaim for S3 backup location and click the Add (E) button. Additionally, the Show/Hide button on the Secret key can be used to display the text or hide it.
> NOTE: This configuration would not be appropriate for a production environment as the S3 target location should not be part of the Red Hat OpenShift Container Platform being backed up.

*Table  – Add a backup location details*

| Field name | Value | Callout |
| --- | --- | --- |
| Endpoint: | Refer to section S3 Route for information on how to gather the openshift-storage S3 route information. | (A) |
| Bucket: | Object Bucket Claim Bucket Name | (B) |
| Access Key: | Object Bucket Claim Access Key | (C) |
| Secret Key: | Object Bucket Claim Secret Key | (D) |


![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-location-for-hub-spoke-restore-03.png)

1. The newly added backup location should appear in a new tile and show as connected after a few seconds.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-location-for-hub-spoke-restore-04.png)

### Create a new backup policy for hub/spoke restore
A new backup policy will be created for use by the hub and spoke clusters using the newly created backup location.
1. In the Fusion GUI for the hub, navigate to the Policies screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Policies (B) sub-item. When the Policies screen is shown, click the Add policy + (C) button to create a new local object storage policy.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-policy-for-hub-spoke-restore-01.png)

1. (A) Enter hubspoke-backup in the Policy name text entry field, set Frequency to monthly (B), select 1 (C) for Choose a day, and specify a Time window for the backup to occur.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-policy-for-hub-spoke-restore-02.png)

1. Scroll down and click the Location on the Object storage (A) tile. Click the backup locations on the hubspoke-bucket (B) tile and click the Create policy (C) button to complete creation of the hubspoke-backup backup policy.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-policy-for-hub-spoke-restore-03.png)

1. The hubspoke-backup policy will now appear in the list of backup policies. This summary shows you the schedule of the policy, where the backup is stored, and which application uses the policy.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-new-backup-policy-for-hub-spoke-restore-04.png)

### Deploy application for spoke cluster restore
In this section a new application will be created in a new namespace that can be backed up in preparation of being restored to the hub cluster.
1. In the OpenShift GUI, navigate to the Projects screen by clicking on the Home (A) menu item in the left-hand side navigation pane and selecting the Projects (B) sub-item. When the Projects screen is shown, click the Create Project (C) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-01.png)

1. (A) Enter the value hubspoke in the Name text entry field and click the Create (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/deploy-application-for-spoke-cluster-restore-01.png)

1. Verify that the project listed is set to the newly created hubspoke namespace. Click the Import YAML (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/deploy-application-for-spoke-cluster-restore-02.png)

1. Navigate to the filebrowser-all.yaml file hosted in GitHub, https://github.com/matt-levan/fusion-l4-material/blob/main/backuprestore-lab/filebrowser-all.yaml. Click the Copy raw file (A) button (the icon that looks like 2 overlapping windows) to copy the contents of the file to the clipboard.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-04.png)

1. Return to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the editor (A) text entry field. Click the Create (B) button to create the filebrowser resources.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/deploy-application-for-spoke-cluster-restore-03.png)

1. The following information will be displayed listing all resources that were created and Creation status.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/deploy-application-for-spoke-cluster-restore-04.png)

1. Navigate to the Route screen by clicking on the Network (A) menu item shown in the left-hand side navigation pane and selecting the Routes (B) sub-item. When the Routes screen is shown, click the URL Location (C) for the filebrowser route to open a new tab/window to the filebrowser application.
> NOTE: It may take a minute or two for the filebrowser application to become fully online and accessible from the route screen.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/deploy-application-for-spoke-cluster-restore-05.png)

1. Login to the File Browser application with Username (A): admin and Password (B): admin. Click the Login (C) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-08.png)

1. No files will be listed in the Filebrowser application.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-09.png)

1. Use New folder (A) and Upload file (B) to create some directories and upload a couple files. In the example shown, 2 directories were created, and 3 files were uploaded.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-10.png)

### Assign hubspoke application to hubspoke-backup policy
In this section the hubspoke-backup policy will be assigned to the new hubspoke application.
1. In the Fusion GUI for the hub, navigate to the Applications page by clicking on the Applications (A) menu item shown in the left-hand side navigation pane. When the Applications screen is shown, select the checkbox (B) associated with the hubspoke application and click the Assign backup policy (C) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-hubspoke-application-to-hubspoke-backup-policy-01.png)

1. Select the checkbox (A) associated with the hubspoke-backup policy. Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the Save (B) button to complete assigning the policy. Allow enough time for the backup to complete before starting the restore process.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-hubspoke-application-to-hubspoke-backup-policy-02.png)

1. Wait for the backup to complete before continuing to the next section.
## Restore application to spoke cluster
This section outlines the steps required to restore an application to a spoke cluster using a previously created backup.
1. In the Fusion GUI of the hub cluster, navigate to the Backed up application screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Backed up applications (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-01.png)

1. Click the hubspoke (A) application name to open the application details page.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-02.png)

1. On the hubspoke application details page, click the Restore (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-03.png)

1. In Step 1 of the Restore hubspoke wizard, open the drop-down list associated with the Cluster destination (A) and select the spoke cluster (B) from the list of Target Clusters. Choose the cluster that does not display the **This cluster** tag.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-04.png)

1. Select the Use same project (A) tile and then click on the Next (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-05.png)

1. In Step 2 of the Restore hubspoke wizard, select the most recent (A) Backup time and click the Next (B) button to continue.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-06.png)

1. In Step 3 of the Restore hubspoke wizard, review the summary information for the restore, then click the Restore (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-07.png)

1. Click the Restore (A) button to confirm restore to the spoke cluster.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-08.png)

1. In the Fusion GUI on the hub cluster, navigate to the Jobs page by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the Jobs (B) sub-item. When the Jobs screen is shown, click the Restore (C) tab.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-09.png)

1. Click the restore-hubspoke-<date> (A) restore job name to access the restore job details page.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-10.png)

1. Monitor the status of the restore job until it is marked as Completed.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-11.png)

1. In the OpenShift GUI on the spoke cluster, navigate to the Pods page of the hubspoke project by clicking on the Workloads (A) menu item shown in the left-hand side navigation pane and selecting the Pods (B) sub-item. When the Pods screen is shown, click the Pod actions (C) (the icon that looks like 3 stacked dots) button and select the Delete Pod (D) option.
> NOTE: This step is a workaround for the application starting properly, but the route not working until the pod is restarted.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-12.png)

1. Click the Delete (A) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-13.png)

1. Wait for the pod status to report 1/1 Ready before moving on to the next step.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-14.png)

1. In the OpenShift GUI on the spoke cluster, navigate to the Routes page of the hubspoke project by clicking on the Networking (A) menu item shown in the left-hand side navigation pane and selecting the Routes (B) sub-item. When the Routes screen is shown, click the URL (C) link to open the filebrowser application in a new tab.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/restore-application-to-spoke-cluster-15.png)

1. Login to the filebrowser application and verify the uploaded files and directories have been restored to the spoke cluster.