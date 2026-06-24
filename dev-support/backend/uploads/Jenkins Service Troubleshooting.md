# Jenkins Service Troubleshooting Runbook

## Overview

This runbook provides troubleshooting steps for resolving common Jenkins service issues.

---

## Problem

Jenkins web interface is inaccessible.

---

## Symptoms

* Jenkins dashboard does not load.
* Browser displays "Connection Refused".
* Port `8080` is not reachable.
* CI/CD pipelines are not running.

---

## Prerequisites

* SSH access to the Jenkins server.
* Sudo privileges.

---

## Step 1: Check Jenkins Service Status

Run the following command:

```bash
sudo systemctl status jenkins
```

Expected output:

```bash
Active: active (running)
```

If the service is inactive, proceed to Step 2.

---

## Step 2: Restart Jenkins Service

```bash
sudo systemctl restart jenkins
```

Verify the status again:

```bash
sudo systemctl status jenkins
```

---

## Step 3: Check Jenkins Logs

View the last 100 log entries:

```bash
sudo journalctl -u jenkins -n 100
```

Common errors:

* Java OutOfMemoryError
* Port already in use
* Plugin loading failure

---

## Step 4: Verify Port Availability

Check whether Jenkins is listening on port 8080:

```bash
sudo netstat -tulpn | grep 8080
```

or

```bash
sudo ss -tulpn | grep 8080
```

Expected output:

```bash
tcp LISTEN 0 50 *:8080
```

---

## Step 5: Validate Java Installation

Jenkins requires Java.

Check Java version:

```bash
java -version
```

Expected:

```bash
openjdk version "17"
```

---

## Step 6: Restart the Server (Optional)

If Jenkins still fails:

```bash
sudo reboot
```

---

## Troubleshooting Checklist

| Check                       | Status |
| --------------------------- | ------ |
| Jenkins Service Running     | ☐      |
| Port 8080 Accessible        | ☐      |
| Java Installed              | ☐      |
| Logs Reviewed               | ☐      |
| Plugins Loaded Successfully | ☐      |

---

## Escalation

Escalate to the DevOps team if:

* Jenkins fails repeatedly after restart.
* Persistent plugin failures occur.
* JVM crashes continue.

---

## Related Commands

```bash
sudo systemctl start jenkins
sudo systemctl stop jenkins
sudo systemctl restart jenkins
sudo systemctl status jenkins
sudo journalctl -u jenkins
```
