"""Hypothesizer — LLM-based plan scaffolding when Raphael is stuck."""
from __future__ import annotations
import json
import logging
import os
from typing import Optional
from raphael.models.engagement_state import EngagementState
from raphael.techniques import TECHNIQUE_REGISTRY, Technique

logger = logging.getLogger("raphael.hypothesizer")


class Hypothesizer:
    """
    When the planner is stuck and ModelRefiner found nothing,
    Hypothesizer sends the current constraint-vector profile to an LLM
    and asks for new approach suggestions.
    
    For Wave 2: uses the orchestrator API at :3800/tools/agent or
    falls back to heuristic rules if LLM unavailable.
    """

    async def hypothesize(self, state: EngagementState) -> Optional[dict]:
        """
        Generate candidate next steps based on the current profile.
        Returns an Action-like dict or None.
        
        Tries:
        1. Orchestrator API LLM endpoint
        2. Heuristic fallback rules
        """
        # Try the orchestrator API first
        result = await self._try_llm_api(state)
        if result:
            return result

        # Fallback: heuristic rules
        return self._heuristic_fallback(state)

    async def _try_llm_api(self, state: EngagementState) -> Optional[dict]:
        """Try calling the orchestrator's LLM endpoint for suggestions."""
        api_url = os.getenv("ORCHESTRATOR_URL", "http://localhost:3800")
        try:
            import httpx
            
            # Build a prompt with the current profile
            domain = state.target.domains.get("network")
            affs = list(domain.affordances) if domain else []
            cons = list(domain.constraints) if domain else []
            
            prompt = (
                f"Target: {state.target_address}\n"
                f"Current cycle: {state.current_cycle}\n"
                f"Available affordances: {affs}\n"
                f"Constraints: {cons}\n"
                f"Available techniques: {list(TECHNIQUE_REGISTRY.keys())}\n\n"
                f"The planner selected all viable techniques but none produced new information. "
                f"Given this profile, what technique should I try next? "
                f"Respond with a single technique name from the available list."
            )

            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{api_url}/agent/analyze",
                    json={"prompt": prompt, "context": "stuck_engagement"},
                    timeout=30,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    suggestion = data.get("technique") or data.get("suggestion") or data.get("response", "")
                    if suggestion and suggestion in TECHNIQUE_REGISTRY:
                        logger.info(f"Hypothesizer: LLM suggested {suggestion}")
                        return {
                            "action_type": "execute",
                            "technique": suggestion,
                            "reason": "LLM hypothesis from stuck state",
                        }
        except Exception as e:
            logger.debug(f"Hypothesizer LLM API failed: {e}")
        
        return None

    def _heuristic_fallback(self, state: EngagementState) -> Optional[dict]:
        """
        When LLM is unavailable, use heuristic rules to suggest next steps.
        Each suggestion is checked against technique blockers to avoid loops.
        """
        domain = state.target.domains.get("network")
        if not domain:
            return None

        affs = domain.affordances
        cons = domain.constraints

        def _is_not_blocked(tech_name: str) -> bool:
            """Check if a technique's blockers prevent it from being useful."""
            tech = TECHNIQUE_REGISTRY.get(tech_name)
            if not tech:
                return False
            return not any(b in cons for b in tech.blockers)

        # Rule 1: If HTTP is detected but no tech fingerprint was done
        if ("http_service" in affs or "https_service" in affs):
            if not any(a.startswith("tech:") for a in affs) and "tech_stack" not in affs:
                if "tech_fingerprint" not in state.target.failed_techniques and _is_not_blocked("tech_fingerprint"):
                    return {
                        "action_type": "execute",
                        "technique": "tech_fingerprint",
                        "reason": "heuristic: HTTP detected, unknown tech stack",
                    }

        # Rule 2: If we found open ports but no service scan attempted
        if "open_ports" in affs and "service_versions" not in affs:
            if "service_scan" not in state.target.failed_techniques and _is_not_blocked("service_scan"):
                return {
                    "action_type": "execute",
                    "technique": "service_scan",
                    "reason": "heuristic: open ports, unknown services",
                }

        # Rule 3: If domain name (not IP) and no DNS records checked
        import re
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', state.target_address):
            if "dns_records_resolved" not in affs:
                if "dns_lookup" not in state.target.failed_techniques and _is_not_blocked("dns_lookup"):
                    return {
                        "action_type": "execute",
                        "technique": "dns_lookup",
                        "reason": "heuristic: domain target, no DNS records",
                    }

        # Rule 4: If SMB but no null session or user enum tried
        if "smb_service" in affs:
            if "smb_null_session_works" not in affs and "smb_null_session" not in state.target.failed_techniques and _is_not_blocked("smb_null_session"):
                return {
                    "action_type": "execute",
                    "technique": "smb_null_session",
                    "reason": "heuristic: SMB detected, try null session",
                }

        # Rule 5: If no open ports found, try DNS recon instead
        if "no_open_ports" in cons:
            if "dns_lookup" not in state.target.failed_techniques and _is_not_blocked("dns_lookup"):
                return {
                    "action_type": "execute",
                    "technique": "dns_lookup",
                    "reason": "heuristic: no open ports, try DNS recon",
                }

        # Rule 6: HTTP detected but WAF not checked
        if "http_service" in affs and "waf_detected" not in affs and "no_waf_detected" not in cons:
            if "waf_detect" not in state.target.failed_techniques and _is_not_blocked("waf_detect"):
                return {
                    "action_type": "execute",
                    "technique": "waf_detect",
                    "reason": "heuristic: HTTP detected, unknown WAF status",
                }

        return None


# Singleton
_hypothesizer: Optional[Hypothesizer] = None

def get_hypothesizer() -> Hypothesizer:
    global _hypothesizer
    if _hypothesizer is None:
        _hypothesizer = Hypothesizer()
    return _hypothesizer
