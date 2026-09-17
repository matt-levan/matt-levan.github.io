---
layout: default
title: "IBM Fusion Demo Guide"
permalink: /fusion-demo-guide/
nav_order: 1
---

# Introduction

The core value of Fusion is derived from “Fusion 5”—five foundational application data services that deliver a consistent experience across public cloud and on-premises bare metal or virtualized platforms.
1. Data persistence: Platform engineering and application development teams gain productivity from Fusion's automation for data storage provisioning.
1. Data resilience: Ensures that data is always available, even during disruptive events or system failures.
1. Data security: Data encryption, retention and recovery to protect from intentional or unintentional data loss.
1. Data mobility: Applications need to run from the edge, to the core, and to the cloud, which requires your data to be mobile.
1. Data cataloging: Data scientists seek simple and fast ways to create actionable data insights at scale.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/introduction-02.png)

## About this demo
The purpose of this exercise is to enable you to get some hands-on experience with IBM Fusion on an OpenShift Cluster. The environment used is a VMware server provisioned on IBM Technology Zone and is suitable for self-education, demos, and a customer Proof of Experience (PoX). In this exercise you will:
- Learn how to install, configure, and use IBM Fusion and the Fusion graphical user interface (GUI)
- Explore scenarios that are written, tested, documented, and maintained by the IBM Worldwide (WW) Storage Technical Architect team.
- Learn how to install the IBM Fusion Operator on a pre-configured, ready to use Red Hat OpenShift Container Platform instance.
- Use the IBM Fusion Operator to create an IBM Fusion instance.
- Login to IBM Fusion
- Use the IBM Fusion GUI to connect to a remote Storage Scale file system (and in the process, see IBM Fusion automatically install containerized Storage Scale).
- Create and execute IBM Fusion backup and restore policies.
## Product disclaimer
This product is being developed and released in an agile manner. In addition to adding new capabilities, the interface is likely to change over time. Therefore, the screenshots used in this demo may not always look exactly like what you see in the product. Depending on the product, you can expect to encounter some of the following:
- Changes in the user interface (UI), such as the location of buttons or text in various fields
- Additional tabs or buttons
These differences should not affect how the demos work but have patience and explore.
## Getting help
If you require assistance in interpreting any of the steps in this lab, please post your questions to the #storage_demo_feedback ([https://ibm.enterprise.slack.com/archives/C06KQ49RJBF](https://ibm.enterprise.slack.com/archives/C06KQ49RJBF)) Slack channel (IBMers only). Business Partners can request help at the [Partner Plus Support](https://www.ibm.com/partnerplus/support) website.
For troubleshooting tips, see the TechZone Set Up Troubleshooting Guide ([https://ibm.seismic.com/Link/Content/DCGT3pQ7hHM828WDQ86R7Tf6gpPV](https://ibm.seismic.com/Link/Content/DCGT3pQ7hHM828WDQ86R7Tf6gpPV)) for help with common issues and solutions when using IBM Technology Zone. Additionally, go to the IBM Technology Zone Help page ([https://techzone.ibm.com/help](https://techzone.ibm.com/help)). If you have an issue with the site, you can open a support case ([https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US](https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US)). Alternatively, you can send an email to [techzone.help@ibm.com](mailto:techzone.help@ibm.com). This contact information is also provided in the emails you receive from IBM Technology Zone.
Help with the Fusion product itself is available in the #ibm-fusion-help ([https://ibm.enterprise.slack.com/archives/C029ET42U8Y](https://ibm.enterprise.slack.com/archives/C029ET42U8Y)) Slack channel (IBMers only).
Additionally, see the Fusion documentation ([https://www.ibm.com/docs/en/storage-fusion-software](https://www.ibm.com/docs/en/storage-fusion-software)).