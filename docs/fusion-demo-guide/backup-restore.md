---
layout: default
title: "Protect Workload – Backup/Restore"
permalink: /fusion-demo-guide/backup-restore/
nav_order: 9
parent: "IBM Fusion Demo Guide"
---

# Protect Containerized Workload – Backup/Restore

The following section will step through the process of installing the Fusion Backup & Restore service.
## Install Backup & Restore service
1. In the Fusion GUI, navigate to the Services screen by clicking on the **Services** (A) menu item shown in the left-hand side navigation pane.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-01.png)

1. Click the **Backup & Restore** (A) tile to open the install window for the Backup & Restore service.
   > NOTE: Do not click to the Backup & Restore Agent on the Services page.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-02.png)

1. Click the **Install** (A) button to begin the installation process for the Backup & Restore service.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-03.png)

1. Open the drop-down list associated with the “Storage class to be used to deploy the service” field and select the value **ocs-storagecluster-ceph-rdb** (A) from the list.
   > Note: The internal data catalog for the Backup & restore service requires a minimum of 200 GB of ReadWriteOnce (RWO) storage.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-04.png)

1. Click on the **Install** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-05.png)

1. The Backup & Restore service installation will show as Installing.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-06.png)

1. Once the Backup & Restore service installation has completed, a pop-out appears showing “Install complete!” and the service reports as being Healthy.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-07.png)

1. Notice that a new Backup & restore menu item has been added to the left-hand navigation pane in the IBM Fusion GUI.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-backup-restore-service-08.png)

The process to install the IBM Fusion Backup & Restore server and local agent has been completed. The Custom Resource YAML that would be used to do this without a GUI would be as follows. The YAML displayed here could be applied manually to install the IBM Backup & restore server and local agent via either the command-line interface or the Import YAML page.
> Note: The fusionServiceInstance custom resource YAML presented here is for informational purposes only. Installs during a Proof of Experience (PoX) may differ depending on the configuration and options selected.

```yaml
apiVersion: service.isf.ibm.com/v1
kind: FusionServiceInstance
metadata:
  name: ibm-backup-restore-service-instance
  namespace: ibm-spectrum-fusion-ns
spec:
  creator: User
  doInstall: true
  parameters:
  - name: namespace
    provided: false
    value: ibm-backup-restore
  - name: doInstall
    provided: false
    value: "true"
  - name: storageClass
    provided: true
    value: ocs-storagecluster-ceph-rbd
  serviceDefinition: ibm-backup-restore-service
  triggerUpdate: false
  updateServiceCRSpec: false
```

## Create Backup Locations and Policies
Applications have different requirements for backup frequency and retention. IBM Fusion uses Backup Policies to define and automate backup operations.
To configure backup and restore activities, go to the Backup & Restore section on the left-hand side navigation pane. To access the Overview page for Backup & Restore, click on the **Backup & Restore** (A) menu item shown in the left-hand side navigation pane and select the **Overview** (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-backup-locations-and-policies-01.png)

Select the **Topology** (A) sub-item of the Backup & Restore to view the Topology page. Here, you can determine if the cluster has been configured for backup and restore. This screen will also display additional Spoke clusters if a hub-and-spoke setup was configured.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-backup-locations-and-policies-02.png)

IBM Fusion backups can use one of two methods: local snapshots that are stored on the OpenShift cluster or backups that are stored at an external object storage location. Before creating backup policies and backups, you must configure a backup location.
### Backup location

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-01.png)

1. S3 Backup Bucket

Create an S3 backup location using IBM Data Foundation. Data Foundation must be installed and setup. In the OpenShift Console, navigate to **Data Foundation → Object Storage** and select the tab "Object Bucket Claims".

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-02.png)

1. Click create ObjectBucketClaim

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-03.png)

1. Once the bucket claim is created, scroll down and reveal values

We will use the “Bucket Name”, “Access Key” and “Secret Key”.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-04.png)

1. Next we need to get the external endpoint

Navigate to “networking”  “routes” and choose all projects and search for “S3”
1. There you will find the correct route to use.
1. In the Fusion GUI, navigate to the Locations screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Locations** (B) sub-item. When the Locations screen is shown, click the **Add location +** (C) button and use the wizard to provide the appropriate S3 endpoint information and credentials.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-05.png)


   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-06.png)

1. (A) Enter object1 in the Location name text entry field and click the **MCG/NooBaa** (B) tile. Then, click Next (C) to enter the connection details.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-07.png)

1. Enter the S3 endpoint and connection collected in the previous steps

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-location-08.png)

1. The newly added backup location should appear in a new tile and be connected after a few seconds.
### Backup policies
A backup policy is a set of rules and schedules that define how and when data is backed up. It outlines the frequency of backups, the type of data to be backed up, the retention period, and the storage location. The Backup & Restore service allows you to create and manage backup policies to ensure your data is protected according to your specific needs.
The Policies page lists all policies. You can search for policy records based on the backup location or other keywords, configure the table display, and perform actions like viewing, editing, or deleting policies from the ellipsis overflow menu.
1. In the Fusion GUI, navigate to the Policies screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Policies** (B) sub-item. When the Policies screen is shown, click the **Add policy +** (C) button to configure a backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-policies-01.png)

1. (A) Enter daily-snapshot in the Policy Name text entry field, set Frequency to Daily and specify a Time window for the backup to occur. Then, select the In **place snapshot** (B) Backup location tile. Finally, click the Next (C) button to create the new daily-snapshot backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-policies-02.png)

1. The daily-snapshot policy will now appear in the list of backup policies. Next, we will create a weekly-backup policy using object storage as the backup location. Click the **Add policy +** (A) button to begin.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-policies-03.png)

1. (A) Enter weekly-backup in the Policy name text entry field, set **Frequency to weekly** (B), select **Sunday** (C) for Schedule, and specify a Time window for the backup to occur. Select the **Object Storage** (D) Backup location tile to **pick the backup location object1** (E). Click the Create **policy** (F) button to complete creation of the weekly-backup backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-policies-04.png)

1. The Policies summary screen shows where backups are stored, the schedule for each policy, and the application that uses the policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/backup-policies-05.png)

When installing IBM Fusion, the administrator chooses to use a specific Storage Class from the available classes in the OpenShift cluster. This storage class is used by Fusion for the In Place Snapshot. The snapshots are only saved in place and can be lost if there is a problem with the OpenShift Cluster.
To avoid losing a backup, use an Object Storage backup location.
## Create a workload
In this section, you’ll learn how to create a basic application to demonstrate core functionality and prepare for backup and restore operations.
1. In the OpenShift GUI, navigate to the Projects screen by clicking on the **Home** (A) menu item in the left-hand side navigation pane and selecting the **Projects** (B) sub-item. When the Projects screen is shown, click the Create **Project** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-01.png)

1. (A) Enter the value filebrowser in the Name text entry field and click the Create (B) button.
   > Important: If this demo guide is being used for the IBM Fusion Level 3 stand and deliver demonstration, please note that the IBM Fusion Demo Script (Level 3) will create an application using the bankapp project instead of filebrowser. Regardless of the project name used—filebrowser or bankapp—the same application is deployed.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-02.png)

1. Verify that the project listed is set to the newly created filebrowser namespace. Click the Quick create (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-03.png)

1. Click on the **Import YAML** (A) button from the drop-down list provided.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-04.png)

1. Navigate to the filebrowser-all.yaml file hosted in GitHub, [https://github.com/matt-levan/fusion-l4-material/blob/main/backuprestore-lab/filebrowser-all.yaml](https://github.com/matt-levan/fusion-l4-material/blob/main/backuprestore-lab/filebrowser-all.yaml). Click the Copy **raw file** (A) button (the icon that looks like 2 overlapping windows) to copy the contents of the file to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-05.png)

1. Return to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the **editor** (A) text entry field. Click the Create (B) button to create the filebrowser resources.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-06.png)

1. The following information will be displayed listing all resources that were created and Creation status.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-07.png)

1. Navigate to the Route screen by clicking on the **Network** (A) menu item shown in the left-hand side navigation pane and selecting the **Routes** (B) sub-item. When the Routes screen is shown, click the **URL Location** (C) for the filebrowser route to open a new tab/window to the filebrowser application.
   > NOTE: It may take a minute or two for the filebrowser application to become fully online and accessible from the route screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-08.png)

1. Login to the File Browser application with **Username** (A): admin and **Password** (B): admin. Click the **Login** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-09.png)

1. No files will be listed in the Filebrowser application.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-10.png)

1. Use **New folder** (A) and **Upload file** (B) to create some directories and upload a couple files. In the example shown, 2 directories were created, and 3 files were uploaded.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-11.png)

## Assign Policy to application
The OpenShift Cluster can host many application workloads; IBM Fusion provides a simple graphical user interface (GUI) to assign backup policies to applications and automate their protection.
> There are two (2) methods for interacting with applications in the Fusion GUI. The Applications menu item on the left-hand side navigation pane shows only the applications local to the cluster. The Backed up applications sub-item under the Backup & restore menu allows for assigning policies to local and remote clusters. For this lab either option can be used.

### Assign policy using applications menu item
This sub-section describes the process for managing backups of applications deployed in the local cluster using the Applications page.
1. Navigate to the Application pane by clicking on the **Applications** (A) menu item on the left-hand side navigation pane.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-applications-menu-item-01.png)

1. Select the **filebrowser application checkbox** (A) and click the Assign **backup policy** (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-applications-menu-item-02.png)

1. Select **both the daily-snapshot checkbox** (A) and **weekly-backup checkbox** (B). Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the **Save** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-applications-menu-item-03.png)

1. A confirmation window will appear in the upper-right corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications.
### Assign policy using Backed up applications menu item
This sub-section describes the process for managing backups of applications deployed across both hub and spoke clusters using the Backup up applications page.
1. Navigate to the Backed up applications pane in the IBM Fusion UI by clicking **Backup & Restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Backed up applications** (B) sub-item. You should now see a page listing the applications that have been backed up, together with application details and assigned backup policies. Each line represents an OpenShift namespace which can contain a different application/workload.
1. If you want to find a specific namespace, you can use the search toolbar present on the page.
1. You can assign a backup policy to a namespace by clicking **Protect apps +** (C) on the right side. This will launch the Protect applications wizard.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-backed-up-applications-menu-item-01.png)

1. The Protect applications wizard can be used to backup applications locally and in hub and spoke configurations. Select the **local cluster** (A) from the drop-down list, and a list of unprotected applications will populate in the list below. Next select, **filebrowser** (B) from the unprotected applications list. Finally click on the Next (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-backed-up-applications-menu-item-02.png)

1. On the Assign policies, you can select one or more policies to attach to the application and if backup should start right after applying the policies. Select **both the daily-snapshot** (A) and **weekly-backup** (B) policies. Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the Assign (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-backed-up-applications-menu-item-03.png)

1. A confirmation window will appear in the right-hand upper corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/assign-policy-using-backed-up-applications-menu-item-04.png)

## Monitor backup status
Depending on the method used to Assign a backup policy, the Pending and In progress screens will be slightly different. Selecting the application name will display a page with the same information.
1. After a short period of time the Backup status will change from Pending to an In progress status, until it is Completed.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/monitor-backup-status-01.png)

1. Status of each policy can be checked by going into the application pane and clicking the **Backups** (A) tab. In the example shown below, the daily-snapshot policy has Completed and the weekly-backup is Snapshot in progress.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/monitor-backup-status-02.png)

## Application restore
This section describes the steps required to restore an application from a previously created backup.
1. From the Applications or Backed up applications page, click the application name to open its Overview page.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-01.png)

1. The Backups tab shows all the backups created for this application and lets you choose the backup you want to restore from.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-02.png)

1. A restore action can also be started by using buttons at top of the page. Click on the **Restore** (A) button located at the top of the pane.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-03.png)

1. The wizard presents the choice to restore to the same cluster or to a different cluster, if you have a hub-spoke setup. Open the drop-down list associated with the “Target cluster” field and select the This **cluster** (A) item from the list.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-04.png)

1. The restore wizard also provides a choice to restore over the same project, an existing project, or to a new project. Select Create a **new project** (A) and (B) enter filebrowser2 in the Project name text entry field. Then, click on the Next (C) button to select the backup to restore.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-05.png)

1. Choose the **Backup time** (A) you want to restore from, from the list of backups provided – note that if you want multiple backups to choose from, you must first create them. Then click on the Next (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-06.png)

1. Keep all the default settings shown and click on the **Restore** (A) button. A Summary (B) is displayed on the right pane with details on what the Before restore and After restore states will be.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-07.png)

1. Confirm the restore by clicking on the **Restore** (A) button in the final dialog box.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-08.png)

1. Watch the restore progress. Item (A) is the Restore job that has been scheduled; Item (B) will update as the restore operation progresses. The Restore process can also be tracked on the Jobs page. The Jobs page can be accessed by clicking on the Backup & restore menu item shown in the left-hand side navigation pane and selecting the Jobs sub-item. On the Jobs page, click the Restore tab to track progress.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-09.png)

1. In the OpenShift Console, navigate to the Pods page by clicking on the **Workloads** (A) menu item shown in the left-hand side navigation pane and selecting the click **Pods** (B) sub-item. Then click the **project selector** (C) and choose **filebrowser2** (D) from the projects drop down menu. Refer to section Error! Reference source not found. on how to use the project selector.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-10.png)

1. Watch the application being restored and the new pods created for the restored application.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-11.png)

1. Navigate to the PersistenVolumesClaims screen by selecting the **Storage** (A) menu item shown in the left-hand side navigation pane and selecting the **PersistentVolumeClaims** (B) sub-item. The newly restored PVCs are shown.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-12.png)

1. Navigate to the Routes screen by clicking on the **Networking** (A) menu item shown in the left-hand side navigation pane and selecting the **Routes** (B) sub-item. When the Routes screen is shown, click on the **Location** (C) URL to launch the filebrowser application in a new tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/application-restore-13.png)

1. Login to the File Browser application with the **Username** (A): admin and **Password** (B): admin. Click **Login** (C). Review that the files added earlier have been restored to a new application project.

   ![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/create-a-workload-09.png)
