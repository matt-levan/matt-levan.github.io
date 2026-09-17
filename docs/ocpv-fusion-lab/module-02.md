---
layout: default
title: "Module 2: VM Lifecycle Management"
permalink: /ocpv-fusion-lab/module-02/
nav_order: 5
parent: "OCP Virtualization with IBM Fusion Lab"
---

This lab module provides a structured introduction to virtual machine (VM) lifecycle management using Red Hat OpenShift Virtualization. Attendees will gain practical skills to create, operate, migrate, snapshot and decommission virtual machines within a Red Hat OpenShift cluster.

Red Hat OpenShift Virtualization is an add-on that enables running virtual machines alongside containers on the same platform. It is built on the open-source KubeVirt project and uses the Linux Kernel-based Virtual Machine (KVM) hypervisor underneath.

As such, VMs are integrated to the platform using Custom Resource and Custom Resource Definition objects. To put it simply, VM are not treated as foreign objects managed by a separate hypervisor but like any containerized application. This means every tool — `oc`, `kubectl`, RBAC, NetworkPolicy, GitOps — applies equally to VMs and containers.

By the end of this module, attendees will understand how traditional VM operations map to Red Hat OpenShift native constructs and can manage the VM lifecycle using both the web console and/or command-line tools.

## Learning objectives

By the end of this module, you will be able to:

- What are the core Custom Resources used by Red Hat OpenShift Virtualization
- Virtual Machine various states and their meaning

## Core Red Hat OpenShift Virtualization Custom Resources (CRs)

Three Custom Resource Definitions (CRDs) form the foundation of VM lifecycle management:

`VirtualMachine` (VM)::
The persistent definition of a virtual machine, analogous to a Deployment. It records the desired state and survives reboots. Created once, it persists until explicitly deleted.

`VirtualMachineInstance` (VMI)::
Represents a single running instance of a VM, analogous to a Pod. It is ephemeral: a VMI is created at start-up and deleted at shutdown. The VM controller reconciles the desired state in the VM object against the actual VMI.

`DataVolume` (DV)::
A CDI (Containerized Data Importer) object that manages the import, cloning, or upload of disk images into PersistentVolumeClaims. DVs handle the heavy lifting of getting OS images onto cluster storage.

> **Tip:** The **VM is to VMI as Deployment is to Pod**. The VM is defined once and the controller takes care of the creation, the restart, and the deletion of the corresponding VMI objects.

## Virtual Machine states

A virtual machine transitions through specific states during its lifecycle. It is essential to understand each state:

| State | Description | Allowed Transitions |
| --- | --- | --- |
| Stopped | VM is defined but not running. No CPU or memory consumed but storage is allocated. | → Running, → Paused (offline) |
| Starting | VMI pod is being scheduled and then launched. | → Running, → Failed |
| Running | VM is active. A VMI object and pod exist on a node for this VM. | → Paused, → Stopped, → Migrating |
| Paused | vCPU execution halted; memory retained on the node. Storage remains allocated | → Running, → Stopped |
| Migrating | Live migration is in progress to move the VM from one node to another. | → Running (on target) |
| Failed | VMI encountered an unrecoverable error. | → Stopped (manual restart) |

## Creating VMs

Red Hat OpenShift Virtualization provides three primary ways to create a virtual machine, each suited to different workflows:

Web Console Wizard::
Guided UI experience with templates. Ideal for ad-hoc creation or new users.

YAML Manifest::
Declarative, version-controllable definition. Preferred for automation and GitOps pipelines.

virtctl CLI::
Imperative command-line creation. Useful for quick provisioning in scripted environments.

### VM manifest anatomy

A `VirtualMachine` manifest is a standard Kubernetes object. The following annotated example creates a RHEL 9 VM with 2 vCPUs, 4 GiB RAM, and a 30 GiB boot disk cloned from a golden image.

```bash
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: rhel9-webserver
  namespace: vmlab-student
  labels:
    app: webserver
spec:
  running: false               # <1>
  template:
    metadata:
      labels:
        kubevirt.io/vm: rhel9-webserver
    spec:
      domain:
        cpu:
          cores: 2             # <2>
          sockets: 1
          threads: 1
        memory:
          guest: 4Gi
        devices:
          disks:
          - name: rootdisk
            disk:
              bus: virtio      # <3>
          - name: cloudinitdisk
            disk:
              bus: virtio
          interfaces:
          - name: default
            masquerade: {}     # <4>
      networks:
      - name: default
        pod: {}
      volumes:
      - name: rootdisk
        dataVolume:
          name: rhel9-webserver-rootdisk
      - name: cloudinitdisk
        cloudInitNoCloud:
          userData: |
            #cloud-config
            user: cloud-user
            password: redhat123
            chpasswd: { expire: False }
            runcmd:
              - dnf install -y httpd
              - systemctl enable --now httpd
  dataVolumeTemplates:         # <5>
  - metadata:
      name: rhel9-webserver-rootdisk
    spec:
      storage:
        accessModes: [ReadWriteMany]
        resources:
          requests:
            storage: 30Gi
        storageClassName: ocs-storagecluster-ceph-rbd-virtualization
      source:
        pvc:
          namespace: openshift-virtualization-os-images
          name: rhel9-guest-image
```
<1> VM is created in a stopped state. Set to `true` to start immediately.
<2> vCPU topology: 2 cores × 1 socket × 1 thread = 2 vCPUs total.
<3> `virtio` is the paravirtualized driver — fastest option for Linux guests.
<4> `masquerade` provides NAT connectivity via the pod network.
<5> `dataVolumeTemplates` ties the disk lifecycle to the VM — the PVC is deleted with the VM.

TIP: Using `dataVolumeTemplates` keeps the disk definition co-located with the VM. When the VM is deleted, the associated DataVolume and PVC are also deleted automatically unless the PVC is first unlinked.

### Cloud-init customization

Cloud-init runs inside the VM on first boot and configures the guest operating system. OpenShift Virtualization supports two cloud-init data sources:

`cloudInitNoCloud`::
Data is passed directly in the VMI spec as a volume. No DHCP or metadata server required. Suitable for most lab and production scenarios.

`cloudInitConfigDrive`::
Compatible with OpenStack-style config drives. Used when migrating workloads from OpenStack environments.

A practical cloud-init configuration covering common provisioning tasks:

```bash
#cloud-config
hostname: rhel9-webserver
user: cloud-user
password: redhat123
chpasswd: { expire: False }
ssh*authorized*keys:
  - ssh-rsa AAAA...your-public-key
packages:
  - httpd
  - firewalld
runcmd:
  - systemctl enable --now httpd
  - firewall-cmd --add-service=http --permanent
  - firewall-cmd --reload
write_files:
  - path: /var/www/html/index.html
    content: |
      <h1>Hello from OpenShift Virtualization!</h1>
```

## Exercise 1: Create and Inspect Virtual Machine

In this exercise you will create a RHEL 9 virtual machine from a YAML manifest, verify the underlying Kubernetes objects, and connect to the VM console.

1. Setup your namespace

   ```bash
   oc new-project vmlab-student
   ```

Expected output:
+ 
```bash
Now using project "vmlab-student" on server "https://api.ocp.t26dj.sandbox4392.opentlc.com:6443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app rails-postgresql-example

to build a new example application in Ruby. Or use kubectl to deploy a simple Kubernetes application:

    kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.43 -- /agnhost serve-hostname
```

1. Create VM Manifest

   ```bash
   cat > rhel9-webserver.yaml << 'EOF'
   apiVersion: kubevirt.io/v1
   kind: VirtualMachine
   metadata:
     name: rhel9-webserver
     namespace: vmlab-student
   spec:
     runStrategy: Manual
     template:
       spec:
         domain:
           cpu:
             cores: 2
             sockets: 1
             threads: 1
           memory:
             guest: 4Gi
           devices:
             disks:
             - name: rootdisk
               disk:
                 bus: virtio
             - name: cloudinitdisk
               disk:
                 bus: virtio
             interfaces:
             - name: default
               masquerade: {}
         networks:
         - name: default
           pod: {}
         volumes:
         - name: rootdisk
           dataVolume:
             name: rhel9-webserver-rootdisk
         - name: cloudinitdisk
           cloudInitNoCloud:
             userData: |
               #cloud-config
               user: cloud-user
               password: redhat123
               chpasswd: { expire: False }
               ssh*authorized*keys:
                 - `{PUBKEY}`
               yum_repos:
                 baseos:
                   name: CentOS Stream 9 BaseOS
                   baseurl: https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/os/
                   enabled: true
                   gpgcheck: false
                 appstream:
                   name: CentOS Stream 9 AppStream
                   baseurl: https://mirror.stream.centos.org/9-stream/AppStream/x86_64/os/
                   enabled: true
                   gpgcheck: false
               packages:
                 - httpd
                 - firewalld
               runcmd:
                 - echo "This is the WEB server before failure." | sudo tee /var/www/html/index.html
                 - systemctl enable --now firewalld
                 - systemctl enable --now httpd
                 - firewall-cmd --permanent --add-service=http
                 - firewall-cmd --reload
     dataVolumeTemplates:
     - metadata:
         name: rhel9-webserver-rootdisk
       spec:
         storage:
           accessModes: [ReadWriteMany]
           resources:
             requests:
               storage: 30Gi
           storageClassName: ocs-storagecluster-ceph-rbd-virtualization
         sourceRef:
             kind: DataSource
             name: rhel9
             namespace: openshift-virtualization-os-images
   EOF
   ```

1. Generate SSH key

   ```bash
   ssh-keygen
   ```

NOTE: Use <CR> for each question

1. Verify the publick key has been generated

   ```bash
   cat ~/.ssh/id_rsa.pub
   ```

Expected output:

```bash
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6K3QfkXhrBio5lWExoRgfx`83GWW5MDFw542kAVU`8eo5YdageNRezQetYTglx5B`ex/u8XfGUSui4RjNx1Z0X7Jjnz8XmaTnDqTu3SwdGyAei`h`UOSq9DkhTLc6HaEm3IoJweNxhObULYF3R`O9r2OdttngYIb02F0YomnGuxI8fvzXzI3ORjCxf6`1N3fLGpw6D`HqVEyhekqI0ZtNSNo8k9vapFT`fI0l5dBT3GVnDhtmI9JD``0QPqEB2CagOIu6XbOAfMz`/8R4MUeNE6J/lWU0MwleF6OudN/o1TZY/1jtQLTuVpGVejUwyHoCBG/h0M72EsAUd3upf8wDI1a/oTvdGyURP7mSQwqRRTSnNLbGRuo3W0BJIQW5FnVUzf461WwZ`Z0DIm65mpmpLNfeqf3aBF90OgwBOnJ1fOCfTGYu7Z9sRXMYUVgjpbdSTR1u7wovFrNvrSj8e6nPp5nHpAq5kOjvtYNo`MUQRIrvVBifbgxR2z/ExhxHlFs= lab-user@bastion.t26dj.internal
```

1. Customize your VM custom resource before we create it using your new SSH key

   ```bash
   export THEKEY=$(cat ~/.ssh/id_rsa.pub)
   sed -i -e "s*`{PUBKEY}`*$`{THEKEY}`_g" rhel9-webserver.yaml
   ```

NOTE: We are using `_` as a delimiter for the `sed` command knowing that the generated public key may contain `/` characters.

1. Apply the manifest to create the virtual machine

   ```bash
   oc apply -f rhel9-webserver.yaml
   ```

Expected output:

```bash
virtualmachine.kubevirt.io/rhel9-webserver created
```

1. Verify the VM status

   ```bash
   oc get vm -n vmlab-student
   ```

Expected output:

```bash
NAME              AGE   STATUS    READY
rhel9-webserver   <age> Stopped   False
```

NOTE: You can see that the status of the VM is `Stopped` and the readiness is `False`

1. Install CLI tool on your bastion node

   ```bash
   curl -L https://$(oc get route hyperconverged-cluster-cli-download -n openshift-cnv -o jsonpath='{.spec.host}')/amd64/linux/virtctl.tar.gz -o virtctl.tar.gz
   tar -xzf virtctl.tar.gz
   chmod +x virtctl && sudo mv virtctl /usr/local/bin/
   ```

1. Start the VM and observe object creation

   ```bash
   virtctl start rhel9-webserver -n vmlab-student
   ```

NOTE: This will create the VMI object

Expected output:

```bash
VM rhel9-webserver was scheduled to start
```

1. Watch the VM reach Running state

   ```bash
   oc get vm rhel9-webserver -n vmlab-student -w
   ```

Expected output:

```bash
NAME              AGE     STATUS    READY
rhel9-webserver   <age>   Running   True
```

TIP: Wait for status to be `Running` and readiness to be `True`. Then hit `Ctrl-C` to stop the watch.

1. Observe the VMI object that was created

   ```bash
   oc get vmi -n vmlab-student
   ```

Expected output

```bash
NAME              AGE    PHASE     IP             NODENAME                                   READY
rhel9-webserver   <age>  Running   10.<x.y.z>     ip-<nodename>.us-east-2.compute.internal   True
```

1. Find the virt-launcher pod backing this VM

   ```bash
   oc get pods -n vmlab-student -l vm.kubevirt.io/name=rhel9-webserver
   ```

Expected output:

```bash
NAME                                  READY   STATUS    RESTARTS   AGE
virt-launcher-rhel9-webserver-<xxx>   2/2     Running   0          <age>
```

1. Describe the VMI for scheduling and resource details

   ```bash
   oc describe vmi rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
[truncated]
Events:
  Type    Reason            Age    From                       Message
  ----    ------            ----   ----                       -------
  Normal  SuccessfulCreate  4m22s  virtualmachine-controller  Created virtual machine pod virt-launcher-rhel9-webserver-<xxx>
  Normal  Created           4m10s  virt-handler               VirtualMachineInstance defined.
  Normal  Started           4m10s  virt-handler               VirtualMachineInstance started.
```

1. Check DataVolume import status

   ```bash
   oc get dv -n vmlab-student
   ```

Expected output:

```bash
NAME                       PHASE       PROGRESS   RESTARTS   AGE
rhel9-webserver-rootdisk   Succeeded   100.0%                <age>
```

NOTE: Note that the import progress field shows `100.0%`

1. Connect to the VM console

   ```bash
   # Attach to the serial console (Ctrl+] to exit)
   virtctl console rhel9-webserver -n vmlab-student
   ```

WARNING: It will take some time for the VM to start and the `cloud-init` step to complete. Once messages stop flowing on your screen, the VM is ready.

1. Log in to the VM

   ```bash
   rhel9-webserver login: cloud-user
   Password: redhat123
   ```

TIP: Hit <CR> to get to the login prompt. The VM username is `cloud-user` and the password `redhat123` as illustrated above.

1. Verify the VM deployment is complete (repeat until you see the expected status)

   ```bash
   sudo cloud-init status
   ```

Expected output:

```bash
status: done
```

1. Verify the WEB server status

   ```bash
   sudo systemctl status httpd
   ```

Expected output:

```bash
● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; preset: di>
     Active: active (running) since Tue 2026-03-24 15:48:57 EDT; 5h 14min ago
       Docs: man:httpd.service(8)
   Main PID: 7918 (httpd)
     Status: "Total requests: 1; Idle/Busy workers 100/0;Requests/sec: 5.3e-05;>
      Tasks: 177 (limit: 22797)
     Memory: 14.9M (peak: 15.4M)
        CPU: 1min 30.890s
[truncated]
```

1. Verify the WEB server is operational

   ```bash
   curl http://localhost
   ```

Expected output:

```bash
This is the WEB server before failure.
```

1. Exit your VM

   ```bash
   exit
   ```

TIP: Hit `CTRL+5` to disconnect from the VM console

### Verify

1. Confirm the VM is running and on what specific node

   ```bash
   oc get pods -l vm.kubevirt.io/name=rhel9-webserver -o custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
   ```

Expected output:

```bash
NAME                                  STATUS    NODE
virt-launcher-rhel9-webserver-<xxx>   Running   ip-<nodename>.us-east-2.compute.internal
```

1. Confirm how many PVCs were created

   ```bash
   oc get pvc -o custom-columns="NAME:.metadata.name,SIZE:.status.capacity.storage,ACCESS MODES:.spec.accessModes[0],STORAGE CLASS:.spec.storageClassName"
   ```

Expected output:

```bash
NAME                       SIZE   ACCESS MODES    STORAGE CLASS
rhel9-webserver-rootdisk   30Gi   ReadWriteMany   ocs-storagecluster-ceph-rbd-virtualization
```

1. Confirm the IP address assigned to the VM

   ```bash
   oc get vmi -o yaml | grep ipAddress:
   ```

Expected output:

```bash
      ipAddress: 10.<x>.<y>.<z>
```

In this exercise you have verified:

- On which node the VM is running
- The number of PVCs for this VM is 1
- The number of DataVolumes for this VM is 1
- You have verified the IP address assigned to the VM

## Operating virtual machines

### `virtctl` CLI

The `virtctl` binary is the primary command-line interface for VM operations that go beyond basic Kubernetes resource management. It communicates with the `virt-api` server to execute actions like start, stop, console access, and live migration. Install it directly from the cluster to ensure version compatibility:

```bash
curl -L https://$(oc get route hyperconverged-cluster-cli-download -n openshift-cnv -o jsonpath='{.spec.host}')/amd64/linux/virtctl.tar.gz -o virtctl.tar.gz
tar -xzf virtctl.tar.gz
chmod +x virtctl && sudo mv virtctl /usr/local/bin/

virtctl version
```

Key `virtctl` commands and their purposes:

| Command | Purpose |
| --- | --- |
| `virtctl start <vm>` | Power on a stopped VM |
| `virtctl stop <vm>` | Gracefully power off a running VM |
| `virtctl restart <vm>` | Graceful reboot (stop + start) |
| `virtctl pause <vm>` | Freeze vCPU execution (memory retained) |
| `virtctl unpause <vm>` | Resume a paused VM |
| `virtctl migrate <vm>` | Initiate live migration to another node |
| `virtctl console <vm>` | Attach to the VM serial console |
| `virtctl vnc <vm>` | Open a VNC session to the VM display |
| `virtctl ssh <vm>` | SSH into the VM via API tunnel |
| `virtctl addvolume <vm>` | Hot-plug a PVC as a disk |
| `virtctl removevolume <vm>` | Hot-unplug a previously attached disk |

### Power operations

The `start`, `stop`, and `restart` operations manage the VM power state. These actions are recorded in the VM status and trigger VMI creation or deletion accordingly.

```bash
# Start a stopped VM
virtctl start <vm-name> -n <namespace>

# Graceful shutdown (sends ACPI power-off signal to guest OS)
virtctl stop <vm-name> -n <namespace>

# Force stop (equivalent to pulling the power cable — use with caution)
virtctl stop --force --grace-period=0 <vm-name> -n <namespace>

# Graceful restart (stop + start, preserves VM definition)
virtctl restart <vm-name> -n <namespace>

# Alternatively, use oc patch to toggle running state
virtctl patch vm <vm-name> -n <namespace> \
  --type merge -p '{"spec":{"running":true}}'
```

TIP: A graceful stop sends ACPI signals to the guest OS, allowing it to flush disk buffers and unmount filesystems cleanly. Always prefer graceful stop over force stop to avoid data corruption.

### Pause and Unpause

Pausing a VM suspends vCPU execution while keeping the VM's memory contents live in RAM on the node. This is useful for temporarily freezing a VM to take a consistent snapshot or to free up CPU cycles on a busy node.

```bash
# Pause a running VM
virtctl pause <vm-name> -n <namespace>

# Verify the paused state
oc get vmi <vm-name> -n <namespace> -o jsonpath='{.status.phase}'

# Resume the VM
virtctl unpause <vm-name> -n <namespace>
```

### Accessing a VM

Red Hat OpenShift Virtualization provides three access methods depending on the use case.

#### Serial Console

Direct serial console access works regardless of network configuration. Use it for initial setup, troubleshooting boot issues, or when SSH is unavailable.

```bash
virtctl console <vm-name> -n <namespace>
# Press Ctrl+] to detach from the console
```

#### VNC Graphical Session

VNC provides a graphical display useful for desktop VMs or when a GUI is required.

```bash
# Opens VNC in the default browser via port-forward tunnel
virtctl vnc <vm-name> -n <namespace>
```

#### SSH via API Tunnel

The `virtctl ssh` subcommand tunnels SSH through the Kubernetes API, avoiding the need to expose SSH ports via a Service or route.
 
```bash
# SSH using cloud-user and the injected key
virtctl ssh cloud-user@vm/<vm-name> -n <namespace>

# Use a specific private key
virtctl ssh cloud-user@vm/<vm-name> -n <namespace> \
  --local-ssh-opts='-i ~/.ssh/id_rsa'
```
 
TIP: You can also use the VMI to `ssh` into the virtual machine

### Storage concepts

Each VM disk maps to a PersistentVolumeClaim (PVC) in Kubernetes. Understanding access modes is critical because they directly affect which operations are possible:

ReadWriteOnce (RWO)::
The PVC can be mounted by a single node. Sufficient for stopped or non-migrating VMs, but live migration requires RWX.

ReadWriteMany (RWX)::
The PVC can be mounted by multiple nodes simultaneously. Required for live migration because both source and target nodes must access the disk at the same time.

ReadOnlyMany (ROX)::
Read-only access from multiple nodes. Used for shared, immutable data.

WARNING: Always provision VM boot disks with *ReadWriteMany* access mode if you plan to use live migration. Attempting to migrate a VM with RWO disks will fail with an error in the `VirtualMachineInstanceMigration` status.

### DataVolumes and import sources

A DataVolume (DV) orchestrates getting disk images into PVCs. It supports several import sources:

- *PVC clone* — clone an existing PVC (most common; used with golden images)
- *HTTP/HTTPS URL* — download an image from an external URL
- *Registry* — pull a container disk image from a container registry
- *Upload* — upload a local disk image via `virtctl image-upload`
- *Blank* — create an empty disk (used for data disks)

### Hot-plugging disks

Red Hat OpenShift Virtualization supports attaching and detaching PVC-backed disks to a running VM without rebooting. This is useful for attaching scratch space, shared data volumes, or importing data.

```bash
# Create a 10 GiB PVC for the data disk
cat > data-disk.yaml << 'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <pvc-name>
  namespace: <namespace>
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 10Gi
  storageClassName: ocs-storagecluster-ceph-rbd-virtualization
EOF
oc apply -f data-disk.yaml

# Wait for the PVC to be Bound
oc get pvc <pvc-name> -n <namespace> -w

# Hot-plug the PVC to the running VM
virtctl addvolume <vm-name> \
  --volume-name=<volume-name> \
  --claim-name=<pvc-name> \
  --persist \
  -n <namespace>

# Verify the disk appears inside the guest
virtctl ssh cloud-user@<vm-name> -n <namespace> -- lsblk

# Remove the disk without rebooting
virtctl removevolume <vm-name> \
  --volume-name=<volume-name> \
  -n <namespace>
```

## Exercise 2: Power Operations and Console Access

1. Confirm the VM is running

   ```bash
   oc get vm,vmi -n vmlab-student
   ```

Expected output:

```bash
NAME                                         AGE     STATUS    READY
virtualmachine.kubevirt.io/rhel9-webserver   <age>   Running   True

NAME                                                 AGE     PHASE     IP             NODENAME                                   READY
virtualmachineinstance.kubevirt.io/rhel9-webserver   <age>   Running   10.<x>.<y>.<z> ip-<nodename>.us-east-2.compute.internal   True
```

1. Pause the VM

   ```bash
   virtctl pause vm rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VMI rhel9-webserver was scheduled to pause
```

1.  Verify the status of the VM

   ```bash
   oc get vmi rhel9-webserver -n vmlab-student -o wide
   ```

Expected output:

```bash
NAME              AGE     PHASE     IP             NODENAME                                   READY   LIVE-MIGRATABLE   PAUSED
rhel9-webserver   <age>   Running   10.<x>.<y>.<z> ip-<nodename>.us-east-2.compute.internal   False   True              True
```

WARNING: Pay attention to the `READY` and `PAUSED` columns for the VMI

1. Unpause the VM

   ```bash
   virtctl unpause vm rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VMI rhel9-webserver was scheduled to unpause
```

1. Check the status of the VMI

   ```bash
   oc get vmi rhel9-webserver -n vmlab-student -o wide
   ```

Expected output:

```bash
NAME              AGE     PHASE     IP             NODENAME                                   READY   LIVE-MIGRATABLE   PAUSED
rhel9-webserver   <age>   Running   10.<x>.<y>.<z> ip-<nodename>.us-east-2.compute.internal   True    True
```

WARNING: Pay attention to the `READY` and `PAUSED` columns for the VMI

1. Perform a graceful restart of the VM

   ```bash
   virtctl restart rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VM rhel9-webserver was scheduled to restart
```

1. Watch the VMI object recreate (old one deleted, new one appears). Hit `Ctrl-C` once you see the new VMI phase as `Running`.

   ```bash
   oc get vmi -n vmlab-student -w
   ```

Expected output:

```bash
NAME              AGE   PHASE        IP    NODENAME   READY
rhel9-webserver   <age> Scheduling                    False
rhel9-webserver   <age> Running   10.<x>.<y>.<z> ip-<nodename>.us-east-2.compute.internal   True
```

1. Access the VM (use `cloud-user` and `redhat123` as the credentials)

   ```bash
   virtctl console rhel9-webserver
   ```

Expected output:

```bash
Register this system with Red Hat Insights: rhc connect

Example:
# rhc connect --activation-key <key> --organization <org>

The rhc client and Red Hat Insights will enable analytics and additional
management capabilities on your system.
View your connected systems at https://console.redhat.com/insights

You can learn more about how to register your system 
using rhc at https://red.ht/registration
Last login: Tue Mar 24 21:46:59 2026
```

NOTE: When done exit your ssh session using `exit` or `CTRL+d`, then `Ctrl-5` to disconnect.

### Verify

Confirm the VMI Custom Resource is linked to the VM state

```bash
oc get vmi -n vmlab-student
virtctl stop --force --grace-period=0 rhel9-webserver -n vmlab-student
oc get vmi -n vmlab-student -w
```
 
Expected output:
 
```bash
NAME              AGE   PHASE     IP             NODENAME                                   READY
rhel9-webserver   32m   Running   10.131.0.214   ip-10-0-7-182.us-east-2.compute.internal   True
VM rhel9-webserver was scheduled to stop
NAME              AGE   PHASE     IP             NODENAME                                   READY
rhel9-webserver   32m   Running   10.131.0.214   ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   32m   Succeeded                  ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   32m   Succeeded                  ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   32m   Succeeded                  ip-10-0-7-182.us-east-2.compute.internal   False
```

Confirm status of `virt-launcher` pod
 
```bash
oc get pod -n vmlab-student | grep virt-launcher
```
 
Expected output:
 
```bash
No resources found in vmlab-student namespace.
```

Confirm what happens when the VM restarts
 
```bash
virtctl start rhel9-webserver -n vmlab-student
oc get vmi -n vmlab-student -w
```
 
Expected output:
 
```bash
VM rhel9-webserver was scheduled to start
NAME              AGE   PHASE        IP    NODENAME   READY
rhel9-webserver   0s    Scheduling                    False
rhel9-webserver   12s   Scheduled          ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   13s   Scheduled          ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   13s   Running      10.131.0.216   ip-10-0-7-182.us-east-2.compute.internal   False
rhel9-webserver   13s   Running      10.131.0.216   ip-10-0-7-182.us-east-2.compute.internal   True
rhel9-webserver   13s   Running      10.131.0.216   ip-10-0-7-182.us-east-2.compute.internal   True
```

Expected output should show the following

- The status of the `virt-launcher` when VM is stopped
- A new VMI object is created upon a restart

## Snapshots

### VM snapshots

A `VirtualMachineSnapshot` captures the state of a VM's disks at a point in time. Snapshots are useful for creating restore points before risky changes such as OS upgrades, configuration changes, or application updates.

Red Hat OpenShift Virtualization snapshots leverage the CSI (Container Storage Interface) VolumeSnapshot API and require a CSI driver that supports snapshots (such as OpenShift Data Foundation / Ceph RBD).

```bash
# Stop the VM for a consistent snapshot (preferred)
virtctl stop <vm-name> -n <namespace>

cat << 'EOF' | oc apply -f -
apiVersion: snapshot.kubevirt.io/v1beta1
kind: VirtualMachineSnapshot
metadata:
  name: <snapshot-name>
  namespace: <namespace>
spec:
  source:
    apiGroup: kubevirt.io
    kind: VirtualMachine
    name: <vm-name>
EOF

# Monitor snapshot creation
oc get vmsnapshot -n <namespace> -w

# Verify snapshot is Ready
oc get vmsnapshot <snapshot-name> -n <namespace> \
  -o jsonpath='{.status.readyToUse}'
```

### Restoring from a Snapshot

A `VirtualMachineRestore` reverts a VM to the state captured in a snapshot. The VM must be stopped before initiating a restore.

```bash
# Restore the VM to the snapshot (VM must be stopped)
cat << 'EOF' | oc apply -f -
apiVersion: snapshot.kubevirt.io/v1beta1
kind: VirtualMachineRestore
metadata:
  name: <restore-name>
  namespace: <namespace>
spec:
  target:
    apiGroup: kubevirt.io
    kind: VirtualMachine
    name: <vm-name>
  virtualMachineSnapshotName: <snapshot-name>
EOF

# Watch restore progress
oc get vmrestore -n <namespace> -w

# Start the VM after restore completes
virtctl start <vm-name> -n <namespace>
```

## Exercise 3: Snapshot, Corrupt Data, and Restore

1. Stop the virtual machine

   ```bash
   virtctl stop rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VM rhel9-webserver was scheduled to stop
```

1. Snapshot the virtual machine

   ```bash
   cat << 'EOF' | oc apply -f -
   apiVersion: snapshot.kubevirt.io/v1beta1
   kind: VirtualMachineSnapshot
   metadata:
     name: rhel9-webserver-pre-change
     namespace: vmlab-student
   spec:
     source:
       apiGroup: kubevirt.io
       kind: VirtualMachine
       name: rhel9-webserver
   EOF
   ```

Expected output:

```bash
virtualmachinesnapshot.snapshot.kubevirt.io/rhel9-webserver-pre-change created
```

1. Verify the snapshot exists and succeeded

   ```bash
   oc get vmsnapshot -n vmlab-student -w
   ```

Expected output:

```bash
NAME                         SOURCEKIND       SOURCENAME        PHASE       READYTOUSE   CREATIONTIME   ERROR
rhel9-webserver-pre-change   VirtualMachine   rhel9-webserver   Succeeded   true         5s
```

TIP: Verify the snapshot `PHASE=Succeeded` and `READYTOUSE=true`.

1. Restart the virtual machine

   ```bash
   virtctl start rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VM rhel9-webserver was scheduled to start
```

1. Connect back to your VM (`cloud-user`, `redhat123`, `Ctrl-5` to disconnect)

   ```bash
   virtctl console rhel9-webserver
   ```

1. Simulate failure

   ```bash
   sudo systemctl stop httpd
   sudo dnf remove -y httpd
   ```

1. Verify Webserver stopped inside the VM

   ```bash
   curl http://localhost
   ```

   ```bash
   **Expected Output**
   curl: (7) Failed to connect to localhost port 80: Connection refused
   ```

NOTE: Disconnect from the virtual machine using `exit` followed by `CTRL+5`

1. Stop the virtual machine

   ```bash
   virtctl stop rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VM rhel9-webserver was scheduled to stop
```

1. Restore the virtual machine

   ```bash
   cat << 'EOF' | oc apply -f -
   apiVersion: snapshot.kubevirt.io/v1beta1
   kind: VirtualMachineRestore
   metadata:
     name: rhel9-webserver-restore-pre
     namespace: vmlab-student
   spec:
     target:
       apiGroup: kubevirt.io
       kind: VirtualMachine
       name: rhel9-webserver
     virtualMachineSnapshotName: rhel9-webserver-pre-change
   EOF
   ```

Expected output:

```bash
virtualmachinerestore.snapshot.kubevirt.io/rhel9-webserver-restore-pre created
```

1. Verify the status of the restore

   ```bash
   oc get vmrestore rhel9-webserver-restore-pre -n vmlab-student -w
   ```

Expected output:

```bash
NAME                          TARGETKIND       TARGETNAME        COMPLETE   RESTORETIME
rhel9-webserver-restore-pre   VirtualMachine   rhel9-webserver   true       10s
```

NOTE: Verify the status of the restore shows `COMPLETE=true`

1. Restart the virtual machine when restore is complete

   ```bash
   virtctl start rhel9-webserver -n vmlab-student
   ```

Expected output:

```bash
VM rhel9-webserver was scheduled to start
```

### Verify

Now that the restore has completed it is important to verify the restore was successful and the webserver is operational.

Verify the webserver is opertational again
 
```bash
virtctl ssh -i ~/.ssh/id_rsa cloud-user@vm/rhel9-webserver -n vmlab-student \
  -c 'curl http://localhost' 2>/dev/null
```

Expected output:

```bash
This is the WEB server before failure.
```

Expected output should show the following

- The webserver is operational

## VM decommissioning and cleanup

### Planned decommissioning

Decommissioning a VM is a multi-step process. Rushing it can result in data loss or orphaned storage objects. Follow this procedure for a safe, clean decommission:

1. Back up any data that needs to be retained (application data, snapshots, exports).
1. Notify users or dependent services of the pending shutdown.
1. Stop the VM gracefully using `virtctl stop`.
1. Delete any snapshots associated with the VM (optional — frees storage).
1. Delete the VM object — this cascades to delete associated DataVolumes and PVCs created via `dataVolumeTemplates`.
1. Verify all associated objects are removed.

### Deletion commands

```bash
# Step 1: Graceful stop
virtctl stop <vm-name> -n <namespace>

# Step 2: Delete snapshots (if any)
oc delete vmsnapshot -n <namespace> --all

# Step 3: Delete the VM (cascades to DVs and PVCs from dataVolumeTemplates)
oc delete vm <vm-name> -n <namespace>

# Step 4: Verify cleanup
oc get vm,vmi,dv,pvc,vmsnapshot -n <namespace>

# Note: Manually created PVCs (not in dataVolumeTemplates) are NOT
# automatically deleted. Remove them explicitly if no longer needed.
oc delete pvc <volume-name> -n <namespace>
```

### Protecting against accidental deletion

To prevent accidental deletion of production VMs, use Kubernetes finalizers or resource annotations. Red Hat OpenShift Virtualization also supports a deletion protection annotation:

```bash
# Add deletion protection annotation
oc annotate vm <vm-name> -n <namespace> \
  kubevirt.io/vm-deletion-protection=true

# The VM cannot be deleted until the annotation is removed
oc delete vm <vm-name> -n <namespace>
# Error: admission webhook denied the request

# Remove protection before decommissioning
oc annotate vm <vm-name> -n <namespace> \
  kubevirt.io/vm-deletion-protection-
```

## VM lifecycle issues

### VM stuck in scheduling state

If a VM stays in `Scheduling`/`Pending` for more than a few minutes, investigate using the following approach:

```bash
# Check VMI events for scheduling errors
oc describe vmi <vm-name> -n <namespace> | grep -A20 Events

# Check the virt-launcher pod (may reveal image pull or resource errors)
oc get pods -n <namespace> -l kubevirt.io/vm=<vm-name>
oc describe pod <virt-launcher-pod> -n <namespace>

# Check node capacity
oc describe nodes | grep -A10 'Allocated resources'

# Check if DataVolume import is still in progress
oc get dv -n <namespace>
oc describe dv <root-disk-name> -n <namespace> | grep -A10 Conditions
```

## Learning outcomes

By completing this module, you should now understand:

- How to create virtual machines
- How to alter the state of virtual machines
- How to connect to virtual machines
- How to snapshot virtual machines as a user
- How to restore virtual machines as a user

## Module summary

You have successfully explored the OpenShift Virtualization lifecycle management.

**What you accomplished:**

- Navigate and identify Red Hat OpenShift Virtualization CRs
- Interact with the state of a virtual machine
- Connect to your virtual machine
- Backed up and restored a virtual machine using snapshots

**Key takeaways:**

- You are now familiar with `VM`, `VMI` and `DV` Custom Resources
- You understand virtual machine states
- You can start, stop, pause virtual machine
- You can connect into virtual machines with different methods
- You are familiar with `virtctl`
- You can snapshot and restore virtual machines

**Next steps:**

Module 3 will cover VM live migration.
