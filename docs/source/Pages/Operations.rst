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

.. list-table:: Component & Logs
   :widths: 50 50
   :header-rows: 2

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

Katonic monitoring (Pending Implimentation) 
---------------------------------------------

Monitoring Katonic involves tracking several key application metrics. These metrics reveal the health of the application and can provide advance warning of any issues or failures of Katonic components. 

Metrics 

Katonic recommends tracking these metrics in priority order:

.. list-table:: Component & Logs
   :widths: 50 50 50
   :header-rows: 3

   * - Metric 
     - Suggested threshold 
     - Notes

   * - Latency to ``/health`` 
     - 1000ms
     - Measures the time to receive a response to a request to the Katonic API server. If the response time is too high, this suggests that the system is unhealthy and that user experience might be impacted. This can be measured by calls to the Katonic application at a path of ``/health``.  
   * - Dispatcher pod availability from `metrics server <https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server>`_
     - ``nucleus-dispatcher`` pods available = 0 for > 10 minutes 
     - If the number of pods in the ``nucleus-dispatcher`` deployment is 0 for greater than 10 minutes, its an indication of critical issues that Katonic will not automatically recover from, and functionality will be degraded.  
   * - Frontend pod availability from `metrics server <https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server>`_
     - ``nucleus-frontend`` pods available < 2 for > 10 minutes 
     - If the number of pods in the ``nucleus-frontend`` deployment is less than two for greater than 10 minutes, its an indication of critical issues that Katonic will not automatically recover from, and functionality will be degraded.

.. _metrics server: <https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server>

.. _metrics server: <https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server>

There are many application monitoring tools you can use to track these metrics, including: 

 * `NewRelic <https://newrelic.com/platform/kubernetes/monitoring-guide>`_

 .. _NewRelic: <https://newrelic.com/platform/kubernetes/monitoring-guide>

 * `Splunk <https://docs.splunk.com/Documentation/InfraApp/2.0.2/Admin/AddDataKubernetes>`_

 .. _Splunk: <https://docs.splunk.com/Documentation/InfraApp/2.0.2/Admin/AddDataKubernetes>

 * `Datadog <https://www.datadoghq.com/blog/how-to-collect-and-graph-kubernetes-metrics/>`_

 .. _Datadog: <https://www.datadoghq.com/blog/how-to-collect-and-graph-kubernetes-metrics/>

 **Alerting** (Pending ) 

Users are advised to configure alerts to their application administrators if the thresholds listed above are exceeded. These alerts are an indication of potential resourcing issues or unusual usage patterns worth investigation. Refer to the Katonic application logs, the Katonic administration UI, and the Katonic Control Center to gather additional information. 

Sizing infrastructure for Katonic 
-------------------------------------

Katonic runs in Kubernetes, which is an orchestration framework for delivering applications to a distributed computing cluster. The Domino application runs two types of workloads in Kubernetes, and there are different principles to sizing infrastructure for each: 

 * Katonic Platform 

These always-on components provide user interfaces, the Domino API server, orchestration, metadata and supporting services. The standard architecture runs the platform on a stable set of three nodes for high availability, and the capabilities of the platform are principally managed through vertical scaling, which means changing the CPU and memory resources available on those platform nodes and changing the resources requested by the platform components. 

 * Katonic Compute 

These on-demand components run users’ data science, engineering, and machine learning workflows. Compute workloads run on customizable collections of nodes organized into node pools. The number of these nodes can be variable and elastic, and the capabilities are principally managed through horizontal scaling, which means changing the number of nodes. However, when there are more resources present on compute nodes, they can handle additional workloads, and therefore there are benefits to vertical scaling. 

**Sizing the Katonic Platform** 

The resources available to the Katonic Platform will determine how much concurrent work the application can handle. This is the primary capability of Katonic that is limited by vertical scale. To increase the capacity, key components must have access to additional CPU and memory. 

The default size for the Katonic Platform is three nodes, with 8 CPU cores and 32GB memory each, for a total of 24 CPU cores and 96GB of memory. Those resources are available to the `collective of Platform services <https://admin.dominodatalab.com/en/latest/architecture.html#services>`_, and each service claims some resources via `Kubernetes resource requests <https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/>`_. 

.. _collective of Platform services: <https://admin.dominodatalab.com/en/latest/architecture.html#services>

.. _Kubernetes resource requests: <https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/>

The capabilities of that default size are shown below, along with options for alternative sizing. 

.. list-table:: Component & Logs
   :widths: 50 50 50
   :header-rows: 3

   * - Size 
     - Maximum concurrent executions
     - Platform specs

   * - Default  
     - 300 
     - 4 nodes with at least 4 CPU cores and 16 GiB memory each. AWS recommendation: 3x t2.`xlarge <https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/>`_ GCP recommendation: 3x `n1-standard-8 <https://cloud.google.com/compute/docs/machine-types>`_ Azure recommendation: 3x `Standard_DS5_v2 <https://docs.microsoft.com/en-us/azure/virtual-machines/dv2-dsv2-series?toc=/azure/virtual-machines/linux/toc.json&bc=/azure/virtual-machines/linux/breadcrumb/toc.json#dsv2-series>`_
   * - Other 
     - Contact your Katonic account team if you need an alternative size 
     - Varies 

.. _xlarge: <https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/>

.. _n1-standard-8: <https://cloud.google.com/compute/docs/machine-types>

.. _Standard_DS5_v2: <https://docs.microsoft.com/en-us/azure/virtual-machines/dv2-dsv2-series?toc=/azure/virtual-machines/linux/toc.json&bc=/azure/virtual-machines/linux/breadcrumb/toc.json#dsv2-series>

**Estimating concurrent executions** 

Katonic recommends assuming a baseline maximum number of workloads equal to 50% of the number of total Katonic users, expressed as a _concurrency_ of 50%. However, different teams and organizations may have different usage patterns in Katonic. For teams that regularly run batches of many executions at once, it may be necessary to size Katonic to support a concurrency of 100%, or even 200%. 

Optimizing your configuration for efficient use of Platform resources 

The following practices can maximize the capabilities of a Platform with a given size. 

* When a user launches a Katonic Run, part of the start-up process is loading the user’s environment onto the node that will host the Run. For large images, the process of transferring the image to a new node can take several minutes. Once an image has been loaded onto a node once, it gets cached, and future Runs that use the same environment will start up faster. 

* Optimize your hardware tiers and node sizes to fit many workloads in tidy groups. Each additional node runs message brokers, logging agents, and adds load to Platform services that process queues from the Compute Grid. The Platform can handle more concurrent executions by running more executions on fewer nodes. 

* Parallelize your tasks by running your workload on many cores of one large node, rather than by chunking tasks into multiple workloads across multiple nodes. This reduces the total number of nodes being managed, and thereby reduces load on the Katonic platform.

**Container resource management** 

Katonic uses `Kubernetes requests <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`_ and limits to manage the CPU and memory resources that Katonic pods use. These requests and limits can be scaled to adjust resource consumption and performance. Container workloads such as databases and search systems whose data integrity is affected by the enforcement of limits do not have limits added to their configuration and care should be taken not to add limits to them. 

.. _Kubernetes requests: <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
