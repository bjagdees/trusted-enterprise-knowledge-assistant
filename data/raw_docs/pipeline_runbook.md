# Pipeline Failure Recovery

If a pipeline fails:

1. Check logs for error classification
2. Identify failed stage
3. Retry if transient failure
4. Escalate if schema mismatch
5. Validate downstream impact

All retries must follow idempotent execution principles.

If downstream certified datasets are impacted, incident escalation is mandatory.
