# Invite-only hosted pilot

This milestone prepares one shared HTTPS address for at most ten invited accounts. It preserves the local installation. It is not a public self-service or paid product, and no cloud account or charge is created by this repository.

## Decision

Use one Render Docker web service plus a 2 GB persistent disk for the first invited pilot. Serve the React build and FastAPI API from the same origin. Retain one process and SQLite; save private photos on the attached disk. This is a deliberate small-pilot topology: it must not be horizontally scaled or started with several workers. Deployments briefly interrupt the service; in-flight model requests remain failed/unknown and never retry automatically.

Render officially supports FastAPI and provides an `onrender.com` address. Its default filesystem is ephemeral; persistent disks require a paid service and only preserve files under the mount path. Review current service and disk charges before creating the service. A purchased domain is optional. Sources: [FastAPI on Render](https://render.com/docs/deploy-fastapi), [persistent disks and limitations](https://render.com/docs/disks), [current pricing](https://render.com/pricing).

Why not connect every tool immediately:

- **GitHub Actions:** implemented now for isolated tests, frontend build and a real container persistence smoke test. Read-only token permissions, pinned action revisions, no model keys or private notes.
- **Supabase:** a good later option for managed identity, Postgres and private object storage. Adopting it requires explicit identity-to-record mapping, RLS policies and storage policies with cross-account tests. A connection string alone would not supply those guarantees. [Storage authorization](https://supabase.com/docs/guides/storage/security/access-control).
- **Vercel:** can host a frontend and Python functions, but this process currently owns local files and a model lock. Moving it to functions requires external storage and a durable job coordinator first. [Python runtime](https://vercel.com/docs/functions/runtimes/python), [function limits](https://vercel.com/docs/functions/limitations).
- **Stripe:** deferred until the teaching pilot and billing unit are settled. The later phase needs sandbox subscription/webhook tests and a separate usage ledger. No payment form or live charge is present. [Stripe testing](https://docs.stripe.com/testing).

## User handoff: login and billing

1. Sign in or register at https://dashboard.render.com/. Account terms, GitHub access and payment confirmation are the owner's actions.
2. After the deployment PR passes checks and is approved, create a **Blueprint** from `sh1ranY/stem-study-vault`, selecting the branch containing `render.yaml`. Inspect the proposed **0.5 CPU / 512 MB web service (`0.5c-512mb`) + 2 GB disk, Frankfurt** and its displayed cost. Do not confirm if that cost is not acceptable.
3. Set `OPENAI_API_KEY` privately in Render if using AI. Leave it empty to use manual photo transcription and offline checks first. `STUDIO_VISION_MODEL` must name a model available to this key. Never paste secrets in chat, GitHub, frontend variables or screenshots.
4. Render supplies `RENDER_EXTERNAL_URL`; hosted startup checks that it is an exact HTTPS origin. The Blueprint generates `STUDIO_BOOTSTRAP_TOKEN`. Copy that value privately from the service environment.
5. Visit the service address. Create the first owner account with that setup token and your own password. Subsequent accounts require one-use invitations valid for seven days. The default pilot cap is ten accounts; model calls default to ten per account per UTC day. Each account has a 100 MB photo budget. These are usage limits, not a guaranteed monetary cap.
6. Verify HTTPS, owner login, English/Chinese, photo upload/manual confirmation, export and a service restart before inviting anyone. Create a separate learner account and check record isolation. AI quality still needs real handwriting evaluation.
7. Share the site address and one invitation with each learner yourself. The agent does not send invitations to other people.

Initial hosted content is a distributable three-topic authored sample. It does **not** upload this computer's private Obsidian vault, university documents, photos, API keys or learner database. Importing the full private course is a separate explicit operation after choosing what may be shared with this cohort. The importer supports custom paths; no computer filesystem is reachable from the hosted app.

## Runtime boundary

`STUDIO_DEPLOYMENT=local` remains the default and accepts only loopback origins. `hosted` requires an exact HTTPS origin, an absolute persistent data path and a setup token of at least 32 characters. Startup fails on missing configuration. Hosted cookies are Secure/HttpOnly/SameSite=Strict, legacy APIs and API docs are disabled, requests have body limits, and sign-in has per-name and aggregate limits. First-owner registration is protected by the setup token. User evidence and files are checked by owner on every request.

The Docker entrypoint initializes the disk directory, drops to UID 10001, then starts exactly one process. Never run `uvicorn --workers 2` or scale instances with this storage layout. The initial setup token remains an environment secret for recovery; it does not authorize later account registration without an invitation.

When adding a custom domain, set `STUDIO_PUBLIC_ORIGIN` to that exact HTTPS address and restart. There is intentionally no wildcard origin or host.

## Backup and recovery drill

The backup tool is for SQLite installations. It creates a SQLite-consistent snapshot, includes retained photos and course assets, checks referenced files, and records checksums. Run during a quiet period with no imports/deletions or in-flight model calls. If files change or disappear, the backup fails rather than silently omitting them. Archives include private student records and password hashes: transfer them through the owner's private channel, keep access restricted, and never put them in Git or a public bucket.

From the service's shell (the disk is mounted at runtime):

```sh
python -m backend.backup create --data /var/data/study-studio --output /tmp/study-backup.zip
```

Download the archive using the provider's authenticated file-transfer mechanism. `/tmp` is temporary: it is not the durable backup destination. A backup on the same disk alone is not disaster recovery.

Restore into a **new directory** first; the tool refuses to overwrite live data, verifies checksums and SQLite integrity, rewrites local photo/asset paths and invalidates old login sessions:

```sh
python -m backend.backup restore --archive /tmp/study-backup.zip --destination /var/data/restored-studio
```

Point `STUDIO_DATA_DIR` at the restored directory and ensure UID 10001 owns restored files before restarting. Sign in again, open a photo, export a record and compare expected counts before directing learners back. If a custom `STUDIO_DATABASE_URL` was set, remove or update it to match the restored path. Provider disk snapshots are not a substitute for this tested database/file backup. [Render recovery considerations](https://render.com/docs/disks#restoring-a-custom-database).

## Next architecture milestone

Before broader public use: hosted identity and account recovery, a relational evidence schema plus database policies, private object storage, durable jobs with job status and cancellation, per-task budget accounting, automated off-host backups and restore drills, consented pilot feedback, and real handwriting/teaching evaluation. Preserve stable concept IDs, content versions, answer-time language, and the distinction between guided and independent evidence throughout that migration.
