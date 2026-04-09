## Citation & Evidence Design (Phase 4)

This system formats retrieved chunks into structured "Source blocks":

[Source 1]
Document: ...
Chunk ID: ...
Content: ...

### Why this matters

This creates a formal boundary between:
- retrieved enterprise knowledge
- generated model responses

Without this:
The model sees unstructured text → higher hallucination risk

With this:
The model sees explicit, auditable evidence units → better grounding and traceability

This is a key design principle for enterprise RAG systems.