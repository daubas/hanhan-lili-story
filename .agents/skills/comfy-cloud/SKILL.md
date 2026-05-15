---
name: comfy-cloud
description: Inspect Comfy Cloud account state through its HTTP API, including running jobs, recent jobs, assets, and saved workflows. Use when the user asks what is running in Comfy Cloud, what resources exist, which workflows are saved, or when Codex needs to reconcile workflow IDs with saved workflow filenames.
---

# Comfy Cloud

Use this skill for Comfy Cloud account inspection. Prefer the bundled script for routine reads so the API quirks stay consistent.

## Required environment

- Read the API key from `COMFY_API_KEY`.
- Send the key as `X-API-Key`, not as a bearer token, for the cloud REST API.
- Do not echo the key back to the user or persist it in project files.

## Mental model

- `jobs` are execution history, not saved workflows.
- Saved workflows live in user data under `workflows/`.
- The saved workflow filename is the human-facing name; the JSON file contains the internal workflow `id`.
- The same workflow may appear in jobs under `workflow_id` while being saved as a differently named file.

## Common tasks

Use [`scripts/comfy_cloud.py`](scripts/comfy_cloud.py):

```bash
python3 scripts/comfy_cloud.py running-jobs
python3 scripts/comfy_cloud.py jobs --limit 20
python3 scripts/comfy_cloud.py assets --limit 20
python3 scripts/comfy_cloud.py saved-workflows
python3 scripts/comfy_cloud.py workflow workflows/lihan_api_seedance2_0.json
```

## API map

- Running jobs: `GET /api/jobs?status=pending,in_progress`
- Recent jobs: `GET /api/jobs`
- Assets: `GET /api/assets`
- Saved workflow list: `GET /api/userdata?dir=workflows`
- Saved workflow file: `GET /api/userdata/{urlencoded path}`
  - Example path: `workflows%2Flihan_api_seedance2_0.json`

## Guardrails

- If `/api/jobs` shows only `workflow_id`, do not conclude that no saved workflow name exists.
- If the user asks for saved workflows, query `userdata?dir=workflows` first.
- If Comfy MCP itself returns a rollout / availability error, continue with the REST API when the user only needs account inspection.
- Validate any surprising result by checking both the saved workflow list and the workflow JSON `id`.
