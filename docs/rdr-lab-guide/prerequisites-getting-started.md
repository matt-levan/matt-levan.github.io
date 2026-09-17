---
layout: default
title: "Prerequisites & Getting Started"
permalink: /rdr-lab-guide/prerequisites-getting-started/
nav_order: 2
parent: "IBM Fusion RDR Lab Guide"
---

# Prerequisites & Getting Started

You will need an IBM account and corresponding IBMid to gain access to IBM Technology Zone.

{% include shared/redhat-prerequisites.md %}

When instructions are given to enter text, the text is usually shown in mono space font (this is an example). This is to help indicate that you need to type or copy/paste all the text as is.
IBM employees can use their IBM credentials to access IBM Technology Zone or IBM Cloud.
Business Partners must use an IBMid for IBM Technology Zone. If you do not have an IBMid, you can create one by using steps in this document. There is no cost to creating an IBMid.
You might also require an IBM Cloud account for some lab environments.
Additionally, you might need to configure an OpenVPN connection to be able to access the lab environment.
## Creating an IBMid
1. In your web browser, go to the IBM account page (https://www.ibm.com/account/us-en/).
1. Click **Log in to **My IBM**** (A).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-01.png)

1. The Log in to IBM page is displayed. Click **Create an **IBMid**** (A).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-02.png)

1. On the **Create an IBMid** page, enter the following information:
**- Your email address** (A)
- A **password for your IBMid account** (B)
**- First name** (C)
**- Last name** (D)
- Your country or region of **residence** (E) and state or **province** (F)
- If you select that **you are not a student** (G), then enter the name of **your company** (G)
- Click **Next** (I) to continue

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-03.png)

1. You are then prompted to verify your email and complete your account creation. Enter the code that was emailed to you in **Verification **token**** (A), and then click **Create **account**** (B).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-04.png)

1. The **About your IBMid Account** page is shown. Click **Proceed** (A).

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/creating-an-ibmid-05.png)

1. After a few minutes, you will receive an email confirming that your IBMid has been activated.
   > Note: The first time that you log in using your IBMid you will be sent another code to verify your log in.

To access the IBM Fusion infrastructure provided in your environment, you will need to refer to the IBM Technology Zone “Reservation Ready” email, which will contain links to the login credentials needed.
> Note: Connectivity to the Red Hat OpenShift console may be lost during the first 30 minutes after receiving the Technology Zone “Reservation Ready” email. The machineConfigPool is still updating and rebooting the worker nodes during this time causing the loss of connection to the console during this period.

The IBM Technology Zone “Reservation Ready” email should look like the one shown here.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-01.png)

> NOTE: You can also see this information under “My Reservations” when you are logged into IBM Technology Zone (https://techzone.ibm.com/my/reservations).

The desktop URL provided is used for direct access to the OpenShift Console.

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-02.png)

| Field | Value |
| --- | --- |
| Desktop url | `https://console-openshift-console.apps.ocp-xxxxxxxxx-xxxx.cloud.techzone.ibm.com` |
| Username | `kubeadmin` |
| Password | provided in your reservation |

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/connect-to-the-lab-environment-03.png)

This gives you direct access to the OpenShift Console via your browser.
## Addressing plan and credentials
Access to the lab environment is provided through your desktop web browser. The access information needed is provided in the Technology Zone Reservations page.
1. Navigate to your “Reservations” page on IBM Technology Zone using either the “View My Reservations” button on your IBM Technology Zone email notification or log into IBM Technology Zone and use the “My reservations” link. Select your reservation by clicking on the corresponding tile. A screen like the one shown below should be displayed.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/addressing-plan-and-credentials-01.png)

1. Note the username and password credentials (the information highlighted in the red rectangle in the previous screen shot).

The table below is a summary of the reservation detail information you will use. This information is listed on the environment reservation page.

|  | IP Address | User | Password |
| --- | --- | --- | --- |
| Cluster URL | https://console-openshift-console.apps.fusion.Storage.lan | kubeadmin | Provided by IBM Technology Zone |
| IBM Storage Scale | 192.168.252.5 | root | Passw0rd! |
| IBM Storage Scale GUI | https://192.168.252.5 | admin | Passw0rd! |
| IBM Storage Scale GUI |  | csi-storage-gui-user | csi-storage-gui-password |
| IBM Ceph | 192.168.252.7 | admin | Passw0rd! |
| IBM Ceph GUI | https://192.168.252.7:8443 | admin | ceph |

## OpenShift Web Console
1. To access the OpenShift console, click on the **blue Desktop button** (A) or click on the the **Desktop url link** (B). The login credentials **needed are the Username “kubeadmin”** (C) and the **Password** (D) provided. (The actual connection information will be specific to your cluster.)

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-01.png)

1. When your browser connects to the OpenShift Container Platform web user interface (UI), select kube:admin (A) to bring up the login screen. (The IBMid option will use your IBM account to login and is not the recommended method to use for authentication to the environment.)

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-02.png)

1. Enter **Username** (A) and **Password** (B) as found in your TechZone reservation.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-03.png)

1. Once you have logged in, you will be presented with the OpenShift home page.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-web-console-04.png)

## OpenShift Command Line Access
1. To get command line access, **find the Bastion SSH Connection** (A) information on your IBM Technology Zone reservation details page. The **Bastion Password** (B) is used to access the remote shell environment. Here is an image of what you will see – the connection data will be specific to your cluster. The **API URL** (C) will be used in a later step to connect to the OpenShift cluster with the ‘oc’ command.

   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-01.png)

1. To connect via SSH, open a terminal on a Mac or Linux system and enter a command that looks something like this:
   ```bash
   ssh itzuser@apps.ocp-50t6fjgae-droi.cloud.techzone.ibm.com -p 40222
   ```

(Use the Bastion Password. Also the hostname is an example; get the real host name from your reservation.)
> Note: On Windows you can use PowerShell or an SSH utility like ‘putty’.

1. Once you are in the bastion host, connect to the cluster with the API URL and the kubeadmin user and kubeadmin password by executing a command that looks like this:
   ```bash
   oc login -u kubeadmin [API_URL]
   ```

where API_URL is the API URL value obtained from your reservation page of your environment details. For example:
```bash
oc login -u kubeadmin https://api.ocp-50t6fjkgae-droi.cloud.techzone.ibm.com:6443
```

(When prompted, enter the kubeadmin “Cluster Admin Password”)

![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-02.png)

1. Now, that you can access the cluster, run a couple of OpenShift commands from the ‘oc’ command line:
   ```bash
   oc get nodes
   oc get clusterversion
   ```


   ![Screenshot]({{ site.baseurl }}/assets/images/rdr-lab-guide/openshift-command-line-access-03.png)

Congratulations! You have just learned how to access the environment that was provisioned on IBM Technology Zone. This concludes the exercises in this lab guide.