---
layout: default
title: "Provide Persistent Storage"
permalink: /fusion-demo-guide/provide-persistent-storage/
nav_order: 8
parent: "IBM Fusion Demo Guide"
---

# Provide Persistent Storage

As of Fusion 2.13, Storage is installed via the Data Foundation service. The first step is to install Data Foundation via the Data Foundation Service tile.

> **Note:** If you are going to set up a remote mount of an external Storage Scale cluster, apply the MachineConfig Operator (MCO) required for IBM Storage Scale first. Log into the bastion server and connect to the cluster with the `oc` CLI, then run:

```bash
oc apply -f https://raw.githubusercontent.com/IBM/ibm-spectrum-scale-container-native/v6.0.0.x/generated/scale/mco/mco.yaml
```

After applying the MCO, wait for the machine ready count to complete:

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-01.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-02.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-03.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-04.png)

Install the Data Foundation service from the services menu on the fusion console



After selecting Data Foundation you will see:

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-05.png)

Select “Install”

and you will get an option for “internal” or “external”. Select “internal” if you only want to install Internal Data Foundation. Select “external” if you want to enable remote mount of Ceph, Scale and Fusion Access.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/provide-persistent-storage-06.png)

For this lab, we want to explore all of the features. Therefore, select “external”