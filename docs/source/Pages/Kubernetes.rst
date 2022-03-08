Kubernetes
===============

Cluster requirements
------------------------

**Kubernetes 1.20+** 

Starting with Kubernetes 1.21, Docker is deprecated as a container runtime. Some distributors of Kubernetes software and providers of managed Kubernetes services (such as AKS and EKS) may change their default runtime from Docker to containerd. If its On-premise and below to kubernetes version 1.21 then we will give option to choose between Docker and containerd. When upgrading a cluster using a managed Kubernetes service: 

 * Confirm that the version you’re upgrading supports Docker runtime. 

 * Configure the upgrade to use Docker runtime. 

Some default upgrade paths on AKS automatically switch you to containerd unless you specify and From EKS 1.22 they are changing their default runtime engine to containerd. 

 

**Cluster creation** 

We use AKS and EKS. If it's On-premise we install kubernetes using Kubespray. 

 

**Platform installation** 

Katonic platform installation is done by Katonic ansible role. 

 

**Namespaces** 

There are some dedicated namespaces used in our platform. 

 

**Storage requirements** 

Katonic uses 2 storage classes. 

1. Dynamic storage 

This storage needs to be backed by a storage class with the following properties: 

 * Supports dynamic provisioning 

 * Can be mounted on any node in the cluster 

 * SSD-backed recommended for fast I/O 

 * Capable of provisioning volumes of at least 100GB 

 * Underlying storage provider can support ``ReadWriteOnce`` semantics 

 

By default, this storage class is named kdisk. 

 

In AWS, EBS is used to back this storage class. As per requirement of user we can change the EBS type to io1, gp2, gp3, etc.
:: 


  apiVersion: storage.k8s.io/v1 

  kind: StorageClass 

    metadata: 

        name: katonic-compute-storage 

  provisioner: kubernetes.io/aws-ebs 

    parameters: 

        type: gp2 

        fsType: ext4

In azure, azure disk is used to back this storage class. We use azure disk storage class.  

 Azure disk storage class   
::


  apiVersion: storage.k8s.io/v1 

    kind: StorageClass 

      metadata: 

        name: slow 

    provisioner: kubernetes.io/azure-disk 

      parameters: 

        storageaccounttype: Standard_LRS 

        kind: managed   
  
2. Long term shared storage 

Katonic needs a separate storage class for long term storage for: 

 * Project data uploaded or created by users 

 * Katonic Datasets 

This storage needs to be backed by a storage class with the following properties: 

 * Dynamically provisions Kubernetes PersistentVolume 

 * Can be accessed in ReadWriteMany mode from all nodes in the cluster 

 * Uses a VolumeBindingMode of Immediate 

In AWS, these storage requirements are handled by two separate classes. One backed by EFS for Katonic Datasets, and one backed by S3 for project data, backups, and Docker images. Similarly for other cloud providers or on-premises cluster, we need an S3 bucket (Not necessarily aws s3 bucket) to store backups. 

By default, this storage class is named kfs(Katonic file system). 

**Native** 

For shared storage, we allow for (and even require) native cloud provider object store for a few resources and services: 

 * Blob Storage. For AWS, the blob storage must be backed by S3 (see `Blob storage <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#blob-storage>`_). For other infrastructure, the Kfs storage class is used. 

 * Logs. For AWS, the log storage must be backed by S3 (see `Blob storage <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#blob-storage>`_). For others, the kfs storage class is used. 

 * Backups. For all supported cloud providers, storage for backups is backed by the native blob store. For on-prem, backups are backed by the kfs storage class. 

    * AWS: `S3 <https://aws.amazon.com/s3/>`_

    * Azure: `Azure Blob Storage <https://azure.microsoft.com/en-us/services/storage/blobs/>`_

 * Datasets. For AWS, Datasets storage must be backed by EFS (see `Datasets storage <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#datasets-storage>`_). For other infrastructure, the kfs storage class is used. 

 .. _Blob storage: <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#blob-storage>

 .. _Blob storage: <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#blob-storage>

 .. _S3: <https://aws.amazon.com/s3/>

 .. _Azure Blob Storage: <https://azure.microsoft.com/en-us/services/storage/blobs/>

 .. _Datasets storage: <https://admin.dominodatalab.com/en/5.0.1/kubernetes/eks.html#datasets-storage>

**On-Prem** 

In on-prem environments, both  kdisk and kfs can be backed by NFS. In some cases, host volumes can be used (and even preferred). Host volumes are preferred for the Git, Postgres, and MongoDB. Postgres and MongoDB provide state replication. Host volumes can be used for Runs, but not preferred since we want leverage files cached in block storage that can move between nodes. If host volumes are used for Runs, file caching should be disabled and you will potentially expect slow start up executions for large Projects. 

**Node requirements** 

OS requirement = ubuntu 20.04 

.. list-table:: OS requirement = ubuntu 20.04 
   :widths: 60 60 60 60 60 60
   :header-rows: 1

   * - Nodes
     - CPU
     - Memory
     - OS Drive 
     - Additional disk
     - GPU 

   * - Master Nodes 
     - 4
     - 8 
     - >=30Gb 
     - Not required 
     - Not Required
   * - Worker Node
     - 8
     - 16 
     - >=30Gb
     - >=100 Gb 
     - Optional

**Cluster networking** 

Katonic relies on `Kubernetes network policies <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_ to manage secure communication between pods in the cluster. Network policies are implemented by the network plugin, so your cluster use a networking solution which supports ``NetworkPolicy``, such as `Calico <https://docs.projectcalico.org/v3.11/getting-started/kubernetes/>`_. 

.. _Kubernetes network policies: <https://kubernetes.io/docs/concepts/services-networking/network-policies/>

.. _Calico: <https://docs.projectcalico.org/v3.11/getting-started/kubernetes/>

**Ingress and SSL** 

Katonic platform will need to be configured to serve from a specific FQDN, and DNS for that name should resolve to the address of an SSL-terminating load balancer with a valid certificate. The load balancer must target incoming connections on ports 80 and 443 to port 80 on all nodes in the Platform pool. This load balancer must support websocket connections. 

Encryption in transit
------------------------ 

Intra-cluster encryption in transit is implemented via a deployed service mesh, specifically `Istio <https://istio.io/>`_. At installation time, Domino can deploy Istio for Domino use only, or Domino can be configured to leverage an existing deployed Istio on the Kubernetes cluster (potentially shared with other applications). See `Installation Configuration Reference <https://admin.dominodatalab.com/en/5.0.1/installation/installer-configuration.html#istio>`_ for details. 

 
Out of the box, Istio provides scalable `identity and X.509 certificate management <https://istio.io/latest/docs/concepts/security/#pki>`_ for use with mTLS encryption, including periodic certificate and key rotation. Because all encrypted communication is internal, these certificates are not exposed or required for communication to any external services, such as web browsers and clients. 

We do understand that certain enterprise policies mandate the use of corporate public key infrastructure (PKI) and necessitate the use of certificate authority (CA) certificates. 

.. _Istio: <https://istio.io/>

.. _Installation Configuration Reference: <https://admin.dominodatalab.com/en/5.0.1/installation/installer-configuration.html#istio>]

.. _identity and X.509 certificate management: <https://istio.io/latest/docs/concepts/security/#pki>

Requirements checker
----------------------

You must create a account from Sign up page https://katonic.ai/signup.html

Katonic on EKS
--------------------

 * Kubernetes control moves to the EKS control plane with managed Kubernetes masters 

 * Katonic uses a dedicated Auto Scaling Group (ASG) of EKS workers to host the Katonic platform. 

 * ASGs of EKS workers host elastic compute for katonic executions 

 * AWS S3 is used to store user data, internal Docker registry, backups, and logs 

 * AWS EFS is used to store Katonic File Manager. 

 * The ``kubernetes.io/aws-ebs`` provisioner is used to create persistent volumes for katonic executions. 

 * `Calico <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>`_ is used as a network plugin to support `Kubernetes network policies <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_. 

 * Katonic cannot be installed on EKS Fargate, since Fargate does not support stateful workloads with persistent volumes. 
 
.. _Calico: <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>

.. _Kubernetes network policies: <https://kubernetes.io/docs/concepts/services-networking/network-policies/>

All nodes in such a deployment have private IPs, and internode traffic is routed by internal load balancer. Nodes in the cluster can optionally have egress to the Internet through a NAT gateway. 

**Setting up an EKS cluster for Katonic**
This section describes how to configure an Amazon EKS cluster for use with Katonic. Administrators configuring an EKS cluster for Katonic should be familiar with the following AWS services: - Elastic Kubernetes Service (EKS) - Identity and Access Management (IAM) - Virtual Private Cloud (VPC) Networking - Elastic Block Store (EBS) - Elastic File System (EFS) - S3 Object Storage Additionally, a basic understanding of Kubernetes concepts like node pools, network CNI, storage classes, autoscaling, and Docker will be useful when deploying the cluster. 

**Requirement nodes configuration** 

 1. OS requirement = ubuntu 20.04 

 2. System requirements 

.. list-table:: OS requirement = ubuntu 20.04 
   :widths: 60 60 60 60 60 60
   :header-rows: 1

   * - Nodes
     - CPU
     - Memory
     - OS Drive 
     - Additional disk
     - GPU 

   * - Master Nodes 
     - 4
     - 8 
     - >=30Gb 
     - Not required 
     - Optional
   * - Worker Node
     - 8
     - 16 
     - >=30Gb
     - >=30Gb 
     - Optional

**Security Considerations** 

You will need to create IAM policies in the AWS console in order to provide an EKS cluster. We recommend following the standard security practice of granting the least privilege when you create IAM policies. Begin with the least privileges and then grant elevated privileges when necessary. `Additional information on the grant least privilege concept is available here <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege>`_. 

.. _Additional information on the grant least privilege concept is available here: <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege>

**Service Quotas** 

Amazon maintains default service quotas for each of the services listed above. You can check the `default service quotas <https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html>`_ and manage your quotas by logging in to the `AWS Service Quotas console <https://console.aws.amazon.com/servicequotas/home>`_. 

 .. _default service quotas: <https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html>

 .. _AWS Service Quotas console: <https://console.aws.amazon.com/servicequotas/home>

**VPC networking** 

If you plan to do `VPC peering <https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html>`_ or set up a `site-to-site VPN connection <https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html>`_ to connect your cluster to other resources like data sources or authentication services, be sure to `configure your cluster VPC accordingly <https://eksctl.io/usage/vpc-networking/>`_ to avoid any address space collisions. 

.. _VPC peering: <https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html>

.. _site-to-site VPN connection: <https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html>

.. _configure your cluster VPC accordingly: <https://eksctl.io/usage/vpc-networking/>
 
**Namespaces** 

No namespace configuration is necessary prior to installation. Katonic will create some namespaces in the cluster during installation. 

 

**Node pools** 

The EKS cluster must have at least two ASGs that produce worker nodes with the following specifications and distinct node labels, and it may include an optional GPU pool: 

The platform ASG can run in 1 availability zone or across 3 availability zones. If you want Katonic to run with some components deployed as highly available `ReplicaSets <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>`_ You must use 3 availability zones. Using 2 zones is not supported, as it results in an even number of nodes in a single failure domain. Note that all compute node pools you use should have corresponding ASGs in any AZ used by other node pools. Setting up an isolated node pool in one zone can cause volume affinity issues. 

To run the default and default-gpu pools across multiple availability zones, you will need duplicate ASGs in each zone with the same configuration, including the same labels, to ensure pods are delivered to the zone where the required ephemeral volumes are available. 

The easiest way to get suitable drivers onto GPU nodes is to use the `EKS-optimized AMI distributed by Amazon <https://docs.aws.amazon.com/eks/latest/userguide/gpu-ami.html>`_ as the machine image for the GPU node pool. 

Additional ASGs can be added with distinct Katonicdatalab.com/node-pool labels to make other instance types available for Katonic executions. Read Managing the Katonic compute grid to learn how these different node types are referenced by label from the Katonic application. 

.. _ReplicaSets: <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>

.. _EKS-optimized AMI distributed by Amazon: <https://docs.aws.amazon.com/eks/latest/userguide/gpu-ami.html>
 
**Network plugin** 

Katonic relies on `Kubernetes network policies <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_ to manage secure communication between pods in the cluster. Network policies are implemented by the network plugin, so your cluster uses a networking solution that supports NetworkPolicy, such as `Calico <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>`_. 

Refer to `the AWS documentation on installing Calico <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>`_ for your EKS cluster. 

If you use the `Amazon VPC CNI <https://github.com/aws/amazon-vpc-cni-k8s>`_ for networking, with only Network Policy enforcement components of Calico, you should ensure the subnets you use for your cluster have CIDR ranges of sufficient size, as every deployed pod in the cluster will be assigned an elastic network interface and consume a subnet address. Katonic recommends at least a /23 CIDR for the cluster. 

.. _Kubernetes network policies: <https://kubernetes.io/docs/concepts/services-networking/network-policies/>

.. _Calico: <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>

.. _the AWS documentation on installing Calico: <https://docs.aws.amazon.com/eks/latest/userguide/calico.html>

.. _Amazon VPC CNI: <https://github.com/aws/amazon-vpc-cni-k8s>


Domino on GKE
--------------------

Katonic on AKS 
--------------------

Katonic can run on a Kubernetes cluster provided by the `Azure Kubernetes Service <https://azure.microsoft.com/en-us/services/kubernetes-service/>`_. When running on AKS, the Katonic architecture uses Azure resources to fulfill the Katonic cluster requirements as follows: 

.. _Azure Kubernetes Service: <https://azure.microsoft.com/en-us/services/kubernetes-service/>

 * For a complete Terraform module for Domino-compatible AKS provisioning, see `terraform-azure-aks on GitHub <https://github.com/dominodatalab/terraform-azure-aks>`_. 

 * Kubernetes control is handled by the AKS control plane with managed Kubernetes masters. 

 * The AKS cluster’s default `node pool <https://docs.microsoft.com/en-us/cli/azure/ext/aks-preview/aks/nodepool?view=azure-cli-latest>`_ is configured to host the katonic platform. 

 * Additional AKS node pools provide compute nodes for user workloads. 

 * Starting with Katonic, when Katonic is deployed in AKS, it is compatible with the containerd runtime, which is the AKS default runtime for Kubernetes 1.19 and above. 

 * When using the containerd runtime, Katonic images are stored in Azure Container Registry. 

 * An `Azure storage account <https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview>`_ stores Katonic blob data and datasets. 

 * The ``kubernetes.io/azure-disk`` provisioner is used to create persistent volumes for Katonic executions 

 * The Advanced Azure CNI is used for cluster networking, with network policy enforcement handled by Calico 

 * Ingress to the Domino application is handled by an SSL-terminating `Application Gateway <https://docs.microsoft.com/en-us/azure/application-gateway/overview>`_ that points to a Kubernetes load balancer. 

.. _terraform-azure-aks on GitHub: <https://github.com/dominodatalab/terraform-azure-aks>

.. _node pool: <https://docs.microsoft.com/en-us/cli/azure/ext/aks-preview/aks/nodepool?view=azure-cli-latest>

.. _Azure storage account: <https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview>

.. _Application Gateway: <https://docs.microsoft.com/en-us/azure/application-gateway/overview>

**Resource groups** 

You can provide the cluster, storage, and application gateway in an existing resource group. Note that in the process of creating the cluster itself, Azure will create a separate resource group that will contain the cluster components themselves. 

 
**Namespaces** 

No namespace configuration is necessary prior to installation. Katonic will create some namespaces in the cluster during installation. 

 

**Node pools** 

The AKS cluster’s initial default node pool can be sized and configured to host the must have at least two node pools that produce worker nodes with the following specifications and distinct node labels, and it may include an optional GPU pool: 

 

**Requirement nodes configuration** 

OS requirement = ubuntu 20.04 

System requirements

.. list-table:: OS requirement = ubuntu 20.04 
   :widths: 60 60 60 60 60 60
   :header-rows: 1

   * - Nodes
     - CPU
     - Memory
     - OS Drive 
     - Additional disk
     - GPU 

   * - Master Nodes 
     - 4
     - 8 
     - >=30Gb 
     - Not required 
     - Optional 
   * - Worker Node
     - 8
     - 16 
     - >=30Gb
     - >=30Gb 
     - Optional

**Network plugin** 

Katonic relies on `Kubernetes network policies <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_ to manage secure communication between pods in the cluster. Network policies are implemented by the network plugin, so your cluster uses a networking solution that supports NetworkPolicy, such as Calico. 

.. _Kubernetes network policies: <https://kubernetes.io/docs/concepts/services-networking/network-policies/> 

**Dynamic block storage** 

AKS clusters come equipped with several kubernetes.io/azure-disk backed storage classes by default. Domino requires use of premium disks for adequate input and output performance. The managed-premium class that is created by default can be used. Consult the following storage class specification as an example. 

:: 
  
  allowVolumeExpansion: true 
  apiVersion: storage.k8s.io/v1 
  kind: StorageClass 
    metadata: 
    labels: 
      kubernetes.io/cluster-service: "true" 
    name: managed-premium 
    selfLink: /apis/storage.k8s.io/v1/storageclasses/default 
  parameters: 
    cachingmode: ReadOnly 
    kind: Managed 
    storageaccounttype: Premium_LRS 
  reclaimPolicy: Delete 
  volumeBindingMode: Immediate 
 


Domino on OpenShift
--------------------

NVIDIA DGX in Domino
--------------------

Katonic in Multi-Tenancy K8s cluster
------------------------------------------------
**What is Multi-Tenancy?** 

In the context of Kubernetes and Katonic, multi-tenancy means a Kubernetes cluster (hereinafter simply referred to as “cluster” unless otherwise disambiguated) that supports multiple applications and is not dedicated just to Katonic (i.e., each application is an individual cluster tenant). Katonic supports multi-tenant clusters (or multi-tenancy) by adhering to a set of principles that ensure it does not interfere with other applications or other cluster-wide services that may exist. This also translates to the installation of Katonic into a multi-tenant cluster, assuming typical best practice multi-tenancy constraints.

**Multi-Tenancy Use Cases** 

 * On-Premise and Capacity Constrained Environments. In this case, you are trying to maximize the utilization of limited, often physical, infrastructure. 

 * Minimize Administration Costs. 

**Multi-Tenancy Risks** 

 * Shared Resource Loading. Multi-tenant clusters still share common resources, such as the Kubernetes control plane (e.g., API server), DNS, and ingress. This results in how other applications will impact Katonic and vice versa. 

 * Imperfect Compute Isolation and Predictability.

   * Unless you restrict node-level usage for applications, there is no isolation at the node level. Hence, Katonic Runs will potentially share compute with other applications.  

   * Ill-behaved tenants could impact Katonic Runs by hogging resources causing drops in resources available to Katonic or in the worst case, bring down the node.  

   * In most cases, this will probably not happen. However, if particular Katonic Runs need predictability or strict isolation, this may be an issue.  

   * You can reserve nodes just for the Katonic application in your cluster, but this does drive down the argument for multi-tenancy. 

 * Increased Security Complexity and Risk. Cluster administrators will likely have to manage a larger, or finer grain, set of RBAC objects and rules. Shared resources and node-level coupling exposes an additional attack surface for any malicious tenants. 

 * Shared Cluster Maintenance. Any cluster maintenance will cause all applications to be subject to the same maintenance window. Hence, if the cluster maintenance is due to a particular application, all applications will be subjected to the same down time even though they do not require that maintenance. 

**Requirement nodes configuration**

 1. OS requirement = ubuntu 20.04 

 2. System requirements 

.. list-table:: OS requirement = ubuntu 20.04 
   :widths: 60 60 60 60 60 60
   :header-rows: 1

   * - Nodes
     - CPU
     - Memory
     - OS Drive 
     - Additional disk
     - GPU 

   * - Master Nodes 
     - 4
     - 8 
     - >=30Gb 
     - Not required 
     - Optional 
   * - Worker Node
     - 8
     - 16 
     - >=30Gb
     - >=30Gb 
     - Optional

**Known Considerations** 

**Files** 

If two or more applications attempt to map a file from the “host path” and read or modify that file, then problems can arise. The use of host paths is frowned upon except for monitoring software and currently, the only place that Katonic requires a host mount is for fluentd to monitor container logs. As this is standard practice for `fluentd <https://www.fluentd.org/>`_ and an explicitly read-only operation, we will not interfere with other applications. 

.. _fluentd: <https://www.fluentd.org/> 

**System Settings** 

Applications that require system settings to be modified for performance or reliability can interfere with or overwrite other applications’ settings. 

**Elasticsearch** 

Currently, the only service that requires an updated setting for Katonic is `Elasticsearch <https://www.elastic.co/elasticsearch/>`_ and this is currently disable-able if the cluster operators have an acceptable setting already. ``vm.map_max_count`` needs to be set for Elasticsearch to work; This is not a Katonic requirement, but a mandatory `requirement from the upstream Elasticsearch Helm chart <https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html#vm-max-map-count>`_. 

.. _Elasticsearch: <https://www.elastic.co/elasticsearch/> 

.. _requirement from the upstream Elasticsearch Helm chart: <https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html#vm-max-map-count> 

**GPU Support** 

We deploy a number of services in order to properly expose GPUs for Katonic. In a multi-tenant environment, we would generally ask cluster administrators to manage these themselves, and we can disable our services via our installer. 

**DaemonSets** 

We currently deploy four `DaemonSets <https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/>`_ for standard install. 

 1. ``docker-registry`` **Certificate Management**. This allows the underlying Docker daemon to pull from the Katonic deployed Docker registry, which backs `Katonic Compute Environments <https://docs.dominodatalab.com/en/latest/reference/environments/Video_introduction_to_Domino_Environments.html>`_. The service mounts the underlying ``/etc/docker/certs.d`` directory and creates additional files to support the Katonic Docker registry. This is not something that can necessarily interfere with other applications but may cause concern from cluster operators and any host-level operation is inherently risky. 

 2. ``image-cache-agent``. This handle look-ahead caching and image management for the cluster Docker daemon, allowing for shorter Katonic execution start-up times. This should not be deployed on non-Katonic nodes. 

 3. ``fluentd``. This monitors logs from the User’s compute containers that pushed through a system to feed into the Jobs and Workspaces dashboard. See Files. 

 4. ``prometheus-node-exporter``. This monitors node metrics, such as network statistics, and it is polled by the Katonic deployed Prometheus server. This can be disabled with the ``monitoring.prometheus_metrics flag``. 

As of Katonic 4.2, all DaemonSets can be limited by a ``nodeSelector`` flag which will cause the pods to only be scheduled on a subset of nodes with a specific label. Depending on the cluster operator’s needs, we will require a categorical label on nodes for Katonic’s use that we could target for deployment.  

(Add some daemonsets for ceph) 

**Non-Namespaced Resources** 

**ClusterRoles** 

Katonic creates separate namespaces for its services and requires communication between these namespaces. Katonic creates a number of ClusterRoles and bindings that control access its namespaces or into global resources. As of Katonic, all Katonic-created ClusterRoles are prefixed by the deployment name, which is specified by the name ``key`` in the ``Katonic.yml`` configuration file  

**Pod Security Policies** 

By default, Katonic uses `pod security policies <https://kubernetes.io/docs/concepts/policy/pod-security-policy>`_ (PSP) to ensure that, by default, pods cannot use system-level permissions that they have not been granted. Unfortunately, PSPs are globally-namespaced so they too have been prefixed with the deployment name. Applications cannot use these PSPs without explicitly being granted access through a Role or Cluster Role. 

**Custom Resource Definitions** 

Katonic does not make extensive use of `Custom Resource Definitions <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>`_ (CRDs) except for the on-demand spark feature in 4.x. Our CRD is named uniquely, ``sparkclusters.apps.Katonicdatalab.com`` and should not interfere with other applications. 

Persistent Volumes 

Katonic uses `persistent volumes <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>`_ extensively throughout the system to ensure that data storage is abstracted and permanent. With the exception of two shared storage mounts, which both incorporate namespaces to ensure uniqueness, we strictly use dynamic volume creation through `persistent volume claims <https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims>`_ which dynamically allocates a name that will not conflict with any other applications. 

.. _DaemonSets: <https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/> 

.. _Katonic Compute Environments: <https://docs.dominodatalab.com/en/latest/reference/environments/Video_introduction_to_Domino_Environments.html> 

.. _pod security policies: <https://kubernetes.io/docs/concepts/policy/pod-security-policy> 

.. _Custom Resource Definitions: <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/> 

.. _persistent volumes: <https://kubernetes.io/docs/concepts/storage/persistent-volumes/> 

.. _persistent volume claims: <https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims> 

Encryption in transit
------------------------

Compatibility
---------------

Requirement Checker 
---------------

We have our own script that can check the system's requirements. That script will run on your system and check the requirements for hardware and packages that Katonic platform requires. 