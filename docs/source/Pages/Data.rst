Data
===============

Katonic.ai is an Machine Learning (ML) and Artificial Intellegence  (AI) company that provide Pipelines and show ml model.
Follow these instructions to start Katonic.ai.

Data In Katonic 
------------------------

There are basically two systems that store user data in Katonic: 

 * Project files in Katonic 

 * File manager in Katonic 

Katonic supports connecting to many external data stores. Users can import data from external stores into Katonic , they export data from Katonic to external stores, or run code in Katonic that reads and writes from external stores without saving data in Katonic itself. 

  

***1. Project Files:*** 

 * Every Katonic project has a corresponding collection of project files.  

 * Project files are stored in a durable object storage system. 

 * Katonic has native support for backing up the storage with the following cloud storage services: -  

 * Amazon S3  

 * Azure File Storage 

 * The Katonic Blob Store can be backed with a shared Kubernetes Persistent Volume from a compatible storage class.  

 * If desired, you can provide an NFS storage service, and Katonic installation utilities can deploy the nfs-client-provisioner and configure a compatible storage class backed by the provided NFS system. 

  

***2. Is project file data encrypted?*** 

 * Katonic supports server-side encryption with customer-provided keys (SSE-C) for Amazon S3. 

 * Katonic supports EBS file system encryption using the industry-standard AES-256 algorithm on Elastic Block Store. 

 * Katonic also supports default encryption keys for: - Amazon S3 - Azure File Storage  

 * Katonic does not provide pre-write encryption for nfs-client-provisioner volumes. 

***3. How does data get stored in project files?***

 * When a user starts a run in Katonic , the files from his or her project are fetched from the Katonic File Manager and loaded into the run in the working directory of the Katonic service filesystem.  

 * When the Run finishes, or the user initiates a manual sync in an interactive Workspace session, any changes to the contents of the working directory are written back to Katonic as a new revision of the project files.  

 * Katonic’s versioning system tracks file-level changes and can provide rich file difference information between revisions. 
 
 Katonic also has several features that provide users with easy paths to quickly initiating a file sync. The following events in Katonic can trigger a file sync, and the subsequent creation of a new revision of a project’s files.  

 * User uploads files from the Katonic web application upload interface 

 * User authors or edits a file in the Katonic web application file editor 

 * User syncs their local files to Katonic from the Katonic Command Line Interface 

 * User uploads files to Katonic via the Katonic API 

 * User executes code in a Katonic Job that writes files to the working directory 

 * User writes files to the working directory during an interactive Workspace session, and then initiates a manual sync or chooses to commit those files when the session finishes 

By default, all revisions of project files that Katonic creates are kept indefinitely, since project files are a component in the Katonic Reproducibility Engine. It is always possible to return to and work with past revisions of project files, with the exception of files that have been subjected to a full delete by a system administrator. 

 

***3. Who can access the data in project files?*** 

 * Users can read and write files to the projects they create, on which they automatically are granted an Owner role. Owners can add collaborators to their projects with the following additional roles and associated files permissions. 

 * The permissions available to each role are described in more detail in Sharing and collaboration. 

 * Users can also inherit roles from membership in Katonic Organizations.  

 * Katonic users with some administrative system roles are granted additional access to project files across the Katonic deployment they administer.  

***4. How is the data in Katonic File manager stored?*** 

 * When users have large quantities of data, including collections of many files and large individual files, Katonic recommends storing the data in a Katonic Dataset. File managers are collections of Snapshots, where each Snapshot is an immutable image of a filesystem directory from the time when the Snapshot was created.  

 * These directories are stored in a network filesystem managed by Kubernetes as a shared Persistent Volume. 

 * Katonic has native support for backing Katonic File manager with the following cloud storage services: - Amazon EFS - Azure File Storage  

 * Alternatively, the Katonic File Manager can be backed with a shared Kubernetes Persistent Volume from a compatible storage class. If on-premises installation you can provide a disk attached to the storage nodes on which Katonic Platform configures a reliable file system.   

 * Each Snapshot of a Katonic Dataset is an independent state, and its membership in a Dataset is an organizational convenience for working on, sharing, and permissioning related data. Katonic supports running scheduled Jobs that create Snapshots, enabling users to write or import data into a Dataset as part of an ongoing pipeline. 

 * Dataset Snapshots can be permanently deleted by Katonic system administrators. Snapshot deletion is designed as a two-step process to avoid data loss, where users mark Snapshots they believe can be deleted, and admins then confirm the deletion if appropriate. This permanent deletion capability makes File manager the right choice for storing data in Katonic that has regulatory requirements for expiration. 

 

***5. Who can access the data in Katonic File manager?*** 

 * File manager in Katonic belong to projects, and access is afforded accordingly to users who have been granted roles on the containing project. 

 * The permissions available to each role are described in more detail in Sharing and collaboration. 

 * Users can also inherit roles from membership in Katonic Organizations.  

 * Katonic users with administrative system roles are granted additional access to File manager across the Katonic deployment they administer 

  

  

***6. Integrating Katonic with other data stores and databases*** 

 * Katonic can be configured to connect to external data stores and databases. This process involves loading the required client software and drivers for the external service into a Katonic environment, and loading any credentials or connection details into Katonic environment variables. Users can then interact with the external service in their Runs. 

 * Users can import data from the external service into their project files by writing the data to the working directory of the Katonic service filesystem, and they can write data from the external service to Dataset Snapshots.  

 * Alternatively, it is possible to construct workflows in Katonic that save no data to Katonic itself, but instead pull data from an external service, do work on the data, then push it to an external service. 

  

***7. Tracking and auditing data interactions in Katonic*** 

 * Katonic system administrators can set up audit logs for user activity in the platform. These logs record events whenever users: 

 * Create files 

 * Edit files 

 * Upload files 

 * View files 

 * Sync file changes from a Run 

 * Mount Dataset Snapshots 

 * Write Dataset Snapshots 

Data flow in Katonic 
----------------------

There are three ways for data to flow in and out of a Katonic Run. 

1. Katonic File Store: 

* Each Katonic Run takes place in a project, and the files for the active revision of the project are automatically loaded into the local execution volume for a Job or Workspace according to the specifications of the Katonic Service Filesystem.  

* These files are retrieved from the Katonic File Store, and any changes to these files are written back to the Katonic File Store as a new revision of the project’s files. 

2. Katonic Datasets: 

* Katonic Runs may optionally be configured to mount Katonic Datasets for input or output. Datasets are network volumes mounted in the execution environment.  

* Mounting an input Dataset allows for a Job or Workspace to both start quickly and have access to large quantities of data, since the data is not transferred to the local execution volume until user code performs read operations from the mounted volume.  

* Any data written to an output Dataset is saved by Katonic as a new snapshot. 

3. External data systems: 

* User code running in Katonic can use third party drivers and packages to interact with any external databases, APIs, and file systems that the Katonic-hosting cluster can connect to.  

* Users can read and write from these external systems, and they can import data into Katonic from such systems by saving files to their project or writing files to an output Dataset. 

External Data Volumes
------------------------

External data volumes must be registered with Katonic before they can be used. All registered external data volumes appear in a standard table, which display the EDV name, type, description, and volume access (see Volume Properties). In addition, for each registered EDV, the Projects column indicates which projects had added the EDV. 

  

***Setting up Kubernetes PV and PVC (Storage class)*** 

Katonic runs on a Kubernetes cluster and EDVs must be backed by an underlying Kubernetes persistent volume (PV). That persistent volume must be bound to a persistent volume claim (PVC) The value of that key represents the type of external data volume. Currently, the supported types are NFS, SMB, and EFS. Finally, the PVC must be created in the Katonic compute namespace. 

  

  

***Registering external data volumes*** 

To register an EDV with Katonic, click the Register External Volume button on the upper right-hand size of the EDV administration page. This will open a modal with the EDV registration wizard. The wizard will guide administrators to register the EDV by configuring various EDV properties  

  

***Volume*** 

The first step in the wizard is to select the volume type. The current supported volume types are NFS and EFS. 

The Available Volumes list will show all candidate volumes of the selected type. The name of these volumes is the name of the backing Kubernetes persistent volume claim (PVC) 

  

***Configuration*** 

The second step in the wizard is to configure the volume. 

***Access*** 

The third step in the wizard is to define the volume access. See Volume Properties and Authorization. 

 * Everyone. Allow EDV access to all logged-in users. 

 * Specific users or organizations. Limit EDV access to specific users and organizations. 

***Viewing registered external data volume details*** 

To view a registered EDV details, click on the Name of the EDV in the admin table 

***Editing registered external data volumes*** 

To edit the details of a registered EDV, click on the vertical three dots on the right-hand side of its entry in the admin EDV table. This will expose the Edit action. Click Edit to edit the EDV details. 

***Unregistering external data volumes*** 

To unregister an EDV, click on the vertical three dots on the right-hand side of its entry in the admin EDV table. This will expose the Unregister action.

Datasets administration
-----------------------------

***Accessing the Datasets administration interface*** 

To access the Datasets administration interface, click Admin from the Katonic main menu to open the Admin home, then click Advanced > Datasets. 

***Monitoring Datasets usage*** 

The Datasets administration page shows important information about Datasets usage in your deployment. At the top of the interface is a display that shows: 

 * total storage size used by all stored Snapshots 

 * the size of all storage used by Snapshots marked for deletion 

Below that display is a table of all Snapshots from the history of the deployment. This table can be sorted by Snapshot status, size, and the name of the containing Dataset. 

Setting limits on Datasets usage 

There are two important central configuration options administrators can use to limit the growth of storage consumption by Datasets. 

Namespace: common 

Key: com.cerebro.Katonic.dataset.quota.maxActiveSnapshotsPerDataset 

Value: number 

Default: 20 

This option controls the maximum number of active Snapshots that may 

be stored in a Dataset. Snapshots marked for deletion are not active 

and do not count against this limit. 

  

If a Dataset reaches one of these limits, attempting to start a run with a Dataset configuration that could output a new Snapshot will result in an error message. Before additional Snapshots can be written, you will need to delete old snapshots or increase the limit. 

Administrators can authorize individual projects to ignore these limits with an option in the Hardware & environment tab of the project settings. 

Deleting Snapshots from Datasets 

Administrators can delete entire Datasets or individual Snapshots at any time using the Delete action at the end of each row. Initiating this action will result in a confirmation dialog, and if you choose to confirm, the Dataset (and all associated Snapshots) or the individual Snapshot will be permanently deleted. If the action was initiated by mistake, an administrator can still recover a dataset or snapshot before the delete grace period (see above) expires the delete operation is initiated. 

When a Dataset or a Snapshot is deleted, it will no longer be available for future executions. Executions that are in progress will also be affected if they attempt to read or write to the dataset that is deleted. To avoid disruptions, Katonic recommends following a two-step process for Dataset and Snapshot deletion, where the user who owns the Dataset mark it for deletion, excluding it from any new executions that start. An administrator then takes the action to delete the Dataset or Snapshot, if appropriate. Non-administrator users can never permanently delete a Dataset or Snapshots on their own. 

From the Datasets administration UI, you will have the option to Delete all marked datasets or Delete all marked snapshots and perform bulk delete confirmations. Alternatively, you can sort the tables by status to easily find all Datasets to Snapshots marked for deletion. 

Delete all file instances from the Katonic file system 

Katonic system administrators can use a full delete operation to completely remove all instances of a file from the Katonic file system. Performing a full delete on a file finds all instances of the file’s contents across all revisions of all projects, erases those contents wherever they appear, and replaces them with a message indicating that the file was subject to a full delete. This affects all files that have identical contents to the target file, even if they have different filenames. It does not affect files with the same filename if they have different contents. 

Submitting GDPR requests
----------------------------

