---
layout: default
title: "Fusion Backup and Restore Lab Guide"
permalink: /backup-restore-guide/
nav_order: 1
---

# Introduction

Most organizations will soon be operating in a hybrid multi-cloud environment. Container technology will help drive this rapid evolution from applications and data anchored on-premises in siloed systems, to applications and data that are portable and are independent of infrastructure.
This type of architecture uses containerized workloads; new solutions are being developed to address storage challenges such as provisioning, backup, and security.
IBM Fusion is a fully containerized solution providing backup and restore services to containerized applications running in a Red Hat OpenShift environment. It provides multiple tools to simplify data protection.
## About this lab
The purpose of this exercise is to enable you to get some hands-on experience with IBM Fusion on an OpenShift Cluster. The environment used is a VMware server provisioned on IBM Technology Zone and is suitable for self-education, demos, and a customer Proof of Experience (PoX).
This lab is divided into two main sections, as follows:
1. Configure and use the backup and restore functions of IBM Fusion
  1. Learn how to define and configure backup locations and policies.
  1. Learn how to assign backup policies to applications.
  1. Learn how to restore an application.
  1. Learn how to monitor the status of backups and jobs.
  1. Learn how to create a recipe and assign the recipe to applications for application-consistent backups.
  1. Learn how to configure protection of the backup and restore service.
1. Configure a second cluster as a backup and restore spoke of an IBM Fusion backup and restore hub cluster
  1. Define an object store that is accessible from both the hub and the spoke cluster.
  1. Restore an application backed up on one cluster to a different cluster.
## Product disclaimer

{% include shared/product-disclaimer.md %}

## Getting help

{% include shared/getting-help.md %}
