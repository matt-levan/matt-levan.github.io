---
layout: default
title: "Reserve TechZone Environment"
permalink: /hcp-lab-guide/reserve-a-technology-zone-environment/
nav_order: 3
parent: "IBM Fusion HCP Lab Guide"
---

# Reserve a Technology Zone Environment

{% include shared/reserve-techzone-environment.md %}

> **Important (HCP-specific):** When reserving the HCP environment, set **OCS/ODF size** to **None** to disable automatic ODF deployment — you will install and configure FDF manually as described in this guide. Also ensure the environment includes **infra nodes** (3 nodes with 2 TB internal storage for LVM etcd storage).
