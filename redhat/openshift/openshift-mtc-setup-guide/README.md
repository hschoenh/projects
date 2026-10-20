# Migration Toolkit for Containers (MTC) on OpenShift 4.21

A practical guide to setting up the **Migration Toolkit for Containers (MTC)** for migrations between OpenShift clusters. It covers installation, cluster registration, the replication repository, migration plans, staging, cutover, and validation.

> **Version note:** Use only an MTC Operator version supported for the exact OpenShift version in use. Before production use, check the [Red Hat documentation for OCP 4.21](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html/migration_toolkit_for_containers/index) and its linked support and compatibility matrix. This guide does not replace that check.

## Contents

- [What MTC migrates](#what-mtc-migrates)
- [Prerequisites](#prerequisites)
- [Install MTC](#install-mtc)
- [Open the web console and troubleshoot a missing route](#open-the-web-console-and-troubleshoot-a-missing-route)
- [Register the source and target clusters](#register-the-source-and-target-clusters)
- [Configure the replication repository](#configure-the-replication-repository)
- [Plan and run a migration](#plan-and-run-a-migration)
- [Validate and plan for rollback](#validate-and-plan-for-rollback)
- [Security and credential handling](#security-and-credential-handling)
- [Troubleshooting](docs/troubleshooting.md)

## What MTC migrates

MTC migrates selected Kubernetes resources and, depending on the plan, container images and persistent volume data at namespace level. Dependencies outside the selected scope, external systems, DNS, load balancers, certificates, and application-specific data consistency must be assessed and planned separately.

With an **indirect migration**, data is transferred through a shared object storage repository. For supported topologies, Direct Image Migration and Direct Volume Migration can shorten the data path. Availability and suitability depend on the MTC version, cluster network, registry, storage, and proxy configuration.

- **Stage:** Data is copied in advance while the application continues running on the source. This can reduce the later maintenance window.
- **Cutover:** Final synchronization and workload switch. Applications can be interrupted during this step.
- **Copy:** Source data is retained.
- **Move:** Source data can be removed as part of the process. Check the implications and Red Hat behavior for the selected storage method before using it.

Staging does not replace application-consistent backups or a tested recovery procedure.

## Prerequisites

### Permissions and compatibility

- Administrative access, as required by Red Hat, on the MTC and participating clusters. Installation and configuration usually require `cluster-admin`.
- A supported combination of OpenShift versions, MTC version, and migration mode.
- Access to the Operator catalog. In disconnected environments, mirror the appropriate catalog and required images.
- Project and resource quotas on the target cluster.

### Network and TLS

Prepare a connectivity matrix for the API, Routes, registry, replication repository, and, where applicable, the direct volume data path. Typical destinations include the OpenShift API over TCP 6443, HTTPS/Routes over TCP 443, and traffic required by the repository and migration mode. Required ports and connections depend on the topology. Derive them from the official MTC documentation and cluster endpoints instead of opening broad firewall rules by default.

Check DNS resolution, certificate chains, network policies, egress rules, and MTU. Proxies can disrupt upgraded connections or direct volume traffic. An HTTP(S) proxy that intercepts TLS is not automatically suitable for this data path. Plan proxy exclusions and, if required, a transparent TCP tunnel according to Red Hat guidance.

### Persistent volumes

- PVCs must be bound. Target storage classes must be available or mapped to an appropriate target storage class.
- Snapshot-based copy requires support from the storage provider and a compatible snapshot configuration.
- For file-system copy, check target volume capacity, performance, and permissions.
- Databases and other applications need an application-specific consistency and freeze plan.

## Install MTC

Install MTC on a **host cluster**. By default, the MTC web console and Migration Controller run on this cluster. In simple deployments, this is often the target cluster.

1. Sign in to the OpenShift web console for the host cluster with an appropriately privileged account.
2. Open **Ecosystem → Software Catalog**.
3. Search for **Migration Toolkit for Containers Operator** and install a version supported by the compatibility matrix. The target project is usually `openshift-migration`.
4. Open the Operator under **Installed Operators**.
5. Under **Provided APIs**, select **Create instance** for **Migration Controller** and create it.
6. Check the pods and controller:

```bash
oc get pods -n openshift-migration
oc get migrationcontroller -n openshift-migration
oc get sub,ip,csv -n openshift-migration
```

Continue only after the Operator, controller, and associated pods are ready. Pod names and counts can vary by MTC version.

A minimal, non-sensitive example of the controller instance is in [`examples/migrationcontroller.yaml`](examples/migrationcontroller.yaml). The web console is the preferred path for initial installation. Change custom resource fields only according to the documentation for the installed Operator version.

## Open the web console and troubleshoot a missing route

The web console is exposed through a Route in the `openshift-migration` namespace. Read the actual route name and host from the cluster:

```bash
oc get routes -n openshift-migration
oc get route migration -n openshift-migration \
  -o go-template='https://{{ .spec.host }}{{ "\n" }}'
```

`NotFound` means that a Route with that name does not currently exist in the namespace. A common cause is that the `MigrationController` instance has not been created, or the Operator could not create the UI resources.

```bash
oc get migrationcontroller -n openshift-migration
oc get pods -n openshift-migration
oc get services,routes -n openshift-migration
oc get events -n openshift-migration --sort-by=.lastTimestamp
```

If no controller instance exists, create one through **Installed Operators → Migration Toolkit for Containers Operator → Provided APIs → Migration Controller → Create instance**. Then check the pods and route again. Do not hard-code a route using a guessed internal hostname.

## Register the source and target clusters

In the MTC web console, open **Clusters → Add cluster** and register each cluster:

- **Name:** A unique, simple name, for example `source` or `target`.
- **API endpoint:** `https://<api-endpoint>:6443`.
- **Service account token:** A short-lived token created for the service account procedure required by MTC.
- **CA certificate / SSL verification:** Keep certificate verification enabled. If the cluster uses a private CA, provide the appropriate CA chain.
- **Registry route:** Configure only if required by the selected mode and its documentation, for example for Direct Image Migration.

A short-lived token can be created on each remote cluster. Example for the documented service account identity:

```bash
oc create token migration-controller -n openshift-migration
```

The command prints a sensitive bearer token. Do not copy it into shell history, tickets, chat, Git, or logs. Paste the token directly into the MTC console and issue a new one when necessary. Verify the service account and its permissions against the installed MTC version before use.

If a registry Route is required, use the Red Hat-supported procedure and assess the resulting access. A registry Route can expose images and is a security-relevant change. Do not expose it publicly without an explicit review. The following command is one possible administrative action, not a default for every installation:

```bash
oc create route passthrough --service=image-registry --port=5000 \
  -n openshift-image-registry
```

After adding the clusters, verify their connection status in the MTC console.

## Configure the replication repository

Indirect migrations require object storage that all participating clusters can reach. Supported providers and required fields depend on the installed MTC version. In the MTC console, open **Replication repositories → Add repository**:

1. Select the repository type and a supported storage provider.
2. Enter the bucket/container, region or endpoint, and required options.
3. Enter credentials in the designated credential field or provide a Secret using the applicable Red Hat procedure.
4. For a private TLS CA, provide the certificate according to the product documentation and keep verification enabled.
5. Test the connection and assign the repository to the migration plan.

For OCI or another S3-compatible service, do **not** put tenancy/account IDs, OCIDs, namespace, bucket names, endpoints, fingerprints, keys, passwords, or signed URLs in this Git project. Use placeholders in documentation and store real values only in a secrets manager or the MTC field intended for credentials. Check actual OCI compatibility, API requirements, and signing requirements against the Red Hat support matrix; S3 compatibility alone does not guarantee support.

## Plan and run a migration

### 1. Pre-migration assessment

- Identify application owners, namespaces, maintenance windows, and acceptance criteria.
- Inventory Ingress/Routes, DNS, certificates, Secrets, ConfigMaps, RBAC, SCCs, storage classes, and external dependencies.
- Check quotas, resource requests, image pull access, PV size, backups, and restore procedures.
- Decide which namespaces and resources to exclude.
- Agree on database and application consistency, write freeze, and rollback plan with the responsible teams.

### 2. Create a migration plan

In the MTC web console, open **Migration plans → Create new plan**:

1. Select the source and target clusters and the replication repository.
2. Select namespaces and review resource and PV mappings.
3. Choose the storage class mapping and migration mode.
4. Choose a copy method: file-system copy or supported snapshot copy.
5. Choose **Copy** or **Move** deliberately. Copy is usually the lower-risk choice for an initial run.
6. Validate the plan and resolve all warnings or document why they are accepted.

### 3. Stage

Run a stage migration to copy data in advance. MTC reports status and errors for each migration run. Review the logs and plan, then check the data volume and target PVCs. Staging does not replace the final cutover.

### 4. Cut over

During the agreed maintenance window:

1. Stop writes or put the application in maintenance mode according to the application plan.
2. Run the final migration/cutover.
3. Do not leave source workloads accepting production writes in parallel if this could create split-brain or divergent data.
4. Start the target application and run data and functional checks.
5. Switch DNS, Ingress, or traffic only after business approval.

## Validate and plan for rollback

Before approval, check at least:

- Migration status is successful and there are no unexplained warnings.
- Deployments/StatefulSets, pods, PVCs, and events in the target namespace.
- Application logs, readiness/liveness, end-to-end functionality, and data integrity.
- User access, DNS, TLS, external integrations, monitoring, backup, and restore.
- Resource usage and performance under realistic load.

Define rollback criteria and owners before cutover. Once production writes start on the target, simply switching back to the source is not automatically lossless. Reverse synchronization or recovery must be planned for the application.

## Security and credential handling

This repository is intended for redacted documentation and reusable examples. It contains no production endpoints or credentials.

- Do not commit passwords, bearer tokens, private keys, hashes, Kubernetes Secret manifests, or real `.env` files.
- Do not commit internal OCI/cloud details: account or tenancy IDs, OCIDs, bucket names, private IPs, internal DNS names, fingerprints, region/compartment assignments, or signed URLs.
- Use placeholders such as `<api-endpoint>`, `<bucket-name>`, and `<credential>`. Replace placeholders before running commands.
- Kubernetes Secret data is Base64-encoded, not encrypted. Base64 is not redaction.
- Keep secret files outside the repository, restrict access, and rotate credentials as needed.
- Review `git diff --cached` and the file list before each commit. If a secret is committed by mistake, deleting it in a later commit is not enough: revoke or rotate the credential and clean Git history according to the incident process.

## Project structure

```text
.
├── README.md
├── docs/
│   └── troubleshooting.md
└── examples/
    └── migrationcontroller.yaml
```

## Initialize Git

```bash
git init
git add README.md docs examples .gitignore
git diff --cached --check
git diff --cached
git commit -m "Add OpenShift MTC setup guide"
```

## References

- [Red Hat: Migration Toolkit for Containers, OCP 4.21](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html/migration_toolkit_for_containers/index)
- [Red Hat: MTC Operator in the Red Hat Ecosystem Catalog](https://catalog.redhat.com/en/software/container-stacks/detail/5ec53fffef29fd35586d9a5a)

This project is a practical working guide. The documentation for the MTC Operator actually installed is authoritative for supportability and implementation details.
