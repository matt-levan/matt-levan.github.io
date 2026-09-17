---
layout: default
title: "Workshop Overview"
permalink: /ocpv-fusion-lab/overview/
nav_order: 2
parent: "OCP Virtualization with IBM Fusion Lab"
---

## The virtualization modernization challenge

Many organizations today face a critical decision point with their virtualization infrastructure. Licensing changes, rising costs, and the need for cloud-native agility are driving teams to re-evaluate their approach to running virtual machine workloads.

Red Hat OpenShift Virtualization and IBM Fusion together offer a path forward, enabling you to run VMs alongside containers on a single platform with enterprise-grade storage.

***Your objective***: Gain hands-on experience deploying, managing, and migrating virtual machine workloads using OpenShift Virtualization with IBM Fusion storage integration.

## Success criteria

By the end of this workshop, you will have practical skills in:

- Navigating the OpenShift Virtualization console and understanding the architecture
- Creating and configuring virtual machines using templates and custom specifications
- Leveraging IBM Fusion storage classes for persistent VM storage
- Performing VM lifecycle operations such as live migration, snapshots, and cloning
- Planning and executing workload migrations from legacy virtualization platforms using the Migration Toolkit for Virtualization
- Perform backup and restore operations for your virtual machines
- IBM Fusion Access for SAN to leverage your existing SAN infrastructure

***Technical outcome***: You will have hands-on experience running VM workloads on OpenShift with enterprise storage provided by IBM Fusion.

## Target audience

This workshop is designed for:

- Infrastructure architects evaluating virtualization modernization strategies
- Site reliability engineers managing hybrid VM and container environments
- Platform engineers building and operating OpenShift-based infrastructure
- Infrastructure engineers responsible for VM workload management

## What you need to succeed

You should have:

- Basic understanding of virtualization concepts (VMs, hypervisors, datastores)
- Familiarity with Red Hat OpenShift navigation (projects, operators, console)
- Comfort using a terminal and command line tools
- No prior OpenShift Virtualization or IBM Fusion experience required

## Why OpenShift Virtualization with IBM Fusion

***Current challenges*** facing virtualization teams:

- ***Licensing uncertainty***: Changing vendor strategies create cost and continuity risks
- ***Siloed infrastructure***: VMs and containers managed on separate platforms increase operational overhead
- ***Storage complexity***: VM workloads require enterprise-grade persistent storage with data protection
- ***Migration risk***: Moving workloads between platforms involves downtime and validation effort

***How this workshop addresses them***:

- ***Unified platform***: Run VMs and containers side by side on OpenShift, managed with familiar Kubernetes tooling
- ***Enterprise storage***: IBM Fusion provides persistent, performant storage with snapshot and replication capabilities
- ***Simplified migration***: The Migration Toolkit for Virtualization automates workload migration from legacy platforms
- ***Operational consistency***: A single management plane for all workloads reduces complexity and training overhead

## Workshop modules

***Module 1: Exploring the environment*** (~20 minutes)

Tour the OpenShift console, OpenShift Virtualization operator, and IBM Fusion storage integration. Create your first VM from a template.

***Module 2: VM lifecycle management*** (~20 minutes)

Configure VMs with custom resources, work with IBM Fusion-backed storage, and perform live migration, snapshots, and cloning.

***Module 3: Workload migration*** (~25 minutes)

Use the Migration Toolkit for Virtualization to plan and execute a migration from a legacy virtualization platform.

***Module 4: Optional - IBM Fusion Backup and Restore Recipes*** (If time permits)

Leverage IBM Fusion Backup and Restore services for your applications and virtual machines.

## Common questions

***"Can we run our existing VM workloads without changes?"***

Yes. OpenShift Virtualization runs standard VM images. Module 1 demonstrates creating VMs from existing templates and images.

***"What about storage performance for VM workloads?"***

IBM Fusion provides enterprise-grade storage optimized for both VM and container workloads. Module 2 covers storage configuration and performance considerations.

***"How disruptive is the migration process?"***

The Migration Toolkit for Virtualization supports warm migration with minimal downtime. Module 3 walks through the full migration workflow.

***"Do we need to retrain our entire operations team?"***

OpenShift Virtualization uses familiar VM management concepts within the OpenShift console. The learning curve is manageable for teams with existing virtualization experience.
