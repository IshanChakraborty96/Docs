Disaster Recovery
======================

Katonic.ai is an Machine Learning (ML) and Artificial Intellegence  (AI) company that provide Pipelines and show ml model.
Follow these instructions to start Katonic.ai.

Backing up Katonic 
------------------------

**Backup Structure** 

 

The Katonic Platform backup store the entire user data and cluster state in one single cronjob, and the backup is named “katonic-platform-backup”. 

Backups are bundled into tarballs containing each and every component state and the data they hold. 

 

 

**Backup location** 

The default backup location varies depending on the infrastructure in which Katonic was installed: 

On AWS and Azure, a dedicated s3 bucket is required for storing backups. 

For on-premise deployments, backups are either stored on an s3 bucket provided by client through any storage system or stored locally on a different machine. 

 

Customize backups 

The following primary customizations are available through values fed to the ``domino-data-importer helm chart``: 

 * Backup schedule

 * Importer command-line arguments (The importer is the program that performs the backup. Typically, you do not have to customize this component.) 

 
 

 * Customize backup schedule 

 * Customize importer command-line arguments 

**Customize backup schedule**

Use the helm chart value ``backups.schedule`` to change the interval at which backups are performed. This is fed to a Kubernetes CronJob object. 

The default value is @daily, and any valid Kubernetes CronJob schedule string will work, for example: ``0 */4 * * *.`` The string mimics standard cron syntax. 

 
 

 
 

 
 

**Customize importer command-line arguments** 

Use the  ``backupJobScript helm chart value`` to customize the command that creates the backup bundles. The default command line arguments are: 

/app/importer -c /app/config-4x-example.yaml -b --backup-archive --backup-upload --backup-delete --backup-strategy BACKUP_STRATEGY 
 

Use the following argument, ``(--backup-strategy BACKUP_STRATEGY)`` to define the strategy to back up large-storage services (such as blobs). 

small: Backs up databases and Git only. 

transfer: Same as small, but includes a best-effort attempt to setup configuration files for remote import. 

large: Backs up everything (such as blobs) by pulling them locally from nfs/s3. Do not use in production. 

The transfer strategy adds options to the backup bundle’s importer configuration to copy blobs and other s3-stored data during a backup restore. This is useful if you are restoring to a new Domino deployment while the old one still exists. This is for advanced usage only. Do not use the large backup strategy because backing up the blobs, registry, and datasets into the bundle will become too large for even modest size Domino deployments. The large strategy is only useful for testing on development deployments. 

You can also remove --backup-delete for testing or debugging purposes because the argument backups are typically removed from local storage after upload. Removing the argument leaves the working directory for a backup intact, so you can troubleshoot the state of data prior to upload. 

 

**Run a manual, on-demand backup** 
----------------------------------
 

You can create a backup manually, on-demand. This can be useful during “lift-and-shift” migrations or prior to upgrades. 

To manually generate a backup: 

Run the following command: 

velero backup create katonic-platform-backup --wait 
 

 

**Restore backups**
-------------------- 

To restore a backup: 

velero restore create katonic-platform-restore  


