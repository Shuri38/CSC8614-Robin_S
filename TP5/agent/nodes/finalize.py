# TP5/agent/nodes/finalize.py
import re
from typing import List

from TP5.agent.logger import log_event
from TP5.agent.state import AgentState

RE_CIT = re.compile(r"\[(doc_\d+)\]")


def _extract_citations(text: str) -> List[str]:
    return sorted(set(RE_CIT.findall(text or "")))


def finalize(state: AgentState) -> AgentState:
    log_event(state.run_id, "node_start", {"node": "finalize"})
    if not state.budget.can_step():
        log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "budget_exceeded"})
        return state

    state.budget.steps_used += 1

    intent = state.decision.intent

    if intent == "reply":
        cits = _extract_citations(state.draft_v1)
        state.final_kind = "reply"

        if cits:
            state.final_text = (
                state.draft_v1.strip()
                + "\n\nSources: "
                + " ".join(f"[{c}]" for c in cits)
            )
        else:
            # fallback minimal institutionnel
            state.final_text = (
                state.draft_v1.strip()
                or "Merci pour votre message. Nous revenons vers vous dès que possible."
            )

    elif intent == "ask_clarification":
        state.final_kind = "clarification"

        if state.draft_v1.strip():
            state.final_text = state.draft_v1.strip()
        else:
            # fallback : 1–3 questions précises
            state.final_text = (
                "Pouvez-vous préciser les points suivants afin que je puisse vous répondre correctement ?\n"
                "- Le contexte exact de votre demande\n"
                "- Le document ou la référence concernée (si applicable)\n"
                "- L’échéance éventuelle"
            )

    elif intent == "escalate":
        state.final_kind = "handoff"

        summary = (
            state.draft_v1.strip()
            or "Demande nécessitant une validation humaine."
        )

        # action mockée : HandoffPacket
        state.actions.append({
            "type": "handoff_packet",
            "run_id": state.run_id,
            "email_id": state.email_id,
            "summary": summary,
            "evidence_ids": [d.doc_id for d in state.evidence],
        })

        state.final_text = (
            "Votre demande nécessite une validation humaine. "
            "Elle a été transmise avec un résumé et les éléments disponibles."
        )

    else:
        state.final_kind = "ignore"
        state.final_text = "Message non actionnable. Aucune réponse requise."

    log_event(
        state.run_id,
        "node_end",
        {
            "node": "finalize",
            "status": "ok",
            "final_kind": state.final_kind,
        },
    )

    return state
