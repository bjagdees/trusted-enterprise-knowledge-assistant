# Orchestration Standards

All workflows must:
- Support retries
- Implement checkpointing
- Maintain lineage tracking
- Log execution metadata

DAG-based orchestration is recommended.

All workflow failures must be traceable through observability systems.