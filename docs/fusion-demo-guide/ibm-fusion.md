---
layout: default
title: "IBM Fusion"
permalink: /fusion-demo-guide/ibm-fusion/
nav_order: 7
parent: "IBM Fusion Demo Guide"
---

# IBM Fusion

The following section provides the steps required to install the IBM Fusion operator and connect to the IBM Fusion console.
## Install the IBM Fusion Operator
Although a Red Hat OpenShift environment has been provisioned on IBM Technology Zone, IBM Fusion has not yet been installed. Therefore, the first step is to install the IBM Fusion Operator. (The IBM Catalog and the entitlement key have already been added.) This section of the lab walks you through the process of installing IBM Fusion operator.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-the-ibm-fusion-operator-01.png)

1. In the OpenShift GUI, navigate to the Ecosystem screen by clicking on the Ecosystem menu item shown in the left-hand side navigation pane and selecting the Software Catalog sub-item. Next, type the word Fusion in the Search text entry field located below the All Items heading. Click on the IBM Storage Fusion operator tile when it appears.
1. Keep all the default settings and click on the Install button.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-the-ibm-fusion-operator-02.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-the-ibm-fusion-operator-03.png)

1. When the Install Operator screen appears, keep all the default settings shown and scroll down until the Install  button appears. Then, click on the button.
1. This should cause an “Installing Operator” message to appear.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-the-ibm-fusion-operator-04.png)


![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/install-the-ibm-fusion-operator-05.png)

1. When the screen shows a “create SpectrumFusion” button, it is ready for installation.
## Connect to Fusion
IBM Fusion is fully containerized and designed to be an application in Red Hat OpenShift. Thus, the IBM Fusion GUI can be launched from the OpenShift console.
1. From the OpenShift Console (top right), click the Application menu (A) icon (the icon that looks like 9 squares) and then click IBM Storage Fusion (B). A new tab will be opened for the IBM Fusion GUI. If prompted, enter kubeadmin and your kubeadmin password from the reservation.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-fusion-01.png)

1. If the Red Hat OpenShift Container Platform logon screen appears, select kube:admin to bring up the login screen. Enter the kubeadmin credentials to continue to the IBM Fusion user interface. Othere, accept the license agreement by selecting, I have read and accept the license agreement (A) check box.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-fusion-02.png)

1. Click the Continue (A) button. This should redirect you to the Welcome to IBM Fusion page.
> The spectrumfusion SpectrumFusion custom resource is created after accepting the License Agreement.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-fusion-03.png)

1. Click on the View services (A) button or Services (B) menu item to go directly to the Services page.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/connect-to-fusion-04.png)

### Managing IBM Fusion
The following section discusses additional options available within the IBM Fusion GUI and their functions.
#### Events
IBM Fusion events are Kubernetes native events that include filter-specific labels.
1. In the Fusion GUI, navigate to the Events page by clicking on the Events (A) menu item shown in the left-hand side navigation pane.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/events-01.png)

1. You will then be presented with an event log for IBM Fusion.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/events-02.png)

1. It is possible to filter the results in the events log by clicking the Severity: Filter (A) or Filter…(B) column header and choosing the desired category from the drop-down menus provided. To simplify searching for the desired information, this page also has a Search toolbar (C) that can be used.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/events-03.png)

1. Finally, since all the information displayed is not necessarily useful to everyone, it is possible to modify the columns that are displayed by clicking the “gear” icon (C) located in the top-right-hand corner of the events table.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/events-04.png)

#### Call home
The current Call Home configuration setting can be obtained by clicking on the Settings menu item shown in the left-hand side navigation pane of the IBM Fusion GUI.
> NOTE: This is just for your information; Call Home will not be configured in the IBM Technology Zone environment.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/call-home-01.png)

If you click the Enable button shown under the Call Home configuration, you will be asked to provide contact information for the individual in your organization who is responsible for managing Fusion storage.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/call-home-02.png)

#### Services page
The services page of the IBM Fusion GUI shows the services that have been enabled and configured. If the desired service(s) were not enabled during the installation of the operator, they can be enabled here.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/services-page-01.png)

#### IBM Fusion Help
The following help operations can be selected after clicking on the question mark icon located in the IBM Fusion GUI masthead:
- Open a support case – create a support ticket with IBM.
- Support logs – download support log data.
- IBM documentation – view IBM documentation for IBM Fusion.
- About – display the version of IBM Fusion currently being used.

![Screenshot]({{ site.baseurl }}/assets/images/fusion-demo-guide/ibm-fusion-help-01.png)
