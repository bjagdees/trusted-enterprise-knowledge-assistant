from typing import List, Dict, Any


def assess_retrieval_confidence(retrieved_docs: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Estimate trust level based on retrieved evidence strength.

    WHY THIS EXISTS:
    In enterprise RAG, trust should depend not only on model fluency,
    but also on how much supporting evidence was retrieved.

    CURRENT HEURISTICS:
    - No sources => Low
    - Few / short sources => Low
    - Moderate evidence => Medium
    - Multiple substantial sources => High

    This is intentionally simple for Phase 4 and can later evolve into:
    - retrieval scoring
    - contradiction detection
    - groundedness evaluation
    """
    num_sources = len(retrieved_docs)

    if num_sources == 0:
        return {
            "confidence": "Low",
            "reason": "No supporting sources were retrieved."
        }

    total_chars = sum(len(doc.get("text", "")) for doc in retrieved_docs)

    if num_sources >= 3 and total_chars > 1000:
        return {
            "confidence": "High",
            "reason": "Multiple substantial supporting sources were retrieved."
        }

    if num_sources >= 2 and total_chars > 500:
        return {
            "confidence": "Medium",
            "reason": "Some supporting evidence was retrieved, but coverage may be partial."
        }

    return {
        "confidence": "Low",
        "reason": "Retrieved evidence is limited or shallow."
    }


def build_trust_header(retrieved_docs: List[Dict[str, Any]]) -> str:
    """
    Build a human-readable trust summary for final answer output.
    """
    assessment = assess_retrieval_confidence(retrieved_docs)

    return (
        "Trust Summary:\n"
        f"- Retrieval Confidence: {assessment['confidence']}\n"
        f"- Reason: {assessment['reason']}\n"
    )