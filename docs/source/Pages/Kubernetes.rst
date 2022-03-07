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

Domino on EKS
--------------------

Chat in the `#chat-with-Katonic`chat bot. Katonic bot will respond to anyone in this site.

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

Domino in Multi-Tenant Kubernetes Cluster
------------------------------------------------

Encryption in transit
------------------------

Compatibility
---------------
