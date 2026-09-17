---
layout: default
title: "Addendum"
permalink: /backup-restore-guide/addendum/
nav_order: 7
parent: "Fusion Backup and Restore Lab Guide"
---

# Addendum

## OpenShift project selector
The Project selector is used to switch between the different OpenShift projects available. To switch to a specific project, click on the Project Selector drop-down list (A) and then click on the appropriate project name shown in the Projects list (B). You can limit the list of projects shown in the Projects list OR search for a specific project by entering search criteria in the Search entry field (C) (i.e., the entry field with the magnifying glass icon on the left). You can also create a new project by clicking on the Create Project button (D) shown at the bottom of the screen.
> NOTE: Show default projects toggle switch (E) will show/hide projects that start with the name openshift-.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/openshift-project-selector-01.png)

## S3 Route
1. In the OpenShift GUI, navigate to the Routes screen by click on the Networking (A) menu item shown in the left-hand side navigation pane and selecting the Routes (B) sub-item. Change the project to openshift-storage using the project selector. Copy the Location associated with the S3 route by using the Copy to clipboard (C) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/s3-route-01.png)


![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/s3-route-02.png)
