
---

# Runbook Agent

## File: `jenkins_runbook.md`

```markdown
# Jenkins Troubleshooting Runbook

## Problem

Jenkins UI is inaccessible.

## Resolution Steps

1. Check service status

```bash
sudo systemctl status Jenkins

Restart Jenkins
sudo systemctl restart jenkins
Check logs
sudo journalctl -u jenkins -n 100
Verify port 8080
sudo netstat -tulpn | grep 8080