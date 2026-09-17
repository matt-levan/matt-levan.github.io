---
layout: default
title: "IBM Fusion RDR Lab Guide"
permalink: /rdr-lab-guide/
nav_order: 1
---

# Introduction

Regional disaster recovery (Regional-DR) is composed of Red Hat Advanced Cluster Management for Kubernetes (RHACM) and IBM Fusion Data Foundation components to provide application and data mobility across OpenShift Container Platform clusters. It is built on Asynchronous data replication and hence could have a potential data loss but provides the protection against a broad set of failures.
Fusion Data Foundation is backed by Ceph as the storage provider, whose lifecycle is managed by rook, and it is enhanced with the ability to:
- Enable pools for mirroring.
- Automatically mirror images across RBD pools.
- Provides csi-addons to manage per Persistent Volume Claim mirroring.
Regional-DR supports a multi-cluster configuration that is deployed across different regions and data centers. For example, a 2-way replication across two clusters located in two different regions or data centers. This solution is entitled with Red Hat Advanced Cluster Management (RHACM) and Fusion Data Foundation Advanced SKUs and related bundles.
## About this lab
The Fusion Regional Disaster Recovery Hands-On Lab is a comprehensive, real-world learning environment designed to help you explore and master disaster recovery strategies using Red Hat and IBM technologies.
### Lab Overview
This lab features two fully deployed OpenShift clusters integrated with Fusion Data Foundation (FDF) and managed through Red Hat Advanced Cluster Management (ACM). It is purpose-built to simulate a multi-region architecture and demonstrate how to implement and validate Fusion Regional Disaster Recovery (RDR) capabilities.

### What You'll Learn
Participants will gain hands-on experience with:
- Deploying and configuring Fusion RDR across geographically distributed OpenShift clusters.
- Managing and monitoring clusters using Red Hat ACM.
- Setting up replication policies and failover/relocate procedures using FDF.
- Testing application resilience and data integrity in the event of a regional outage.
- Understanding the architecture and best practices for high availability and business continuity in cloud-native environments.

### Lab Components
- **local-cluster (Primary Region):** Hosts the primary workloads, data services and Red Hat ACM.
- **ocp2 (Secondary Region):** Configured as the disaster recovery site.
- **Fusion Data Foundation:** Provides the underlying storage and replication layer.
- **Red Hat Advanced Cluster Management:** Centralized control plane for managing both clusters and orchestrating DR workflows.
> IMPORTANT: This configuration is not supported for Regional Disaster Recovery and is intended solely for learning purposes. In a production environment, Red Hat Advanced Cluster Management should be deployed on a separate, third cluster that does not participate in data replication.
## Components of Fusion Regional Disaster recovery
### Red Hat Advanced Cluster Management for Kubernetes
Red Hat Advanced Cluster Management (RHACM) provides the ability to manage multiple clusters and application lifecycles. Hence, it serves as a control plane in a multi-cluster environment.
RHACM is split into two parts:
- RHACM Hub
  - Components that run on the multi-cluster control plane.
- Managed clusters
  - Components that run on the clusters that are managed.
For more information about RHACM, see the [Red Hat Advanced Cluster Management for Kubernetes](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.13) product documentation.
### Fusion Data Foundation
Fusion Data Foundation provides the ability to provision and manage storage for stateful applications in an OpenShift Container Platform cluster. It is backed by Ceph as the storage provider, whose lifecycle is managed by Rook in the Fusion Data Foundation component stack and Ceph-CSI provides the provisioning and management of Persistent Volumes for stateful applications.
Fusion Data Foundation is now enhanced with the following abilities for disaster recovery:
- Enable RBD block pools for mirroring across Fusion Data Foundation instances (clusters)
- Ability to mirror specific images within an RBD block pool
- Provides csi-addons to manage per Persistent Volume Claim (PVC) mirroring
### OpenShift DR
OpenShift DR is a disaster recovery orchestrator for stateful applications across a set of peer OpenShift clusters, which are deployed and managed by using RHACM and provides cloud-native interfaces to orchestrate the life cycle of an application’s state on Persistent Volumes. These include:
- Protecting an application and its state relationship across OpenShift clusters.
- Failing over an application and its state to a peer cluster.
- Relocate an application and its state to the previously deployed cluster.
OpenShift DR is split into three components:
- **IBM Fusion Data Foundation Multicluster Orchestrator** — Installed on the Hub cluster with RHACM, it orchestrates configuration and peering of Fusion Data Foundation clusters for Metro and Regional DR relationships.
- **IBM Fusion Data Foundation DR Hub Operator** — Automatically installed as part of IBM Fusion Data Foundation Multicluster Orchestrator installation on the hub cluster to orchestrate failover or relocation of DR enabled applications.
- **IBM Fusion Data Foundation DR Cluster Operator** — Automatically installed on each managed cluster that is part of a Metro and Regional DR relationship to manage the lifecycle of all PVCs of an application.
## Advanced Cluster Manager Managed vs Discovered applications
Managed applications are applications that are part of the ACM application model. They are deployed and managed using a multi-cluster application definition that specifies which clusters they should be deployed to, and how they should be configured. ACM uses GitOps principles to manage the deployment and lifecycle of these applications, ensuring they are deployed consistently across multiple clusters. OpenShift API for Data Protection is not required for managed applications as the definition of the application is in a source code management (SCM) system.
Discovered applications are applications that already exist on managed clusters and are not part of the ACM application model. ACM can discover these applications through mechanisms like OpenShift Container Platform GitOps or Argo CD operators, allowing for some level of visibility and potentially limited management. For example, ACM might be able to monitor their health, enforce policies on them, or integrate them with other ACM features like disaster recovery. OpenShift API for Data Protection is deployed along with ACM to backup and restore the application components in case of failure or relocation of the application.
## Failover vs Relocate
In OpenShift disaster recovery, failover refers to switching an application and its state from a primary cluster to a secondary cluster during a disaster, while relocate refers to moving an application and its state back to the original primary cluster after it is recovered. Both are managed through Fusion Data Foundation's DR solution and utilize the PlacementRule for application placement.

### Failover
- **Purpose:** Switches application and state to a secondary cluster when the primary cluster is unavailable due to a disaster.
- **Process:** Initiated by an administrator, the DR solution orchestrates the application's relocation to the secondary cluster.
- **Data Loss:** Ideally, failover is designed to be non-disruptive, minimizing data loss.
- **Example:** A cluster in one region becomes unavailable, and the application is automatically moved to a secondary cluster in a different region.

### Relocate (Failback)
- **Purpose:** Moves the application and its state back to the original primary cluster after the disaster has been resolved and the primary cluster is restored.
- **Process:** Also initiated by an administrator, the DR solution orchestrates the relocation back to the primary cluster.
- **Data Loss:** Relocation is planned and controlled to ensure no data loss occurs during the switchback.
- **Example:** The cluster in the original region is restored and operational, and the application is moved back to its original location.

### Key Differences
- **Direction:** Failover moves the application away from the primary cluster, while relocate (failback) moves it back.
- **Purpose:** Failover is a defensive measure during a disaster, while relocate is the recovery step after the disaster.
- **Initiation:** Both are typically administrator-initiated processes.
## Product disclaimer

{% include shared/product-disclaimer.md %}

## Getting help

{% include shared/getting-help.md %}
