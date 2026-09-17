---
layout: default
title: "Module 4: Backup and Restore"
permalink: /ocpv-fusion-lab/module-04/
nav_order: 7
parent: "OCP Virtualization with IBM Fusion Lab"
---

You can protect your container workloads and virtual machines by using the IBM Fusion Backup & Restore service.

In the event of data loss or corruption, such as accidental deletion or malicious ransomware attacks, a backup and restore system is needed to ensure data integrity and availability. By taking periodic backups of applications and storing them safely, you can restore your workloads during disasters, thereby minimizing downtime and data loss. Whenever disaster occurs, you can restore the workloads in place or to an alternate cluster.

Backup & Restore service protects both containerized and virtual machine (VM) workloads, going beyond data protection to include the application's state and essential etcd resources. This capability is not only for stateful applications but also for stateless ones, ensuring complete restoration of functionality and configuration.

Backup and restore works by first choosing a secure backup location and then defining backup polices tailored to your application needs with frequency and retention parameters. You can then associate the workloads with defined backup policies to automate and simply the backup process. Finally, you can recover the backed up workloads either in their original location or to an alternate cluster based on the requirements.

For more complex scenarios or whenever you need to run tailored and repeatable workflows, you can make use of the advanced recipes provided by Backup & Restore service.

Backup & Restore supports both single-cluster mode and hub and spoke model. In a single cluster mode, all backup and restore operations are managed within a single cluster. In case of hub and spoke model, the hub acts as a central management point and spokes are individual clusters that run backup and restore tasks locally. You can choose this mode to manage backups across multiple clusters, and it is useful for large-scale environments where multiple clusters need to be managed with resilience in case of failures.

The IBM Fusion Backup & Restore service protection involves the backup of the Backup & Restore data management service itself to a S3 bucket.

In this module, you will explore how to protect virtual machines with the IBM Fusion Backup and Restore Service.

## Learning objectives

By the end of this module, you will be able to:

- Configure and use the backup and restore functions of IBM Fusion
  - Learn how to define and configure backup locations and policies.
  - Learn how to assign backup policies to applications.
  - Learn how to restore an application.
  - Learn how to monitor the status of backups and jobs.
  - Learn how to create a recipe and assign the recipe to applications for application-consistent backups.
  - Learn how to configure protection of the backup and restore service.

## Pre-steps

To complete the activities included in this lab, the IBM Fusion operator and IBM Fusion backup & restore service need to be installed. You will have had to complete Module 1, exercise 3 to proceed with this section.

Switch to the **IBM Fusion** tab on the right.

## Exercise 1: Create Backup Locations and Policies

Applications have different requirements for backup frequency and retention. IBM Fusion uses Backup Policies to define and automate backup operations.

To configure backup and restore activities, go to the Backup & Restore section on the left-hand side navigation pane. To access the Overview page for Backup & Restore, click on the Backup & Restore (A) menu item shown in the left-hand side navigation pane and select the Overview (B) sub-item.

![Backup and Restore Overview]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bandrl-overview.png)

### S3 Backup Bucket

Data Foundation must be installed and setup. In the **OpenShift Console** tab, navigate to **Administrator** -> **Storage** -> **Object storage** and select the tab **Object Bucket Claims**.

![Data Foundation]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-datafoundation.png)

Change to the `ibm-backup-restore` Project.

![IBM Storage Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-storage-project.png)

Click create ObjectBucketClaim

![Object Bucket Claim]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-objectbucketclaim.png)

Once the bucket claim is created, scroll down and reveal values

![Object Bucket Claim Values]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-objectbucketclaimvalues.png)

We will use the `Bucket Name`, `Access Key` and `Secret Key`.

Next we need to get the external endpoint
Navigate to `Networking` -> `Routes` and choose all projects and search for `S3`

![Object Bucket S3 Routes]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-objectbuckets3routes.png)

There you will find the correct route to use.

### Backup Location

Back on the **IBM Fusion** tab, navigate to the Locations screen by clicking on the Backup & restore (A) menu item shown in the left-hand side navigation pane and selecting the **Locations** (B) sub-item. When the Locations screen is shown, click the **Add location** `(C)` button and use the wizard to provide the appropriate S3 endpoint information and credentials.

![Back and Restore Locations]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-locationss.png)

Enter `location1` (or any name of your choosing) in the Location name text entry field and click the **MCG/NooBass** (B) tile. Then, click **Next** to enter the connection details. 

Enter the S3 endpoint and connection information collected in the previous steps.

![Back and Restore Location Details]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-locations-details.png)

The newly added backup location should appear in a new tile and be connected after a few seconds.

![Back and Restore Location Details Added]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-locations-added.png)

### Backup Policies

A backup policy is a set of rules and schedules that define how and when data is backed up. It outlines the frequency of backups, the type of data to be backed up, the retention period, and the storage location. The Backup & Restore service allows you to create and manage backup policies to ensure your data is protected according to your specific needs.

The Policies page lists all policies. You can search for policy records based on the backup location or other keywords, configure the table display, and perform actions like viewing, editing, or deleting policies from the ellipsis overflow menu.

In the Fusion GUI, navigate to the Policies screen by clicking on the **Backup & restore** (A) menu item shown in the left-hand side navigation pane and selecting the **Policies** (B) sub-item. When the Policies screen is shown, click the **Add policy** `(C)` button to configure a backup policy. 

![Back and Restore Policies]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policies.png)

Enter `daily-snapshot` (A) in the **Policy Name** text entry field, set **Frequency** to **Daily** and specify a Time window for the backup to occur. Then, select the **In place snapshot** (B) Backup location tile. Finally, click the **Next** `(C)` button to create the new daily-snapshot backup policy.

![Back and Restore Policy Create]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-create.png)

The daily-snapshot policy will now appear in the list of backup policies. Next, we will create a weekly-backup policy using object storage as the backup location. Click the **Add policy +** (A) button to begin.

![Back and Restore Policy New]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-new.png)

(A) Enter `weekly-backup` in the **Policy name** text entry field, set **Frequency** to **weekly** (B), select **Sunday** `(C)` for **Schedule**, and specify a Time window for the backup to occur. Select the **Object Storage** (D) Backup location tile to pick the backup location `location1` (E). Click the **Create policy** (F) button to complete creation of the weekly-backup backup policy.

![Back and Restore Policy Weekly]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-weekly.png)

The Policies summary screen shows where backups are stored, the schedule for each policy, and the application that uses the policy.

![Back and Restore Policy Summary]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-summary.png)

### Verify

Confirm the following in the IBM Fusion Backup & Restore console:

- The backup location shows as ***Connected***
- Both the `daily-snapshot` and `weekly-backup` policies are listed in the Policies summary

## Exercise 2: Backup and Restore an Application

In this section, you'll learn how to create a basic application to demonstrate core functionality and prepare for backup and restore operations.

### Create a simple application

In the OpenShift GUI, navigate to the **Projects** screen by clicking on the **Home** (A) menu item in the left-hand side navigation pane and selecting the **Projects** (B) sub-item. When the Projects screen is shown, click the **Create Project** `(C)` button.

![Create New Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-create-project.png)

(A) Enter the value `filebrowser` in the Name text entry field and click the **Create** (B) button.

![Create New Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-create-project-new.png)

Verify that the project listed is set to the newly created filebrowser namespace. Click the **Import YAML** (A) (the icon that looks like a + sign) button on the OpenShift GUI masthead.

![Varify New Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-verify-project.png)

Use the following yaml file to create the filebrowser application:

```bash
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  labels:
    app: filebrowser
    app.kubernetes.io/component: filebrowser
    app.kubernetes.io/instance: filebrowser
    app.kubernetes.io/name: filebrowser
    app.kubernetes.io/part-of: filebrowser-app
  name: files
spec:
  storageClassName: ocs-storagecluster-ceph-rbd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  labels:
    app: filebrowser
    app.kubernetes.io/component: filebrowser
    app.kubernetes.io/instance: filebrowser
    app.kubernetes.io/name: filebrowser
    app.kubernetes.io/part-of: filebrowser-app
  name: filebrowser-config
spec:
  storageClassName: ocs-storagecluster-ceph-rbd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---

kind: ConfigMap
apiVersion: v1
metadata:
  name: my-filebrowser-config
  labels:
    app: filebrowser
    app.kubernetes.io/component: filebrowser
    app.kubernetes.io/instance: filebrowser
    app.kubernetes.io/name: filebrowser
    app.kubernetes.io/part-of: filebrowser-app
data:
  .filebrowser.json: |
    {
      "port": 8080,
      "baseURL": "",
      "address": "",
      "log": "stdout",
      "database": "/config/database.db",
      "root": "/files"
    }

---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: filebrowser
  labels:
        app: filebrowser
        deployment: filebrowser
spec:
  replicas: 1
  selector:
    matchLabels:
        app: filebrowser
  template:
    metadata:
      labels:
        app: filebrowser
        app.kubernetes.io/component: filebrowser
        app.kubernetes.io/instance: filebrowser
        app.kubernetes.io/name: filebrowser
        app.kubernetes.io/part-of: filebrowser-app
    spec:
      restartPolicy: Always
      serviceAccountName: default
      schedulerName: default-scheduler
      enableServiceLinks: true
      terminationGracePeriodSeconds: 30
      securityContext: {}
      containers:
        - resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 2
            timeoutSeconds: 2
            periodSeconds: 5
            successThreshold: 1
            failureThreshold: 3
          terminationMessagePath: /dev/termination-log
          name: filebrowser
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            timeoutSeconds: 2
            periodSeconds: 10
            successThreshold: 1
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            failureThreshold: 30
            periodSeconds: 10
          env:
            - name: TZ
              value: UTC
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          imagePullPolicy: IfNotPresent
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: config
              mountPath: /config
            - name: filebrowser-config
              mountPath: /.filebrowser.json
              subPath: .filebrowser.json
            - name: data
              mountPath: /files
          image: 'filebrowser/filebrowser:v2.18.0'
      automountServiceAccountToken: true
      serviceAccount: default
      volumes:
        - name: config
          persistentVolumeClaim:
            claimName: filebrowser-config
        - name: filebrowser-config
          configMap:
            name: my-filebrowser-config
            defaultMode: 420
        - name: data
          persistentVolumeClaim:
            claimName: files
      dnsPolicy: ClusterFirst
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  revisionHistoryLimit: 3
  progressDeadlineSeconds: 600

---

kind: Service
apiVersion: v1
metadata:
  name: filebrowser
  labels:
    app: filebrowser
    app.kubernetes.io/component: filebrowser
    app.kubernetes.io/instance: filebrowser
    app.kubernetes.io/name: filebrowser
    app.kubernetes.io/part-of: filebrowser-app
spec:
  ports:
    - name: 8080-tcp
      protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
  selector:
    app: filebrowser

---
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: filebrowser
  labels:
    app: filebrowser
    app.kubernetes.io/component: filebrowser
    app.kubernetes.io/instance: filebrowser
    app.kubernetes.io/name: filebrowser
    app.kubernetes.io/part-of: filebrowser-app
  annotations:
    openshift.io/host.generated: 'true'
spec:
  to:
    kind: Service
    name: filebrowser
    weight: 100
  port:
    targetPort: 8080-tcp
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

The OpenShift GUI and use `Ctrl-V` (windows), `CMD-V` (Mac) or browser Edit -> Paste button to paste the contents of the clipboard into the editor (A) text entry field. Click the *Create* (B) button to create the filebrowser resources.

![Paste YAML]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-paste-yaml.png)

The following information will be displayed listing all resources that were created and Creation status.

![YAML status]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-yaml-status.png)

Navigate to the Route screen by clicking on the *Network* (A) menu item shown in the left-hand side navigation pane and selecting the *Routes* (B) sub-item. When the Routes screen is shown, click the *URL Location* +(C)+ for the filebrowser route to open a new tab/window to the filebrowser application

NOTE: It may take a minute or two for the filebrowser application to become fully online and accessible from the route screen

![Routes]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-routes.png)

Login to the filebrowser application with *Username* (A): `admin` and *Password* (B): `admin`. Click the *Login* +(C)+ button.

![filebrowser login]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-filebrower-login.png)

No files will be listed in the filebrowser application.

![filebrowser files]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-filebrower-files.png)

Use *New folder* (A) and *Upload file* (B) to create some directories and upload a couple files. In the example shown, 2 directories were created, and 3 files were uploaded.

![Filebrowser Files New]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-filebrower-files-new.png)

### Assign Policy to application

The OpenShift Cluster can host many application workloads; IBM Fusion provides a simple graphical user interface (GUI) to assign backup policies to applications and automate their protection.

TIP: There are two (2) methods for interacting with applications in the Fusion GUI. The Applications menu item on the left-hand side navigation pane shows only the applications local to the cluster. The Backed up applications sub-item under the Backup & restore menu allows for assigning policies to local and remote clusters. For this lab either option can be used. 

#### Assign policy using applications menu item

This sub-section describes the process for managing backups of applications deployed in the local cluster using the Applications page.

Switch to the *IBM Fusion* tab.

Navigate to the Application pane by clicking on the *Applications* (A) menu item on the left-hand side navigation pane.

![Applications Page]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-applications-page.png)

Select the *filebrowser* application checkbox (A) and click the *Assign backup policy* (B) button.

![Applications Assign Policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-assign-policy.png)

Select both the *daily-snapshot* checkbox (A) and *weekly-backup* checkbox (B). Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the *Save* +(C)+ button.

![Applications Assign Policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-assign-policy2.png)

A confirmation window will appear in the upper-right corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications.

#### Assign policy using Backed up applications menu item

This sub-section describes the process for managing backups of applications deployed across both hub and spoke clusters using the Backup up applications page.

Navigate to the Backed up applications pane in the IBM Fusion UI by clicking *Backup & Restore* (A) menu item shown in the left-hand side navigation pane and selecting the *Backed up applications* (B) sub-item. You should now see a page listing the applications that have been backed up, together with application details and assigned backup policies. Each line represents an OpenShift namespace which can contain a different application/workload.

If you want to find a specific namespace, you can use the search toolbar present on the page.

You can assign a backup policy to a namespace by clicking *Protect apps +* +(C)+ on the right side. This will launch the Protect applications wizard.

![Applications Assign Policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-assign-policy2.png)

The Protect applications wizard can be used to backup applications locally and in hub and spoke configurations. Select the *local cluster* (A) from the drop-down list, and a list of unprotected applications will populate in the list below. Next select, *filebrowser* (B) from the unprotected applications list. Finally click on the *Next* +(C)+ button.

![Protect Wizard]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-protect-wizard.png)

On the Assign policies, you can select one or more policies to attach to the application and if backup should start right after applying the policies. Select both the *daily-snapshot* (A) and *weekly-backup* (B) policies. Leave the Back up now toggle set to enabled (displayed with a green checkmark). Click the *Assign* +(C)+ button.

![Protect Wizard]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-protect-wizard2.png)

A confirmation window will appear in the right-hand upper corner notifying that the policies have been assigned and the filebrowser application will appear in the list of Backed up applications. 

![Protect Wizard Confirm]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-protect-wizard-confirm.png)

#### Monitor backup status

Depending on the method used to Assign a backup policy, the Pending and In progress screens will be slightly different. Selecting the application name will display a page with the same information.

After a short period of time the Backup status will change from Pending to an In progress status, until it is Completed. 

![Backup Status]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-status.png)

Status of each policy can be checked by going into the application pane and clicking the *Backups* (A) tab. In the example shown below, the daily-snapshot policy has `Completed` and the weekly-backup is `Snapshot in progress`.

![Backup Complete]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-complete.png)

#### Application restore

This section describes the steps required to restore an application from a previously created backup.

From the Applications or Backed up applications page, click the application name to open its Overview page

![Backedup Applications]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backuped-applications.png)

The *Backups* tab shows all the backups created for this application and lets you choose the backup you want to restore from. 

![Backedup Applications]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backups.png)

A restore action can also be started by using buttons at top of the page. Click on the *Restore* (A) button located at the top of the pane.

![Restoring Applications]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore.png)

The wizard presents the choice to restore to the same cluster or to a different cluster, if you have a hub-spoke setup. Open the drop-down list associated with the “Target cluster” field and select the *This cluster* (A) item from the list.

![Restoring Application Wizard]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-wizard.png)

The restore wizard also provides a choice to restore over the same project, an existing project, or to a new project. Select *Create a new project* (A) and (B) enter `filebrowser2` in the Project name text entry field. Then, click on the *Next* +(C)+ button to select the backup to restore. 

![Restoring Application Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-project.png)

Choose the *Backup time* (A) you want to restore from, from the list of backups provided - note that if you want multiple backups to choose from, you must first create them. Then click on the *Next* (B) button.

![Restoring Application Time]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-time.png)

Keep all the default settings shown and click on the *Restore* (A) button. A *Summary* (B) is displayed on the right pane with details on what the Before restore and After restore states will be.

![Restoring Application Settings]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-settings.png)

Confirm the restore by clicking on the *Restore* (A) button in the final dialog box.

![Restoring Application Confirm]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-confirm.png)

Watch the restore progress on the *Backups* tab. Item (A) is the Restore job that has been scheduled; Item (B) will update as the restore operation progresses. The Restore process can also be tracked on the Jobs page. The Jobs page can be accessed by clicking on the Backup & restore menu item shown in the left-hand side navigation pane and selecting the Jobs sub-item. On the Jobs page, click the Restore tab to track progress.

![Restoring Application Progress]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-progress.png)

In the OpenShift Console, navigate to the Pods page by clicking on the *Workloads* (A) menu item shown in the left-hand side navigation pane and selecting the *Pods* (B) sub-item. Then click the *project selector* +(C)+ and choose `filebrowser2` (D) from the projects drop down menu. Refer to section OpenShift project selector on how to use the project selector.

![Restoring Application Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-project2.png)

Watch the application being restored and the new pods created for the restored application. 

![Restoring Application Watch]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-watch.png)

Navigate to the PersistenVolumesClaims screen by selecting the *Storage* (A) menu item shown in the left-hand side navigation pane and selecting the *PersistentVolumeClaims* (B) sub-item. The newly restored PVCs are shown.

![Restoring Application PVC]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-pvc.png)

Navigate to the Routes screen by clicking on the *Networking* (A) menu item shown in the left-hand side navigation pane and selecting the *Routes* (B) sub-item. The Routes screen is shown

![Restoring Application Routes]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-restore-routes.png)

Login to the filebrowser application with the *Username* (A): `admin` and *Password* (B): `admin`. Click *Login* +(C)+. Review that the files added earlier have been restored to a new application project

![Restoring Application]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-application.png)

### Verify

- The restored filebrowser application in the `filebrowser2` project is accessible via its route
- The files and directories you uploaded earlier are present in the restored application

[[exercise-3]]
== Exercise 3: Backup and Restore Virtual Machines

### Backup a Virtual Machine

In the *Administrative* view, create a new project called `vmbackup`

Navigate to *Virtualization* -> *Catalog*. Create a new Virtual Machine using the *Red Hat Enterprise Linux 9* VM template. Use the name `rhel9-backup`.

Switch to the *IBM Fusion* tab.

Navigate to the Applications screen by clicking on the Applications (A) menu item on the left-hand side navigation pane. Select the check box (B) next to `vmbackup` application and click on the *Assign backup policy* +(C)+ button to open the Assign backup policy page.

![VM Backup Policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backup-policy.png)

Select the check box (A) next to `weekly-backup` and leave the *Back up now* toggle set to `enabled` (green with a checkmark for enabled). Click on the *Save* (B) button to enable the weekly-backup policy for the vmbackup application and start a new backup job. 

![VM Set backup policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backup-set-policy.png)

Wait for backup to show as *Completed* under *Backup status*. 

![VM Backup Complete]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backup-complete.png)

Navigate to the *Jobs* screen by clicking on the *Backup & restore* (A) menu item on the left-hand side navigation pane and selecting the *Jobs* (B) menu sub-item. Click on the `vmbackup-weekly-backup-<OCP cluster name>` +(C)+ button to open the backup summary page.

![VM Backup Jobs]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backup-jobs.png)

Review the information on this page. Some relevant information to the backup has been highlighted for informational purposes.

![VM Backup Summary]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backup-summary.png)

### Restore Virtual Machine

Navigate to the Backed up applications screen by clicking on the *Backup & restore* (A) menu item on the left-hand side navigation pane and selecting the *Backed up applications* (B) menu sub-item. Click on the `vmbackup` +(C)+ application name to open the vmbackup backup details page.

![VM Backed up Applications]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-backed-apps.png)

Click on the *Restore* (A) button to begin the restore process.

![VM Restore]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore.png)

The wizard presents the choice to restore to the same cluster or to a different cluster, if you have a hub-spoke setup. Open the drop-down list associated with the *Target cluster* field and select *This cluster* (A) from the list.

![VM Restore select destination]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore-select-dest.png)

Click on the *Create a new project* (A) combo box to change the Project destination. Enter `vmrestore` in the *Project name* (B) text entry field and click the *Next* +(C)+ button to continue the restore process.

![VM Restore Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore-project.png)

Click on the *latest backup time* (A) combo box (which should be the backup that was run in the previous section). Click the *Next* (B) button to continue to the final step of the restore process.

![VM Restore Select]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore-select.png)

Review the *Summary* (A) details for OpenShift Project and Restore point for accuracy. Click the *Restore* (B) button.

![VM Restore Button]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore-button.png)

Click the *Restore* (A) button again to confirm the start of the restore process.

![VM Comfirm Restore]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-confirm-restore.png)

Click on the *View job details* (A) button to open the `vmbackup` restore details page.

![VM Job Details]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-job-details.png)

Wait for the restore backup job to show *Completed*. 

![VM Restore Complete]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-restore-complete.png)

Return to the *OpenShift Console* tab. Navigate to the *VirtualMachines* screen by clicking on the *Virtualization* (A) menu item on the left-hand side navigation pane and selecting the *VirtualMachines* (B) sub-item. Use the *Project selector* to change to the `vmrestore` +(C)+ project. Notice that the VirtualMachine has been restored to a new namespace and is in a Running Status.

![List Restored VM]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-vm-list-restored.png)

### Verify

- The virtual machine `rhel9-backup` is in **Running** status in the `vmrestore` project
- The VM was restored to a new namespace successfully

[[exercise-4]]
== Exercise 4: Backup and Restore an Application with a recipe

### Create an application with Fusion recipe

When you protect an application with Backup & Restore service, a default backup and restore workflow is used to protect an application. But while the backup and restore workflow is sufficient for some applications, there are some instances where you need to create a custom workflow for the backup and restore process to produce an application consistent backup. Recipes are used to create a custom workflow for the backup and restore process.

****
Types of consistency:

No consistency: Snapshots are not consistent. If an application uses 4 persistent volumes (PV), it rolls through these temporally. At point in time A, a snapshot is taken of one of the PVs. Then a snapshot is taken of the second, and then the third, and so on. Even with scripts, the PVs will not be backed up at the same time. Therefore, they will not be consistent with one another.

Consistency breaks if the application is doing active input/output (IO) to the persistent volumes. If the application is writing to the volumes in the middle of a snapshot and another snapshot of another volume was taken when the write was finished, it ends up being inconsistent.
Crash consistent: IBM Fusion supports crash consistency. This ensures that all the snapshots of the PVs are taken at the exact same time so that they are consistent, even after a disaster. Crash consistency means that if, for example, a rack was to be unplugged and all the servers were to lose power at the same time, then all those PVs are consistent with one another because the writes to them stopped at the exact same time. 

Application consistent: If a client has an application that has many, many persistent volumes, and that application is busy reading and writing to its PVs, there needs to be a way to instruct the application to stop writing or to pause. The application can complete any tasks in process but then stop briefly to allow a snapshot of the PVs to be taken. Then, the application can be instructed to resume. This is like quiescing a database.

With application consistency, it’s possible to restore an application to another cluster without having data stuck in an I/O buffer, thus ensuring the application is back running in the exact state it was in at the time of the backup. Application consistency also means that there needs to be a workflow to back up those applications in a certain order, and Fusion provides this with recipes.

Application consistent backups are important because they ensure that important files and data are saved in a way that keeps them safe and undamaged. This means that if something goes wrong, like a computer crash or a power outage, clients can restore their files and data to the way they were before the event, without losing any important information.
****

In the *OpenShift Console* tab, navigate to the *Projects* screen by clicking on the *Home* (A) menu item in the left-hand side navigation pane and selecting the *Projects* (B) sub-item. When the Projects screen is shown, click on the *Create Project* +(C)+ button.

![Create PacMan Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-create-pm-project.png)

In the popup dialog enter `pacman` as the name.

![Create PacMan Project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-create-pm-project-yaml.png)

Use the following YAML file to create the PacMan Application in the `pacman` namespace.

```bash
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: mongo-storage
spec:
  storageClassName: ocs-storagecluster-ceph-rbd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 8Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    name: mongodb
    app: mongodb
  name: mongodb
spec:
  replicas: 1
  selector:
    matchLabels:
      name: mongodb
  template:
    metadata:
      labels:
        name: mongodb
        app: mongodb
    spec:
      containers:
      - image: bitnami/mongodb:5.0.24-debian-11-r20
        name: mongodb
        ports:
        - name: mongodb
          containerPort: 27017
        volumeMounts:
          - name: mongo-db
            mountPath: /bitnami/mongodb/data/db
      volumes:
        - name: mongo-db
          persistentVolumeClaim:
            claimName: mongo-storage

---
apiVersion: v1
kind: Service
metadata:
  labels:
    name: mongodb
  name: mongo
spec:
  type: ClusterIP
  ports:
    - port: 27017
      targetPort: 27017
  selector:
    name: mongodb

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    name: pacman
  name: pacman
spec:
  replicas: 1
  selector:
    matchLabels:
      name: pacman
  template:
    metadata:
      labels:
        name: pacman
    spec:
      containers:
      - image: quay.io/jpacker/nodejs-pacman-app:latest
        name: pacman
        ports:
        - containerPort: 8080
          name: http-server
      initContainers:
      - name: db-check
        image: busybox:latest
        command: ['sh', '-c', 'echo -e "Checking for the availability of MongoDB Server deployment"; while ! nc -z mongo 27017; do sleep 1; printf "-"; done; echo -e "  >> MongoDB Server has started";']

---
apiVersion: v1
kind: Service
metadata:
  name: pacman
  labels:
    name: pacman
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
  selector:
    name: pacman

---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: pacman
  labels:
    app.kubernetes.io/name: pacman
spec:
  path: "/"
  to:
    kind: Service
    name: pacman
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

Click the *Import YAML* (A) (the icon that looks like a + sign) button on the OpenShift Console masthead.

![Import YAML]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-import-yaml.png)

In the *OpenShift Console* tab use `Ctrl-V` (windows), `CMD-V` (Mac) or the browser `Edit` -> `Paste` function to paste the contents of the clipboard into the editor (A) text entry field. Click the *Create* (B) button to create the recipe.

![Create recipe]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-create-recipe.png)

In the *IBM Fusion* tab, navigate to the Applications screen by clicking on the *Applications* (A) menu item shown in the left-hand side navigation pane. When the Applications screen is shown, select the *pacman* checkbox (B) and click on the *Assign backup policy* +(C)+ button.

![Assign policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-assign-policy3.png)

Select the *weekly-backup policy* (A) and use the *Backup up now* (B) toggle to *disable* the initial backup (shown as gray when disabled). Click the *Save* +(C)+ button.

IMPORTANT: Set the Backup up now option to *disabled* (indicated by the absence of a green checkmark) to prevent an initial backup. The Pacman application does not generate sufficient changes in the MongoDB database and performing an initial backup without the appropriate recipe may result in restore failures when using Change Block Tracking (CBT).

![Set policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-set-policy.png)

The Pacman application is now associated with the weekly-backup policy.

![Policy Associated]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-associated.png)

In the *OpenShift Console* tab, navigate to the Search screen by clicking on the *Home* (A) menu item shown in the left-hand side navigation pane and selecting the *Search* (B) sub-item.

![Search]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-search.png)

Change to the `ibm-spectrum-fusion-ns` project, if not already there. Refer to section OpenShift project selector on how to use the project selector. Open the drop-down list associated with the *Resources* (A) field and (B) enter `policyassignment` in the search box text entry field (displayed with a magnifying glass). Select the *PolicyAssignment* +(C)+. Click anywhere outside the drop-down list to dismiss the window.

![Project Selector]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-project-selector.png)

Click on the *PolicyAssignment* associated with the pacman application that was just created. The syntax for the policy is, `<application>-<backup policy>-<backup cluster name>`. In the example shown here, the PolicyAssignment name is pacman-weekly-backup-apps.66d86bd0694f19a4a8b069f1.ocp.techzone.ibm.com.

![Policy Assignment]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-assignment.png)

Click the *YAML* (A) tab.

![Policy Assignment YAML]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-assignment-yaml.png)

The recipe created in Step 13 will now be added to the Pacman weekly-backup PolicyAssignment.

The recipe syntax is as follows for use in a PolicyAssignment.
```bash
spec:
  recipe:
    apiVersion: spp-data-protection.isf.ibm.com/v1alpha1
    name: RECIPE_NAME
    namespace: RECIPE_NAMESPACE
```
`RECIPE_NAME` is the name of the recipe as specified in the Recipe CR.
`RECIPE_NAMESPACE` is the namespace where the Recipe CR is located.

Enter the following 4 lines before status and after runNow as shown in the screenshot. The spacing included in the text entered is needed to conform to the YAML used by OpenShift.

NOTE: for readability the metadata and status information have been collapsed using the expand/collapse buttons on the left-hand side of the editor.

```bash
  recipe:
    apiVersion: spp-data-protection.isf.ibm.com/v1alpha1
    name: mongodb-image-based-backup-restore-recipe
    namespace: ibm-spectrum-fusion-ns
```
Click the *Save* (A) button after the 4 new lines have been added.

![Policy Save YAML]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-policy-save-yaml.png)

Change to the *pacman* project using the Project selector if necessary. Refer to section OpenShift project selector on how to use the project selector. Navigate to the Pods screen by clicking on the *Workload* (A) menu item shown in the left-hand side navigation pane and selecting the *Pods* (B) sub-item. Click on the `mongodb-XXXXXXXXXX-YYYYY` pod +(C)+ to open the pod details page.

![Pacman project]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-pacman-project-yaml.png)

Click the *Logs* (A) tab and select *Wrap lines* (B) to improve readability. Scroll to the bottom of the logs if necessary. Leave this window open for now as we will return to it after a new backup has been run using the updated PolicyAssignment with the newly attached recipe.

![Pacman logs]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-pacman-logs-yaml.png)

In the *IBM Fusion* tab, navigate to the Applications page by clicking on the *Applications* (A) menu item shown in the left-hand side navigation pane. When the Application screen is shown, select the `pacman` application (B) checkbox and click on the *Back up now* +(C)+ button. 

![backup now]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-now-yaml.png)

Click on the *Back up* (A) button.

![backup now button]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-now-button.png)

Navigate to the Jobs screen by clicking on the *Backup & restore* (A) menu item shown in the left-hand side navigation pane and selecting the *Jobs* (B) sub-item. When the Jobs screen is shown, click on the `pacman-weekly-backup-<cluster name>` job +(C)+ to open the job details page.

![backup jobs]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-jobs.png)

Verify that the Backup sequence includes hooks provided in the backup recipe by expanding the Backup sequence section of the Jobs details.

![backup sequence]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-backup-seq.png)

Additional details can be displayed by selecting the *Log view* on the Backup Jobs page.

![backup log view]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-log-view.png)

In the *OpenShift Console* tab, navigate back to the mongodb Pod logs and look for the fsyncLock command to be executed. You may need to scroll back to find the COMMAND being run.

![Mongo logs view]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-mongo-logs1.png)

Continue investigating the mongodb logs and find the fsyncUnlock log entry.

![Mongo logs view]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-mongo-logs2.png)

### Verify

- The backup job for the `pacman` application completed successfully with the recipe hooks
- The MongoDB logs show `fsyncLock` and `fsyncUnlock` commands, confirming application-consistent backup

[[exercise-5]]
== Exercise 5: Backup Service Protection

The IBM Storage Fusion Backup & Restore service protection involves the backup of the control plane to a S3 object bucket. In the event of cluster failure, you can use this feature to restore the Backup & Restore service to another cluster. In this section you will configure service protection and run the initial service backup.

****
Service protection is just for backup/restore on the hub cluster and not for other configurations that exist in IBM Storage Fusion. For example, Red Hat OpenShift Container Platform cluster, disaster recovery, Red Hat OpenShift Data Foundation.
****

NOTE: To follow this section, create a new object bucket claim, as was done in the backup location section and use the new bucket claim info service protection.

In the *IBM Fusion* tab, navigate to the Service protection page by clicking on the *Backup & restore* (A) menu item shown in the left-hand side navigation pane and selecting *Service protection* (B) sub-item.

![Service Protection]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-protection.png)

Click on the *Configure service backups* (A) tile.

![Service Protection Backups]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-protection-backups.png)

Click on the *S3 Compliant* tile in the Choose an object storage type wizard step and click the *Next* button.

![Add Location]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-add-location.png)

Enter the S3 endpoint and connection information, from the object bucket claim you created.  

![Add Location]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-add-location2.png)

An `Adding backup location, Location service-protection-location is being added` message will appear in the upper-right corner of the IBM Fusion tab.

![Service Protection Location]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-protection-location.png)

Click the *Define schedule* (A) button to configure a schedule for service protection.

![Service Protection Schedule]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-schedule.png)

Select *Weekly* (A) under the *Select frequency* item, select *Sunday* (B) from the *Schedule* item, and select a *Start time*, *End time*, and *Timezone* +(C)+ under the *Time window* item. Click the *Create policy* (D) button. Leave *Initiate Service backup now* selected.

![Service Protection Set Schedule]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-set-schedule.png)

The backup service protection backup policy information should now be displayed.

![Service Protection Backup Policy]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-backup-policy.png)

Confirm that backup service protection has been enabled for the IBM Fusion Backup & restore service.

![Service Protection Enable]({{ site.baseurl }}/assets/images/ocpv-fusion-lab/06-module-04-bnr-service-enable.png)

### Verify

- The Backup & Restore service protection is enabled
- A service backup schedule is configured with the weekly policy

== Module summary
You have successfully explored the IBM Fusion Backup and Restore Service.

**What you accomplished:**

- Defined backup and restore locations and policies.
- Assigned backup polices to applications.
- Restored an application to a new project.
- Defined a backup service protection policy.
- backup up and restored a virtual machine.

**Key takeaways:**

- Fusion Backup and Restore is a key component of IBM Fusion and enhances Red Hat OpenShift.
- IBM Fusion Backup and Restore has an easy to administer user interface. 
- Backup policies allow the customization of scheduled backup and create application consistent backups.
