# ---------------------------------------------------------------------------
# Pipeline techniques (Wave 3)
# ---------------------------------------------------------------------------
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

TECHNIQUE_REGISTRY: Dict[str, "Technique"] = {}


@dataclass
class Technique:
    name: str
    category: str
    prerequisites: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    outcome: str = ""
    provides: List[str] = field(default_factory=list)
    tool: str = ""
    tool_args_template: str = ""
    timeout: int = 300
    stealth_score: float = 0.5
    required_capabilities: List[str] = field(default_factory=list)
    parser: str = "raw"
    type: str = "recon"
    cost: float = 1.0
    detection_risk: float = 0.1
    provides_affordances: List[str] = field(default_factory=list)


def register(technique: Technique) -> None:
    TECHNIQUE_REGISTRY[technique.name] = technique


def get_technique(name: str) -> Optional[Technique]:
    return TECHNIQUE_REGISTRY.get(name)


def list_techniques() -> List[Technique]:
    return list(TECHNIQUE_REGISTRY.values())


def list_by_category(category: str) -> List[Technique]:
    return [t for t in TECHNIQUE_REGISTRY.values() if t.category == category]


# ---------------------------------------------------------------------------
# Register Wave 1/2 basic recon techniques
# ---------------------------------------------------------------------------
register(Technique(
    name="port_scan",
    category="recon",
    prerequisites=[],
    blockers=["all_ports_filtered"],
    outcome="Full TCP port scan to discover open ports",
    provides=["open_ports", "port_list"],
    tool="nmap",
    tool_args_template="-p- -T3 --min-rate 500 {target}",
    timeout=300,
    stealth_score=0.3,
    required_capabilities=[],
    parser="nmap_port_list",
    type="recon",
    cost=1.0,
    detection_risk=0.3,
    provides_affordances=["open_ports"],
))

register(Technique(
    name="service_scan",
    category="recon",
    prerequisites=["open_ports"],
    blockers=["no_open_ports", "no_detectable_services"],
    outcome="Service version detection on discovered open ports",
    provides=["service_versions", "os_detected"],
    tool="nmap",
    tool_args_template="-sV -O -T3 -p{ports} {target}",
    timeout=300,
    stealth_score=0.4,
    required_capabilities=[],
    parser="nmap_service_version",
    type="recon",
    cost=1.5,
    detection_risk=0.4,
    provides_affordances=["service_versions"],
))

register(Technique(
    name="dns_lookup",
    category="recon",
    prerequisites=[],
    blockers=["no_dns_for_ip_target", "dns_lookup_returned_nothing"],
    outcome="DNS enumeration and record resolution",
    provides=["dns_records_resolved"],
    tool="dig",
    tool_args_template="+noall +answer ANY {target}",
    timeout=10,
    stealth_score=0.8,
    required_capabilities=[],
    parser="dns_raw",
    type="recon",
    cost=0.5,
    detection_risk=0.1,
    provides_affordances=["dns_records_resolved"],
))

# ---------------------------------------------------------------------------
# Register Wave 3 techniques
# ---------------------------------------------------------------------------
register(Technique(
    name="vhost_enum",
    category="recon",
    prerequisites=["http_service"],
    blockers=["waf_blocking", "no_http_response"],
    outcome="Enumerates virtual hosts via DNS brute force, CT logs, Host header fuzzing, SSL SAN parsing, and recursive enumeration",
    provides=["vhosts_discovered", "vhost_count"],
    tool="python3",
    tool_args_template="-m raphael.techniques.vhost_enum {target}",
    timeout=300,
    stealth_score=0.6,
    required_capabilities=["raphael_vhost_enum"],
    parser="vhost_enum",
    type="recon",
    cost=1.5,
    detection_risk=0.3,
    provides_affordances=["vhosts_discovered", "vhost_count"],
))

register(Technique(
    name="exploit_factory",
    category="exploit",
    prerequisites=["vhosts_discovered"],
    blockers=[],
    outcome="Generates exploit payloads from CVE database and templates for discovered vhosts",
    provides=["exploit_payloads", "exploit_deliveries"],
    tool="python3",
    tool_args_template="-m raphael.exploit_factory {target} --auto-deliver --tech-stack '{{\"nginx\":\"1.24\"}}'",
    timeout=600,
    stealth_score=0.4,
    required_capabilities=["raphael_exploit_factory"],
    parser="exploit_factory",
    type="exploit",
    cost=2.0,
    detection_risk=0.5,
    provides_affordances=["exploit_payloads", "exploit_deliveries"],
))

register(Technique(
    name="verification_loop",
    category="exploit",
    prerequisites=["exploit_delivered"],
    blockers=[],
    outcome="Verifies exploit delivery via TCP listener, HTTP canary, and DNS callback channels with fallback chain",
    provides=["exploit_verified", "shell_access", "flag_captured"],
    tool="python3",
    tool_args_template="-m raphael.verifier {target}",
    timeout=300,
    stealth_score=0.5,
    required_capabilities=["raphael_verifier"],
    parser="verification_loop",
    type="exploit",
    cost=1.0,
    detection_risk=0.3,
    provides_affordances=["exploit_verified", "shell_access", "flag_captured"],
))