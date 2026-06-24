# Jenkins Restart Runbook

## Incident Summary

Jenkins service is not responding.

## Possible Causes

- Service stopped
- Server reboot
- Configuration issue

## Resolution Steps

1. Login to server
2. Run:
   systemctl restart jenkins
3. Verify:
   systemctl status jenkins

## Validation Steps

- Open Jenkins UI
- Run a sample build

## Rollback Plan

Restart previous Jenkins service version.