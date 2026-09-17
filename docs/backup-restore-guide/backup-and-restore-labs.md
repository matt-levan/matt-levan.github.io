---
layout: default
title: "Backup and Restore Labs"
permalink: /backup-restore-guide/backup-and-restore-labs/
nav_order: 5
parent: "Fusion Backup and Restore Lab Guide"
---

# Backup and restore labs

This section covers how to create backup locations and policies, perform backup and restore operations using the default recipe, and utilize IBM Fusion recipes for application-consistent backups.
## Create Backup Locations and Policies
Applications have different requirements for backup frequency and retention. IBM Fusion uses Backup Policies to define and automate backup operations.
To configure backup and restore activities, go to the Backup & Restore section on the left-hand side navigation pane. To access the Overview page for Backup & Restore, click on the **Backup & Restore** (A) menu item shown in the left-hand side navigation pane and select the **Overview** (B) sub-item.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-01.png)

Select the **Topology** (A) sub-item of the Backup & Restore to view the Topology page. Here, you can determine if the cluster has been configured for backup and restore. This screen will also display additional Spoke clusters if a hub-and-spoke setup was configured.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-02.png)

IBM Fusion backups can use one of two methods: local snapshots that are stored on the OpenShift cluster or backups that are stored at an external object storage location. Before creating backup policies and backups, you must configure a backup location.S3 Backup Bucket

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-03.png)

Data Foundation must be installed and setup. In the OpenShift Console, navigate to “Data Foundation”  “object storage” and select the tab “Object Bucket Claims”

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-04.png)

Click create ObjectBucketClaim

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-05.png)


![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-backup-locations-and-policies-06.png)

Once the bucket claim is created, scroll down and reveal valuesWe will use the “Bucket Name”, “Access Key” and “Secret Key”. Next we need to get the external endpointNavigate to “networking”  “routes” and choose all projects and search for “S3”
There you will find the correct route to use.
### Backup location
1. In the Fusion GUI, navigate to the Locations screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Locations** (B) sub-item. When the Locations screen is shown, click the **Add location +** (C) button and use the wizard to provide the appropriate S3 endpoint information and credentials.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-location-01.png)


   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-location-02.png)

1. (A) Enter object1 in the Location name text entry field and click the **MCG/NooBass** (B) tile. Then, click Next (C) to enter the connection details.
1. Enter the S3 endpoint and connection information collected in the previous steps.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-location-03.png)

1. The newly added backup location should appear in a new tile and be connected after a few seconds.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-location-04.png)

### Backup policies
A backup policy is a set of rules and schedules that define how and when data is backed up. It outlines the frequency of backups, the type of data to be backed up, the retention period, and the storage location. The Backup & Restore service allows you to create and manage backup policies to ensure your data is protected according to your specific needs.
The Policies page lists all policies. You can search for policy records based on the backup location or other keywords, configure the table display, and perform actions like viewing, editing, or deleting policies from the ellipsis overflow menu.
1. In the Fusion GUI, navigate to the Policies screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Policies** (B) sub-item. When the Policies screen is shown, click the **Add policy +** (C) button to configure a backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-policies-01.png)

1. (A) Enter daily-snapshot in the Policy Name text entry field, set Frequency to Daily and specify a Time window for the backup to occur. Then, select the In **place snapshot** (B) Backup location tile. Finally, click the Next (C) button to create the new daily-snapshot backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-policies-02.png)

1. The daily-snapshot policy will now appear in the list of backup policies. Next, we will create a weekly-backup policy using object storage as the backup location. Click the **Add policy +** (A) button to begin.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-policies-03.png)

1. (A) Enter weekly-backup in the Policy name text entry field, set **Frequency to weekly** (B), select **Sunday** (C) for Schedule, and specify a Time window for the backup to occur. Select the **Object Storage** (D) Backup location tile to **pick the backup location object1** (E). Click the Create **policy** (F) button to complete creation of the weekly-backup backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-policies-04.png)

1. The Policies summary screen shows where backups are stored, the schedule for each policy, and the application that uses the policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-policies-05.png)

To avoid losing a backup, use an Object Storage backup location.
## Create a simple application
In this section, you’ll learn how to create a basic application to demonstrate core functionality and prepare for backup and restore operations.
1. In the OpenShift GUI, navigate to the Projects screen by clicking on the **Home** (A) menu item in the left-hand side navigation pane and selecting the **Projects** (B) sub-item. When the Projects screen is shown, click the Create **Project** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-01.png)

1. (A) Enter the value filebrowser in the Name text entry field and click the Create (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-02.png)

1. Verify that the project listed is set to the newly created filebrowser namespace. Click the **Import YAML** (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-03.png)

1. Navigate to the filebrowser-all.yaml file hosted in GitHub, https://github.com/matt-levan/fusion-l4-material/blob/main/backuprestore-lab/filebrowser-all.yaml. Click the Copy **raw file** (A) button (the icon that looks like 2 overlapping windows) to copy the contents of the file to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-04.png)

1. Return to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the **editor** (A) text entry field. Click the Create (B) button to create the filebrowser resources.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-05.png)

1. The following information will be displayed listing all resources that were created and Creation status.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-06.png)

1. Navigate to the Route screen by clicking on the **Network** (A) menu item shown in the left-hand side navigation pane and selecting the **Routes** (B) sub-item. When the Routes screen is shown, click the **URL Location** (C) for the filebrowser route to open a new tab/window to the filebrowser application.
   > NOTE: It may take a minute or two for the filebrowser application to become fully online and accessible from the route screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-07.png)

1. Login to the File Browser application with **Username** (A): admin and **Password** (B): admin. Click the **Login** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-08.png)

1. No files will be listed in the Filebrowser application.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-09.png)

1. Use **New folder** (A) and **Upload file** (B) to create some directories and upload a couple files. In the example shown, 2 directories were created, and 3 files were uploaded.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-10.png)

## Assign Policy to application
The OpenShift Cluster can host many application workloads; IBM Fusion provides a simple graphical user interface (GUI) to assign backup policies to applications and automate their protection.
> There are two (2) methods for interacting with applications in the Fusion GUI. The Applications menu item on the left-hand side navigation pane shows only the applications local to the cluster. The Backed up applications sub-item under the Backup & restore menu allows for assigning policies to local and remote clusters. For this lab either option can be used.

### Assign policy using applications menu item
This sub-section describes the process for managing backups of applications deployed in the local cluster using the Applications page.
1. Navigate to the Application pane by clicking on the **Applications** (A) menu item on the left-hand side navigation pane.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-applications-menu-item-01.png)

1. Select the **filebrowser application checkbox** (A) and click the Assign **backup policy** (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-applications-menu-item-02.png)

1. Select **both the daily-snapshot checkbox** (A) and **weekly-backup checkbox** (B). Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the **Save** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-applications-menu-item-03.png)

1. A confirmation window will appear in the upper-right corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications.
### Assign policy using Backed up applications menu item
This sub-section describes the process for managing backups of applications deployed across both hub and spoke clusters using the Backup up applications page.
1. Navigate to the Backed up applications pane in the IBM Fusion UI by clicking **Backup & Restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Backed up applications** (B) sub-item. You should now see a page listing the applications that have been backed up, together with application details and assigned backup policies. Each line represents an OpenShift namespace which can contain a different application/workload.
1. If you want to find a specific namespace, you can use the search toolbar present on the page.
1. You can assign a backup policy to a namespace by clicking **Protect apps +** (C) on the right side. This will launch the Protect applications wizard.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-backed-up-applications-menu-item-01.png)

1. The Protect applications wizard can be used to backup applications locally and in hub and spoke configurations. Select the **local cluster** (A) from the drop-down list, and a list of unprotected applications will populate in the list below. Next select, **filebrowser** (B) from the unprotected applications list. Finally click on the Next (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-backed-up-applications-menu-item-02.png)

1. On the Assign policies, you can select one or more policies to attach to the application and if backup should start right after applying the policies. Select **both the daily-snapshot** (A) and **weekly-backup** (B) policies. Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the Assign (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-backed-up-applications-menu-item-03.png)

1. A confirmation window will appear in the right-hand upper corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/assign-policy-using-backed-up-applications-menu-item-04.png)

## Monitor backup status
Depending on the method used to Assign a backup policy, the Pending and In progress screens will be slightly different. Selecting the application name will display a page with the same information.
1. After a short period of time the Backup status will change from Pending to an In progress status, until it is Completed.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/monitor-backup-status-01.png)

1. Status of each policy can be checked by going into the application pane and clicking the **Backups** (A) tab. In the example shown below, the daily-snapshot policy has Completed and the weekly-backup is Snapshot in progress.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/monitor-backup-status-02.png)

## Application restore
This section describes the steps required to restore an application from a previously created backup.
1. From the Applications or Backed up applications page, click the application name to open its Overview page.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-01.png)

1. The Backups tab shows all the backups created for this application and lets you choose the backup you want to restore from.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-02.png)

1. A restore action can also be started by using buttons at top of the page. Click on the **Restore** (A) button located at the top of the pane.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-03.png)

1. The wizard presents the choice to restore to the same cluster or to a different cluster, if you have a hub-spoke setup. Open the drop-down list associated with the “Target cluster” field and select the This **cluster** (A) item from the list.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-04.png)

1. The restore wizard also provides a choice to restore over the same project, an existing project, or to a new project. Select Create a **new project** (A) and (B) enter filebrowser2 in the Project name text entry field. Then, click on the Next (C) button to select the backup to restore.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-05.png)

1. Choose the **Backup time** (A) you want to restore from, from the list of backups provided – note that if you want multiple backups to choose from, you must first create them. Then click on the Next (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-06.png)

1. Keep all the default settings shown and click on the **Restore** (A) button. A Summary (B) is displayed on the right pane with details on what the Before restore and After restore states will be.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-07.png)

1. Confirm the restore by clicking on the **Restore** (A) button in the final dialog box.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-08.png)

1. Watch the restore progress. Item (A) is the Restore job that has been scheduled; Item (B) will update as the restore operation progresses. The Restore process can also be tracked on the Jobs page. The Jobs page can be accessed by clicking on the Backup & restore menu item shown in the left-hand side navigation pane and selecting the Jobs sub-item. On the Jobs page, click the Restore tab to track progress.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-09.png)

1. In the OpenShift Console, navigate to the Pods page by clicking on the **Workloads** (A) menu item shown in the left-hand side navigation pane and selecting the click **Pods** (B) sub-item. Then click the **project selector** (C) and choose **filebrowser2** (D) from the projects drop down menu. Refer to section OpenShift project selector on how to use the project selector.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-10.png)

1. Watch the application being restored and the new pods created for the restored application.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-11.png)

1. Navigate to the PersistenVolumesClaims screen by selecting the **Storage** (A) menu item shown in the left-hand side navigation pane and selecting the **PersistentVolumeClaims** (B) sub-item. The newly restored PVCs are shown.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-12.png)

1. Navigate to the Routes screen by clicking on the **Networking** (A) menu item shown in the left-hand side navigation pane and selecting the **Routes** (B) sub-item. When the Routes screen is shown, click on the **Location** (C) URL to launch the filebrowser application in a new tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/application-restore-13.png)

1. Login to the File Browser application with the **Username** (A): admin and **Password** (B): admin. Click **Login** (C). Review that the files added earlier have been restored to a new application project.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-08.png)

## Create an application with Fusion recipe
When you protect an application with Backup & Restore service, a default backup and restore workflow is used to protect an application. But while the backup and restore workflow is sufficient for some applications, there are some instances where you need to create a custom workflow for the backup and restore process to produce an application consistent backup. Recipes are used to create a custom workflow for the backup and restore process.
> Types of consistency:
> No consistency: Snapshots are not consistent. If an application uses 4 persistent volumes (PV), it rolls through these temporally. At point in time A, a snapshot is taken of one of the PVs. Then a snapshot is taken of the second, and then the third, and so on. Even with scripts, the PVs will not be backed up at the same time. Therefore, they will not be consistent with one another.
> Consistency breaks if the application is doing active input/output (IO) to the persistent volumes. If the application is writing to the volumes in the middle of a snapshot and another snapshot of another volume was taken when the write was finished, it ends up being inconsistent.
> Crash consistent: IBM Fusion supports crash consistency. This ensures that all the snapshots of the PVs are taken at the exact same time so that they are consistent, even after a disaster. Crash consistency means that if, for example, a rack was to be unplugged and all the servers were to lose power at the same time, then all those PVs are consistent with one another because the writes to them stopped at the exact same time.
> Application consistent: If a client has an application that has many, many persistent volumes, and that application is busy reading and writing to its PVs, there needs to be a way to instruct the application to stop writing or to pause. The application can complete any tasks in process but then stop briefly to allow a snapshot of the PVs to be taken. Then, the application can be instructed to resume. This is like quiescing a database.
> With application consistency, it’s possible to restore an application to another cluster without having data stuck in an I/O buffer, thus ensuring the application is back running in the exact state it was in at the time of the backup. Application consistency also means that there needs to be a workflow to back up those applications in a certain order, and Fusion provides this with recipes.
> Application consistent backups are important because they ensure that important files and data are saved in a way that keeps them safe and undamaged. This means that if something goes wrong, like a computer crash or a power outage, clients can restore their files and data to the way they were before the event, without losing any important information.

1. In the OpenShift GUI, navigate to the Projects screen by clicking on the **Home** (A) menu item in the left-hand side navigation pane and selecting the **Projects** (B) sub-item. When the Projects screen is shown, click on the Create **Project** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-a-simple-application-01.png)

1. (A) Enter the value pacman in the Name text entry field and click on the Create (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-01.png)

1. Verify that the project listed is set to the newly created pacman namespace. Click the **Import YAML** (A) (the icon that looks like a + sign) button in the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-02.png)

1. Navigate to the pacman-all.yaml file hosted in GitHub, https://github.com/matt-levan/application-samples/blob/main/pacman/pacman-all.yaml. Click the Copy **raw file** (A) (the icon that looks like 2 overlapping windows) button to copy the contents of the file to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-03.png)

1. Navigate back to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or the browser Edit -> Paste function to paste the contents of the clipboard into the **editor** (A) text entry field. Click the Create (B) button to create the pacman application resources.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-04.png)

1. The following information will be displayed, listing all the resources that were created.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-05.png)

1. Navigate to the Routes screen by clicking on the **Network** (A) menu item shown in the left-hand side navigation pane and selecting the **Routes** (B) sub-item. When the Routes screen is shown, click the **URL Location** (C) for the pacman route to open a new tab/window to the pacman application.
   > NOTE: It may take a few minutes for the pacman application to become fully online and accessible from the route screen.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-06.png)

1. The following page will be displayed. Select anywhere in the playable window to begin a new game of Pacman.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-07.png)

1. Play a round (or two) of Pacman until the Game Over screen is displayed. (A) Enter your name in the Total Score text entry field and click the **save** (B) button when finished.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-08.png)

1. Click on the View **Highscore List** (A) button to see a list of high scores that have been stored in the Mongo database.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-09.png)

1. Example of a high score list is shown below.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-10.png)

1. Navigate to the mongodb-image-based-backup-restore.yaml file hosted in GitHub, https://github.com/IBM/storage-fusion/blob/master/backup-restore/recipes/MongoDB/mongodb-image-based-backup-restore.yaml. Select the Copy **raw file** (A) (the icon that looks like 2 overlapping windows) button to copy the contents of the file to the clipboard.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-11.png)

   > You need a recipe to create a custom workflow for the backup and restore process. The recipe used during this lab is designed for a standalone MongoDB instance running as a Deployment. There are additional recipes available in the [IBM Fusion public GitHub repository](https://github.com/IBM/storage-fusion) for many common applications and databases.
   > The recipe custom resource has three basic specification elements:
   > Groups: A group defines a set of resources or PVCs that are processed together within a backup or restore. For example, a group can be a subset of specific resources that are specified with an exclude statement or an include statement.
   > In the MongoDB script the volumes and resources, excluding event, pods, and replicasets, are included in the backup.
   > Hooks: A hook can be used to start external scripts before and after snapshots, scale deployments up and down, or wait for certain conditions. For example, pods starting up and so on.
   > In the MongoDB script there are two hooks provided. The first hook checks to validate that the number of replicas expected by the deployment are equal to the number of replicas that are Ready. The second hook includes the logic to put the Mongodb database into and take it out of hot backup mode allowing for an application consistent backup of the database.
   > Workflows: A workflow defines the sequence of steps for a backup or restore operation, specifically the order in which the groups of resources and PVCs must be processed and any hooks that need to be applied.
   > In the MongoDB script there are two workflows provided for the backup and restore sequence. In the backup workflow, the MongoDB resources are backed up, then the MongoDB is put into hot backup mode. After the MongoDB has entered hot backup mode, the volumes are backed up. Finally, the last step is to take the MongoDB database out of hot backup mode. In the restore section, the resources are restored such that the MongoDB volumes are created before the resources, then the restore waits until all expected replicas are Ready.

1. Click the **Import YAML** (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-12.png)

1. Navigate back to the OpenShift GUI and use Ctrl-V (windows), CMD-V (Mac) or the browser Edit -> Paste function to paste the contents of the clipboard into the **editor** (A) text entry field. Click the Create (B) button to create the recipe.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-13.png)

1. In the Fusion GUI, navigate to the Applications screen by clicking on the **Applications** (A) menu item shown in the left-hand side navigation pane. When the Applications screen is shown, select the **pacman checkbox** (B) and click on the Assign **backup policy** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-14.png)

1. Select the **weekly-backup policy** (A) and use the **Backup up now** (B) toggle to disable the initial backup (shown as gray when disabled). Click the **Save** (C) button.
   > IMPORTANT: Set the Backup up now option to disabled (indicated by the absence of a green checkmark) to prevent an initial backup. The Pacman application does not generate sufficient changes in the MongoDB database and performing an initial backup without the appropriate recipe may result in restore failures when using Change Block Tracking (CBT).

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-15.png)

1. The Pacman application is now associated with the weekly-backup policy.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-16.png)

1. In the OpenShift GUI, navigate to the Search screen by clicking on the **Home** (A) menu item shown in the left-hand side navigation pane and selecting the **Search** (B) sub-item.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-17.png)

1. Change to the ibm-spectrum-fusion-ns project, if not already there. Refer to section OpenShift project selector on how to use the project selector. Open the drop-down list associated with the **“Resources”** (A) field and (B) enter policyassignment in the search box text entry field (displayed with a magnifying glass). Select the **PolicyAssignment** (C). Click anywhere outside the drop-down list to dismiss the window.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-18.png)

1. Click on the PolicyAssignment associated with the pacman application that was just created. The syntax for the policy is, <application>-<backup policy>-<backup cluster name>. In the example shown here, the PolicyAssignment name is pacman-weekly-backup-apps.66d86bd0694f19a4a8b069f1.ocp.techzone.ibm.com.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-19.png)

1. Click the **YAML** (A) tab.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-20.png)

1. The recipe created in Step 13 will now be added to the Pacman weekly-backup PolicyAssignment.
   > The recipe syntax is as follows for use in a PolicyAssignment.
   > spec:  recipe:    apiVersion: spp-data-protection.isf.ibm.com/v1alpha1    name: RECIPE_NAME    namespace: RECIPE_NAMESPACE
   > RECIPE_NAME is the name of the recipe as specified in the Recipe CR.RECIPE_NAMESPACE is the namespace where the Recipe CR is located.

1. Enter the following 4 lines before status and after runNow as shown in the screenshot. The spacing included in the text entered is needed to conform to the YAML used by OpenShift. Do not enter the values (X spaces) and instead press the spacebar the number of times indicated if the editor does not auto-indent.
   > NOTE: for readability the metadata and status information have been collapsed using the expand/collapse buttons on the left-hand side of the editor.

   ```
   `(2 spaces) recipe:`
   `(4 spaces) ``apiVersion``: spp-data-protection.isf.ibm.com/v1alpha1`
   `(4 spaces) name: ``mongodb``-image-based-backup-restore-recipe`
   `(4 spaces) namespace: ``ibm``-spectrum-fusion-ns`
   ```

Click the **Save** (A) button after the 4 new lines have been added.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-21.png)

1. Change to the pacman project using the Project selector if necessary. Refer to section OpenShift project selector on how to use the project selector. Navigate to the Pods screen by clicking on the **Workload** (A) menu item shown in the left-hand side navigation pane and selecting the **Pods** (B) sub-item. Click on the **mongodb-XXXXXXXXXX-YYYYY pod** (C) to open the pod details page.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-22.png)

1. Click the **Logs** (A) tab and select **Wrap lines** (B) to improve readability. Scroll to the bottom of the logs if necessary. Leave this window open for now as we will return to it after a new backup has been run using the updated PolicyAssignment with the newly attached recipe.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-23.png)

1. In the Fusion GUI, navigate to the Applications page by clicking on the **Applications** (A) menu item shown in the left-hand side navigation pane. When the Application screen is shown, select the **pacman application** (B) checkbox and click on the **Back up now** (C) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-24.png)

1. Click on the **Back up** (A) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-25.png)

1. Navigate to the Jobs screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Jobs** (B) sub-item. When the Jobs screen is shown, click on the **pacman-weekly-backup-<cluster name> job** (C) to open the job details page.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-26.png)

1. Verify that the Backup sequence includes hooks provided in the backup recipe by expanding the Backup sequence section of the Jobs details.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-27.png)

1. Additional details can be displayed by selecting the Log view on the Backup Jobs page.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-28.png)

1. In the OpenShift GUI, navigate back to the mongodb Pod logs and look for the fsyncLock command to be executed. You may need to scroll back to find the COMMAND being run.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-29.png)

1. Continue investigating the mongodb logs and find the fsyncUnlock log entry.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/create-an-application-with-fusion-recipe-30.png)

## Backup service protection
The IBM Storage Fusion Backup & Restore service protection involves the backup of the control plane to a S3 object bucket. In the event of cluster failure, you can use this feature to restore the Backup & Restore service to another cluster. In this section you will configure service protection and run the initial service backup.
> Service protection is just for backup/restore on the hub cluster and not for other configurations that exist in IBM Storage Fusion. For example, Red Hat OpenShift Container Platform cluster, disaster recovery, Red Hat OpenShift Data Foundation.

1. In the Fusion GUI, navigate to the Service protection page by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting **Service protection** (B) sub-item.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-01.png)

1. Click on the **Configure service backups** (A) tile.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-02.png)

1. Click on the **S3 Compliant** (A) tile in the Choose an object storage type wizard step and click the Next (B) button.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-03.png)

1. Enter the S3 endpoint and connection information provided in Table 2 - Service protection object bucket details in the Connect IBM Storage Fusion to your backup location and click **Add** (E). Additionally, the Show/Hide button on the Secret key can be used to display the text or hide it.

*Table  - Service protection object bucket details*

| Field name | Value | Callout |
| --- | --- | --- |
| Endpoint: | http://192.168.252.7:80 | (A) |
| Bucket: | testbucket | (B) |
| Access Key: | s3access | (C) |
| Secret Key: | s3secret | (D) |


![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-04.png)

1. An Adding backup location, Location service-protection-location is being added message will appear in the upper-right corner of the Fusion GUI.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-05.png)

1. Click the **Define schedule** (A) button to configure a schedule for service protection.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-06.png)

1. Select **Weekly** (A) under the Select frequency item, select **Sunday** (B) from the Schedule item, and select a Start time, End time, and **Timezone** (C) under the Time window item. Click the Create **policy** (D) button. Leave Initiate Service backup now selected.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-07.png)

1. The backup service protection backup policy information should now be displayed.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-08.png)

1. Confirm that backup service protection has been enabled for the IBM Fusion Backup & restore service.

   ![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/backup-service-protection-09.png)
