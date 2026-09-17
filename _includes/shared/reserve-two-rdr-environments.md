This lab requires two (2) IBM Fusion environments provisioned through IBM Technology Zone. Reserve both at the same time to minimize wait time.

> **Tip:** Reserve the environments far enough in advance. Each environment can take 30–60 minutes to provision.

> **Important:** To complete the lab successfully, set **OCS/ODF size** to **None** on both environments. This disables automatic ODF/FDF deployment so you can install and configure it manually.

## Reserve cluster local-cluster

The **local-cluster** hosts your primary workloads and Red Hat ACM.

1. Open a web browser and go to the [IBM Technology Zone – IBM Fusion Collection](https://techzone.ibm.com/collection/ibm-spectrum-fusion).
1. From the product overview page, click **Environments** in the left-hand menu.
1. Click the **Reserve** button on the **Beta: Storage Fusion on OCP w/ODF and Scale** tile.
1. Select **Reserve now** or **Schedule for later**.
1. Set **Name** to `local-cluster` and select the **Education** purpose tile.
1. Enter a **Purpose description** (e.g., *Using the environment for course work*).
1. Select **Preferred Geography:** `itzvmware-spectrum – AMERICAS – us-east-region – wdc04`.
1. Configure the following options:
   - **OpenShift Version** — 4.18 (required)
   - **Worker Node Count** — 3
   - **Worker Node Flavor** — 16 vCPU x 64 GB – 300 GB ephemeral storage
   - **OCS/ODF Size** — **None** (required)
   - Leave all three **network options** at their defaults.
1. Accept the Terms and Conditions and click **Submit**.

> **Note:** If you have any difficulties, visit the [IBM Technology Zone Help page](https://techzone.ibm.com/help) or email [techzone.help@ibm.com](mailto:techzone.help@ibm.com).

## Reserve cluster ocp2

The **ocp2** cluster is the disaster recovery site. It must use **different** network CIDRs from local-cluster to allow Submariner cross-cluster connectivity.

1. Open a web browser and go to the [IBM Technology Zone – IBM Fusion Collection](https://techzone.ibm.com/collection/ibm-spectrum-fusion).
1. From the product overview page, click **Environments** in the left-hand menu.
1. Click the **Reserve** button on the **Beta: Storage Fusion on OCP w/ODF and Scale** tile.
1. Select **Reserve now** or **Schedule for later**.
1. Set **Name** to `ocp2` and select the **Education** purpose tile.
1. Enter a **Purpose description**.
1. Select **Preferred Geography:** `itzvmware-spectrum – AMERICAS – us-east-region – wdc04`.
1. Configure the following options:
   - **OpenShift Version** — 4.18 (required)
   - **Worker Node Count** — 3
   - **Worker Node Flavor** — 16 vCPU x 64 GB – 300 GB ephemeral storage
   - **OCS/ODF Size** — **None** (required)
1. Modify the **network settings** as follows:

| Setting | Value |
| --- | --- |
| Machine Network | `192.168.242.0/24` |
| OCP/Kubernetes Cluster Network | `10.132.0.0/14` |
| OCP/Kubernetes Service Network | `172.31.0.0/16` |

1. Accept the Terms and Conditions and click **Submit**.

> **Important:** The distinct network CIDRs for ocp2 are required. Submariner uses these non-overlapping networks to establish cross-cluster connectivity for disaster recovery.

## Connect to the environments

Once both environments show **Ready** status, retrieve access details from your [IBM Technology Zone reservations page](https://techzone.ibm.com/my/reservations):

- **Desktop URL** — direct browser access to the OpenShift console
- **kubeadmin** username and password
- **Bastion SSH connection** and password for CLI access

> **Note:** Connectivity to the OpenShift console may be lost during the first 30 minutes after the "Reservation Ready" email. The MachineConfigPool is still updating and rebooting worker nodes during this time.
