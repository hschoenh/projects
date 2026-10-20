# MTC Troubleshooting

## The `migration` route is missing

Symptom:

```text
Error from server (NotFound): routes.route.openshift.io "migration" not found
```

First check whether a differently named route exists and whether the controller has been created:

```bash
oc get routes -n openshift-migration
oc get migrationcontroller -n openshift-migration
oc get pods,services -n openshift-migration
oc get events -n openshift-migration --sort-by=.lastTimestamp
```

If no `MigrationController` instance exists, create one through the installed Operator's Provided APIs. Wait for reconciliation, then check the routes again. Do not infer the route from an example hostname.

## Pods are not running

```bash
oc get pods -n openshift-migration -o wide
oc describe pod <pod-name> -n openshift-migration
oc logs <pod-name> -n openshift-migration --all-containers=true
oc get events -n openshift-migration --sort-by=.lastTimestamp
```

Check for image pull errors, missing resources, Operator/CSV status, RBAC, and events. Review logs for tokens, endpoints, names, and other confidential values before sharing them.

## Cluster or repository is unreachable

- Verify the API endpoint from the relevant cluster context.
- Test DNS, routing, egress/firewall rules, and certificate chains from the MTC components' network.
- Check token validity and permissions; issue a new token if the previous one expired.
- Verify the repository endpoint, bucket/container, region, and credential format against the supported storage configuration for the installed version.
- Do not permanently disable CA verification to work around a TLS error.

## `Upgrade request required` or Direct Volume Migration is stuck

This often indicates an interrupted upgrade/websocket connection or a proxy, firewall, or network-path problem. Check the network path and proxy between clusters for the selected Direct Volume mode. HTTP proxies that intercept TLS can be incompatible. Do not use broad firewall rules; determine the required connections for the installed version.

## Migration fails for persistent volumes

- Check PVC binding, target storage class, and capacity.
- If using snapshot copy, check snapshot support on source and target and provider/region requirements.
- For file-system copy, check permissions, volume mounts, and free space.
- Review logs, events, and MTC plan status; coordinate database consistency with the application team.
