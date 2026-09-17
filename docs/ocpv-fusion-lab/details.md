---
layout: default
title: "Workshop Details"
permalink: /ocpv-fusion-lab/details/
nav_order: 3
parent: "OCP Virtualization with IBM Fusion Lab"
---

## Timing and schedule

### Full workshop (90 minutes)

- ***Module 1***: Exploring the environment (20 minutes)
- ***Module 2***: VM lifecycle management (25 minutes)
- ***Module 3***: Workload migration (25 minutes)
- ***Module 4***: IBM Fusion Backup & Restore (20)

### Abbreviated workshop (60 minutes)

- ***Module 1***: Exploring the environment (20 minutes)
- ***Module 2***: VM lifecycle management (25 minutes)
- ***Module 3***: Workload migration (15 minutes, core exercises only)

## Technical requirements

### Software versions

- Red Hat OpenShift 4.20
- OpenShift Virtualization 4.20
- IBM Fusion 2.12
- Migration Toolkit for Virtualization (latest compatible version)

### Cluster configuration

- Multinode OpenShift cluster
- Cluster admin access
- OpenShift Virtualization operator installed
- IBM Fusion storage operator installed and configured
- Pre-configured storage classes for VM workloads

### Environment access

Participants need access to:

- Red Hat OpenShift web console
- OpenShift CLI (`oc`) via bastion host or web terminal
- Web browser (Chrome, Firefox, Safari, or Edge)

### Network requirements

- Internet connectivity for accessing the OpenShift console
- Access to the lab environment URLs provided in credentials

## Environment setup

### Pre-configured environment

This lab environment is fully pre-configured. The following components are already installed and ready:

- OpenShift Virtualization operator and HyperConverged custom resource
- IBM Fusion storage classes and persistent volume provisioner
- VM templates for common operating systems
- Migration Toolkit for Virtualization operator (Module 3)
- Sample workloads for migration exercises

### Setup validation

Switch to the **Bastion** tab on the right and run these commands to verify your environment:

```bash
# Verify OpenShift CLI access
oc whoami

# Verify cluster version
oc get clusterversion

# Check OpenShift Virtualization operator status
oc get csv -n openshift-cnv | grep kubevirt

# Check IBM Fusion storage classes
oc get storageclass | grep fusion

# Verify VM templates are available
oc get templates -n openshift
```

== Follow-up resources

### Next steps for participants

- link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/virtualization/index[Red Hat OpenShift Virtualization documentation^]
- link:https://www.ibm.com/docs/en/fusion-software/2.12.0[IBM Fusion 2.12 documentation^]
- link:https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/[Migration Toolkit for Virtualization documentation^]

### Additional learning paths

- **Intermediate**: Advanced VM networking with multus and SR-IOV
- **Advanced**: Disaster recovery and high availability patterns with IBM Fusion
- **Certification**: Red Hat Certified Specialist in OpenShift Virtualization

== Authors and contributors

**Lab ID**: LB2298 +
**Primary Author**: Red Hat Technical Marketing +
**Last Updated**: February 2026 +
**Workshop Version**: 1.0
