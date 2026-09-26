# Meridian-App

EECE503M Software Security coursework by Joud Senan, based on the Meridian Service Desk Django application. This repository contains lab scripts, ZAP scan reports, a threat model, and a parameterized-query fix for the ticket search.

## Run locally

Start Docker Desktop, then run from the repository root:

```powershell
docker compose -f lab/docker-compose.yml up --build
```

Open http://127.0.0.1:5001 in your browser or Burp Suite's built-in browser. See [lab/README.md](lab/README.md) for demo accounts and troubleshooting.

## Lab files

- [sqli_blind.py](sqli_blind.py) and [sqli_time.py](sqli_time.py): SQL-injection lab scripts using response-length and timing observations.
- [Threat model](zapout/threat_modeling.md): data flows, trust boundaries, and ranked STRIDE threats.
- [Initial ZAP report](zapout/report.html) and [rerun report](zapout/report-rerun.html): automated scan results; download and open the HTML files in a browser.
- [staff.py](src/helpdesk/views/staff.py): ticket search updated to pass SQL parameters separately from query text.

The scripts document testing of the vulnerable search; they are not expected to recover data after the fix.

**For local educational use only.** The application contains intentional vulnerabilities. Keep it bound to `127.0.0.1`, use only demo data, and do not deploy it publicly.

See [README.rst](README.rst) for the original project documentation.
