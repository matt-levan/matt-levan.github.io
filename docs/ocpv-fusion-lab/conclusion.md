---
layout: default
title: "Workshop Conclusion"
permalink: /ocpv-fusion-lab/conclusion/
nav_order: 8
parent: "OCP Virtualization with IBM Fusion Lab"
---

Congratulations on completing the Modernizing Virtualization with Red Hat OpenShift Virtualization and IBM Fusion hands-on lab!

## What you learned

In this workshop, you gained hands-on experience with:

- Navigating the OpenShift Virtualization console and understanding the operator architecture
- Creating and managing virtual machines using templates and YAML manifests
- Working with IBM Fusion storage classes for persistent VM storage
- Performing VM lifecycle operations including start, stop, pause, snapshots, and cloning
- Executing live migration of VMs between worker nodes
- Performing live storage migration between storage classes
- Backing up and restoring applications and VMs using IBM Fusion Backup & Restore

## Key takeaways

- Red Hat OpenShift Virtualization enables running VMs as native Kubernetes resources alongside containers on a single platform
- IBM Fusion provides enterprise-grade storage with snapshot, cloning, and backup capabilities for VM workloads
- Live migration requires ReadWriteMany (RWX) storage and enables non-disruptive maintenance operations
- IBM Fusion Backup & Restore protects both containerized and VM workloads with customizable policies and application-consistent recipes

## Next steps

- Explore advanced VM networking with Multus and SR-IOV
- Implement disaster recovery patterns with IBM Fusion
- Pursue the Red Hat Certified Specialist in OpenShift Virtualization certification

## References

- [Red Hat OpenShift Virtualization documentation^](https://docs.redhat.com/en/documentation/openshift*container*platform/4.20/html/virtualization/index)
- [IBM Fusion documentation^](https://www.ibm.com/docs/en/fusion-software/2.12.0)
- [Migration Toolkit for Virtualization documentation^](https://docs.redhat.com/en/documentation/migration*toolkit*for_virtualization/)

## Feedback

We value your feedback on this workshop. Share your thoughts with the lab facilitators or through the event feedback channels.
