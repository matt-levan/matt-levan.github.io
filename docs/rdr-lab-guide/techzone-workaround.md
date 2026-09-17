---
layout: default
title: "TechZone OCPv Workaround"
permalink: /rdr-lab-guide/techzone-workaround/
nav_order: 4
parent: "IBM Fusion RDR Lab Guide"
---

# TechZone OCPv: Submariner Setup Workaround

This page documents the steps required to connect two IBM Technology Zone OpenShift Virtualization (OCPv) clusters using Submariner. Because TechZone automatically imports and manages your reserved clusters through its own ACM instance, you must disable that first before deploying your own ACM and Submariner.

> **Prerequisites:** Two TechZone OCPv reservations with different cluster and service subnets (as configured in the [Reserve Two Environments](./reserve-two-environments/) step).

---

## Step 1 — Disable TechZone ACM auto-import

TechZone ACM is the managed hub that automatically imports and monitors your reserved OpenShift clusters. It would interfere with your own ACM instance, so you must disable it first.

1. Open the **VM Remote Console** for your reservation.
1. Click **Techzone ACM** under **Cluster management**.
1. The page loads the current ACM status.
1. Click the toggle switch **ACM Auto-Import** to **Disabled**.

Allow **15–30 minutes** to sync and reconcile the configuration.

Then clean up the TechZone ACM artifacts from each cluster. Run the following on **each cluster**:

> **Warning:** Review the script at the URL below before executing it in your cluster to confirm you understand what it removes.

```bash
bash <(curl -s https://itz-ocpv-downloads.s3.us-east.cloud-object-storage.appdomain.cloud/scripts/cleanup-managed-cluster.sh)
```

Verify the ACM klusterlet is removed from both clusters:

```bash
oc get klusterlet
```

---

## Step 2 — Label worker-1 as the Submariner gateway

Submariner requires exactly one node per cluster designated as the cross-cluster gateway. Run this on **each cluster**:

```bash
oc get node | grep "worker-1 " | cut -d " " -f1 | xargs -I {} oc label node {} submariner.io/gateway=true
```

Then retrieve your **hub cluster's** API hostname and its public IP address, and annotate `worker-1`. Run this **only on the hub cluster (local-cluster)**:

```bash
oc whoami --show-server | cut -d "/" -f3 | cut -d ":" -f1 | xargs -I {} nslookup {} 1.1.1.1
```

```bash
oc get node | grep "worker-1 " | cut -d " " -f1 | xargs -I {} oc annotate node {} \
  gateway.submariner.io/preferred-server=true \
  gateway.submariner.io/public-ip=ipv4:<PUBLIC_IP>
```

Replace `<PUBLIC_IP>` with the IP address returned by the `nslookup` command above.

---

## Step 3 — Deploy ACM on your hub

Install Red Hat Advanced Cluster Management (RHACM) on `local-cluster` following the standard procedure described in the [Configure RHACM](./configure-rhacm/) section.

---

## Step 4 — Install Submariner add-on and connect two clusters

Install the Submariner add-on and connect both clusters following the standard procedure described in the [Configure RHACM → Configure Submariner](./configure-rhacm/) section.

---

## Step 5 — Submariner health check fix (OVN-Kubernetes workaround)

There is a known issue with Submariner health check failures when using OVN-Kubernetes in local gateway mode. Red Hat is planning to resolve this in a future release.

Apply the following workaround on **both clusters** after installing the Submariner ACM add-on:

```bash
# Apply the workaround
oc apply -f https://itz-ocpv-downloads.s3.us-east.cloud-object-storage.appdomain.cloud/scripts/submariner-ovn-snat-workaround.yaml

# Verify DaemonSet is running
oc get ds -n submariner-operator submariner-ovn-snat-fix
```

Allow **5–10 minutes** for Submariner to establish its connection and show a healthy status.

> **Reference:** `ovn-local-gateway-health-check` — this is a known issue tracked by Red Hat.
