---
layout: default
title: "Reserve or Provision Environment"
permalink: /fusion-demo-guide/reserve-or-provision/
nav_order: 3
parent: "IBM Fusion Demo Guide"
---

# Reserve or provision your environment

## Reserve an environment in IBM Technology Zone
This lab requires the use of an environment that is provisioned through IBM Technology Zone.
> Tip: If you are using the lab to demo IBM Fusion to a client, ensure that you reserve enough time to set up the environment, as some environments require a significant amount of set up time. As well, reserve the IBM Technology Zone environment far enough in advance so that you can choose the best time to use to demo the lab to with your client.
1. Open a web browser and go to the IBM Technology Zone – IBM Fusion Collection. ([https://techzone.ibm.com/collection/ibm-spectrum-fusion](https://techzone.ibm.com/collection/ibm-spectrum-fusion))
1. The product overview page is displayed.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-01.png)

1. From the product overview page, locate Environments (A) in the menu shown on the left-hand side of the screen and click on it.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-02.png)

1. Scroll down until the Reserve (A) button located at the bottom of the Beta: Storage Fusion on OCP w/ODF and Scale tile and click on it.
> Important: The Beta:IBM Fusion on OpenShift Virtualization is the new pattern for the labs and is used in this guide. Many options are automatically configured, and this simplifies the user experience of deploying a Fusion Technology Zone environment.

NOTE: This is a new pattern, and the some of the steps in the docs may be out of date.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-03.png)

1. start the Create a request diaglog:

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-04.png)

1. When the options for reserving your environment are displayed, Enter a Name in the text field and then add a brief description.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-05.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-06.png)

1. (A) Enter a description for what you are doing in the Purpose description text entry field. For example, Using the environment for course work.
> Note: Ensure that you enter or select values for the required fields in the form. The required fields are highlighted in red and show an exclamation mark.
> Refer to the appropriate runbook for more information about selecting the correct environment.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-07.png)

1. Select the Preferred Geography: itzvmware-spectrum – AMERICAS – us-east-region – wdc04 datacenter (A).

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-08.png)

1. Scheduling, set your time period

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-09.png)

1. Customize the configuration

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-10.png)

1. There are four important options when you reserve your environment:
   1. OpenShift Version – 4.21 is preferred. Choose either 4.19, 4.20, or 4.21.
   1. Worker Node Count – 3 is preferred. Choose the number of worker nodes required. 3 is enough for this lab.
   1. Worker Node Flavor – 16 vCPU x 64 GB – 300 GB ephemeral storage is preferred.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-11.png)

Make sure you save.
1. After you have completed the form, select I agree to IBM Technology Zone’s Terms and Conditions and End User Security Policies (A) checkbox, and then click the Submit (B) button.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-12.png)

Once you submit your reservation request, you will receive a confirmation email from IBM Technology Zone, but the environment will not be ready at this time.
You will receive additional emails that tell you when your environment is being provisioned and when it is ready.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-13.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/reserve-an-environment-in-ibm-technology-zone-14.png)

You can select “track my request” and see the progress
Follow the steps outlined in the email from IBM Technology Zone telling you the environment is ready to connect to and begin using the environment.
> Note: If you have any difficulties provisioning your environment, visit the IBM Technology Zone Help web page (https://techzone.ibm.com/help). It is recommended to attempt to provision the environment again if it fails the first few times before opening a ticket with IBM Technology Zone. If you have an issue with the site, you can open a support case (https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US). Alternatively, you can send an email to techzone.help@ibm.com. This contact information is also provided in the emails that you receive from IBM Technology Zone.
## Connect to the lab environment
To access the IBM Fusion infrastructure provided in your environment, you will need to refer to the IBM Technology Zone “Reservation Ready” email, which will contain links to the login credentials needed.
> Note: Connectivity to the Red Hat OpenShift console may be lost during the first 30 minutes after receiving the Technology Zone “Reservation Ready” email. The machineConfigPool is still updating and rebooting the worker nodes during this time causing the loss of connection to the console during this period.
> NOTE: You can also see this information under “My Request” when you are logged into IBM Technology Zone (https://techzone.ibm.com/my/requests).

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-01.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-02.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-03.png)

Open The reservation

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-04.png)

Toggle the down arrow next to the name to see the details
Notes:
To access the Bastion via ssh:
Copy the ssh command, but you will need to download the SSH private key, save it, change the mode to 600 (chmod 600 keyfile) on mac or linux and then use it in the command line
```bash
ssh itzuser@api.itz-xxxxxx.sysd05.techzone.ibm.com -p 10022 -i keyfile
```

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-05.png)

You can open the VM remote Console to see the console to all of the nodes and get log in credentials:

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-the-lab-environment-06.png)
