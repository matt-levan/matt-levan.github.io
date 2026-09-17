---
layout: default
title: "Addendum"
permalink: /backup-restore-guide/addendum/
nav_order: 7
parent: "Fusion Backup and Restore Lab Guide"
---

# Addendum

## OpenShift project selector

{% include shared/openshift-project-selector.md %}

## S3 Route
1. In the OpenShift GUI, navigate to the Routes screen by click on the Networking (A) menu item shown in the left-hand side navigation pane and selecting the Routes (B) sub-item. Change the project to openshift-storage using the project selector. Copy the Location associated with the S3 route by using the Copy to clipboard (C) button.

![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/s3-route-01.png)


![Screenshot]({{ site.baseurl }}/assets/images/backup-restore-guide/s3-route-02.png)
