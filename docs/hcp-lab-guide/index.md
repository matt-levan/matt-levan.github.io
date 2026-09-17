---
layout: default
title: "IBM Fusion HCP Lab Guide"
permalink: /hcp-lab-guide/
nav_order: 1
---

# Introduction

This hands-on lab guide is your practical companion for deploying and managing IBM Fusion in a Red Hat OpenShift Hosted Control Plane (HCP) environment. Whether you're exploring Fusion for the first time or deepening your expertise, this guide walks you through the full lifecycle—from environment setup to hosted cluster creation—using real-world tools and configurations.
Built for technical professionals, this lab emphasizes clarity, repeatability, and hands-on experience. You’ll install and configure key components like the IBM Fusion Operator, Fusion Data Foundation in Provider mode, OpenShift Virtualization, MetalLB, and more.
## About this lab
In this lab, you will work with Hosted Control Plane (HCP) clusters, a modern OpenShift deployment model that separates the control plane from the compute infrastructure. For these clusters, the control plane components—such as the API server, etcd, and controller manager—are hosted on an IBM Fusion cluster. The compute nodes, on the other hand, are provisioned as either virtual machines (via OpenShift Virtualization) or bare metal servers.
Unlike traditional OpenShift clusters, where each cluster includes its own dedicated control plane nodes, the hosted control plane model allows these components to run as lightweight pods on a centralized Fusion system. This decoupled architecture enables greater flexibility, scalability, and resource efficiency.
The IBM Fusion system can host multiple OpenShift clusters simultaneously. Clusters can be created and deleted on demand, allowing you to tailor environments to specific workload needs and optimize resource usage.
Key Benefits of Hosted Control Planes
- Cost Efficiency
  - No need for dedicated control plane nodes per cluster
  - Fewer bare metal nodes required overall
  - Compute nodes can be provisioned as VMs or bare metal, depending on workload needs
- Cluster On Demand
  - Clusters can be created when needed and deleted when no longer in use
  - Resources are automatically reclaimed and made available for new deployments
What You’ll Learn
Participants will gain hands-on experience with:
- Deploying and configuring Fusion Data Foundation in Provider mode.
- Deploying and configuring MetalLB load balancer to support hosted control plane clusters.
- Use infra nodes to host a Logical Volume Manager (LVM) volume group (VG) for use by hosted cluster etcd pods.
- Creating and managing a hosted cluster using Red Hat multicluster engine for Kubenetes.

![Screenshot]({{ site.baseurl }}/assets/images/hcp-lab-guide/about-this-lab-01.png)

Lab Components
- Three (3) control plane nodes.
- Three (3) infra nodes with internal disks for use by LVM.
- Three (3) storage nodes with internal disks for use by FDF in provider mode.
- Three (3) workers nodes to host user workload and virtual machines (VMs)
Infra (Infrastructure) nodes
Infrastructure machine sets can be used to create machines that host only infrastructure components, such as the default router, the integrated container image registry, and the components for cluster metrics and monitoring. These infrastructure machines are not counted toward the total number of subscriptions that are required to run the environment.
In a production deployment, it is recommended that you deploy at least three machine sets to hold infrastructure components. Red Hat OpenShift Service Mesh deploys Elasticsearch, which requires three instances to be installed on different nodes. Each of these nodes can be deployed to different availability zones for high availability. This configuration requires three different machine sets, one for each availability zone. In global Azure regions that do not have multiple availability zones, you can use availability sets to ensure high availability.
> NOTE: More information about infra nodes and configuring them can be found in the Red Hat Knowledgebase article 5034771 (https://access.redhat.com/solutions/5034771).
## Product disclaimer

{% include shared/product-disclaimer.md %}

## Getting help

{% include shared/getting-help.md %}
