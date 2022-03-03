Operations
===============

Katonic application logging 
------------------------

There are two types of logs produced by the operation of Katonic. 

 1. Katonic execution logs 

 2. Katonic application logs 

**Execution logs (Pending implimentation)** 

These are the logs output by user code running in Katonic as a Job, Workspace, App, or Model API. These are available in the Katonic web application on the Jobs Dashboard, Workspaces Dashboard, App Dashboard, and Model API instance logs. This data is a key part of the Domino reproducibility model, and is kept indefinitely in the Domino blob store. 

The system these logs are written to is defined in the installation configuration file at ``blob_storage.logs``. 

 
**Application logs** 

All Katonic services output their logs using the `standard Kubernetes logging architecture <https://kubernetes.io/docs/concepts/cluster-administration/logging/>`_. Relevant logs are printed to ``stdout`` or ``stderr`` as indicated, and are captured by Kubernetes. 

.. _standard Kubernetes logging architecture: <https://kubernetes.io/docs/concepts/cluster-administration/logging/>


For example, to look at your front end logs you could do the following: 

 3. List your all namespaces to find the name of you platform namespace 

``kubectl get namespace`` 

 4. List all the pods in your platform namespace to find the name of a front end. Keep in mind you likely have more than one front end pod. 

``kubectl get pods  -n <namespace for you platform nodes>``

 5. Print the front ends logs for one of your front ends 

``kubectl logs <pod name of your front end pod> -n <namespace for you platform nodes> -c nucleus-frontend`` 

The most effective way to aggregate logs is to attach a Kubernetes log aggregation utility to monitor the following `Kubernetes namespaces <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ used by Katonic: 

.. _Kubernetes namespaces: <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>

 * Platform namespace 

This namespace hosts the core application components of the Katonic application, including API servers, databases, and web interfaces. The name of this namespace is defined in the installer configuration file at ``namespaces.platform.name``. 

The following components running in this namespace produce the most important logs: 

.. list-table:: Title
   :widths: 25 25 50
   :header-rows: 1

   * - Component
     - Logs

   * - nucleus-frontend
     - The nucleus-frontend pods host the frontend API server that routes all requests to the Katonic application. Its logs will contain details on HTTP requests to Katonic from the application or another API client. If you see errors in Katonic with HTTP error codes like 500, 504, or 401, you can find corresponding logs here. 
   * - nucleus-dispatcher
     - The nucleus-dispatcher pod hosts the Katonic scheduling and brokering service that sends user execution pods to Kubernetes for deployment. Errors in communication between Katonic and Kubernetes will result in corresponding logs from this service. 
   * - keycloak 
     - The keycloak pods hosts the Katonic authentication service. The logs for this service will contain a record of authentication events, including additional details on any errors. 
   * - cluster-autoscaler
     - This pod hosts the open-source Kubernetes cluster autoscaler, which controls and manages autoscaling resources. The logs for this service will contain records of scaling events, both scaling up new nodes in response to demand and scaling down idle resources, including additional details on any errors.  
   
**Compute grid namespace** 

This namespace hosts user executions plus Katonic environment builds. The name of this namespace is defined in the installer configuration file at ``namespaces.compute.name``. 

Logs that appear in this namespace will correspond to ephemeral pods hosting using work. Each pod will contain a user-defined environment container, whose logs are described above as **Execution logs**. There are additional supporting containers in those pods, and their logs may contain additional information on any errors or behavior seen with specific Katonic executions. 

Users are advised to aggregate and keep at least 30 days of logs to facilitate debugging. These logs can be harvested with a variety of Kubernetes log aggregation utilities, including: 

 * `Loggly <https://www.loggly.com/solution/kubernetes-logging/>`_

 .. _Loggly: <https://www.loggly.com/solution/kubernetes-logging/> 

 * `Splunk <https://docs.splunk.com/Documentation/InfraApp/2.0.2/Admin/AddDataKubernetes>`_

 .. _Splunk: <https://docs.splunk.com/Documentation/InfraApp/2.0.2/Admin/AddDataKubernetes>

 * `NewRelic <https://docs.newrelic.com/docs/logs/enable-logs/enable-logs/kubernetes-plugin-logs>`_

 .. _NewRelic: <https://docs.newrelic.com/docs/logs/enable-logs/enable-logs/kubernetes-plugin-logs>

 
**Audit logging (Pending implimentation)** 

Katonic System Administrators can enable audit logging for a number of events. Audit logging for models has been improved in the 4.6.1 release. These are the major model events that are logged when triggered through the Katonic UI: 

 * New model create 

 * New model version publish 

 * Model version stop / start 

 * Model archived 

 * Model collaborator add / change / remove 

 * Model settings change 

Audit log messages are written using the Katonic event tracker system, which writes logs to the following destinations, depending on configuration: 

 * Application logs `(see above) <https://admin.dominodatalab.com/en/5.0.1/operations/logging.html#application-logs>`_

 .. _(see above): <https://admin.dominodatalab.com/en/5.0.1/operations/logging.html#application-logs>  

 * Syslog server 

 * Mixpanel 

After you enable audit logging, messages are written to Application logs. Other log targets require additional configuration. 

Contact `support@katonic.ai <mailto:support@katonic.ai>`_ for assistance enabling, accessing, and processing audit logs. 
Monitoring

.. _support@katonic.ai: <mailto:support@katonic.ai>  
----------------------

You must create a account from Sign up page https://katonic.ai/signup.html

Sizing infrastructure for Domino
-------------------------------------

Chat in the `#chat-with-Katonic`chat bot. Katonic bot will respond to anyone in this site.
