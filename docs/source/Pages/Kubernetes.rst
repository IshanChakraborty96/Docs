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

.. list-table:: Component & Logs
   :widths: 50 50 50 50 50 50
   :header-rows: 6

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

Requirements checker
----------------------

You must create a account from Sign up page https://katonic.ai/signup.html

Domino on EKS
--------------------

Chat in the `#chat-with-Katonic`chat bot. Katonic bot will respond to anyone in this site.

Domino on GKE
--------------------

Domino on AKS
--------------------

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
