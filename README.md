# Raphael V3 — Autonomous Cognitive Offensive AI Platform

A self-growing offensive AI organism that autonomously probes targets, builds constraint-vector profiles, plans via greedy selection, acquires capabilities in parallel, and rewrites its own decision logic through post-engagement reflection.

## Architecture

Raphael V3 is a **cognitive organism**, not a toolchain. Organs run at different cadences, communicate through shared state, and a reflection loop rewrites decision logic.

```
┌──────────────────────────────────────────────────────────────────────┐
│                        RAPHAEL COGNITIVE ORGANISM                    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │                    raphael/ (THE BRAIN)                     │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │      │
│  │  │ Planner  │  │ Executor │  │ Model    │  │ Cerebellum│  │      │
│  │  │ (cortex) │  │          │  │ Refiner  │  │ (errors)  │  │      │
│  │  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │      │
│  │  │Techniques│  │Blackboard│  │ EventBus │  │ Memory    │  │      │
│  │  │ (26 reg) │  │ (shared) │  │ (pipeline│  │(hippocampus│  │      │
│  │  │          │  │          │  │  events) │  │ + cortex) │  │      │
│  │  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │      │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────────────┐  │      │
│  │  │ VHOST    │  │ Exploit  │  │ Verification Loop       │  │      │
│  │  │ Enum     │  │ Factory  │  │ (TCP/HTTP/DNS)          │  │      │
│  │  └──────────┘  └──────────┘  └─────────────────────────┘  │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │               INFRASTRUCTURE (orchestrator/)                │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │      │
│  │  │Harvester │  │ Mesh     │  │Privesc   │  │Propagation│  │      │
│  │  │(CVE feed)│  │(P2P net) │  │(27 LPE)  │  │(lateral)  │  │      │
│  │  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │      │
│  │  │Weaponizer│  │Social    │  │Survivabil│  │TTP Playbk │  │      │
│  │  │(C/Go/Rust)│ │(phish)   │  │(kill sw) │  │(6 chains) │  │      │
│  │  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │              IMPLANT (agent/)                              │      │
│  │  syscall (Hell's Gate/Halo's Gate) | injection | stealth   │      │
│  │  credtheft | exfil | persistence | lateral | cleanup       │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │              SERVICES                                       │      │
│  │  cli/  sword/  c2-server/  cai-service/  cloak-service/    │      │
│  │  kali-tools/  phishing/  recon-pipeline/  mcp-hub/         │      │
│  │  sliver/  mhddos-service/  bridge/                         │      │
│  └────────────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────────────┘
```

## The Cognitive Organism (raphael/)

The brain operates as a continuous loop:

### Cycle

1. **Planner** (`cortex/planner.py`) — selects next technique using:
   - TargetModel filter (constraints + affordances)
   - CapabilityModel filter (owned vs gaps)
   - Memory prior ranking (recon=0.6, exploit=0.3 default)
   - Exhaustion tracking (skips techniques that return no new info)
   - Stuck detection → parallel ModelRefiner + Hypothesizer escape hatches

2. **Executor** (`executor/`) — runs techniques via:
   - KaliBridge (HTTP :3800 or subprocess fallback)
   - ProtocolInferenceEngine (enriches domain state from ports/services)
   - Cerebellum error diagnosis (19 error patterns)
   - SpinalReflex thermoregulator (1 Hz, inhibits at detection risk >0.8)

3. **Absorb** (`models/target_model.py`) — integrates results:
   - Per-field diff checking (constraints, affordances, unknowns)
   - Returns False when nothing changed (prevents infinite loops)
   - Negative cache with resurrection (dead technique revives when profile changes)

4. **Reflection** (`cognitive/`) — post-engagement:
   - ModelRefiner updates target/capability models
   - Hypothesizer generates new technique affordances
   - SelfModificationEngine rewrites decision logic
   - Episodic memory stored in Hippocampus

### 26 Registered Techniques

| Type | Technique | Purpose |
|------|-----------|---------|
| Recon | `port_scan` | Full TCP port scan |
| Recon | `service_scan` | Service version detection |
| Recon | `dns_lookup` | DNS record enumeration |
| Recon | `vhost_enum` | Virtual host discovery (DNS brute, CT logs, SSL SAN) |
| Recon | `subdomain_enum` | Subdomain discovery |
| Recon | `waf_detect` | WAF fingerprinting |
| Recon | `tech_detect` | Technology stack identification |
| Recon | `directory_brute` | Directory/file busting |
| Recon | `parameter_fuzz` | Parameter fuzzing |
| Recon | `ad1_xor_sweep` | Full-image XOR sweep with shifted-phase key derivation |
| Exploit | `sqli_check` | SQL injection detection |
| Exploit | `xss_check` | XSS detection |
| Exploit | `ssrf_check` | SSRF detection |
| Exploit | `cmdi_check` | Command injection detection |
| Exploit | `lfi_check` | Local file inclusion |
| Exploit | `ssti_check` | Server-side template injection |
| Exploit | `open_redirect` | Open redirect detection |
| Exploit | `jwt_crack` | JWT weakness testing |
| Exploit | `cors_check` | CORS misconfiguration |
| Exploit | `http_verbs` | HTTP method abuse |
| Exploit | `auth_bypass` | Authentication bypass |
| Exploit | `nosqli_check` | NoSQL injection |
| Pipeline | `vhost_enum` | 5-enumerator vhost discovery pipeline |
| Pipeline | `exploit_factory` | CVE-based payload generation (5 CVEs, 8 templates) |
| Pipeline | `verification_loop` | 3-channel verification (TCP/HTTP/DNS) |
| Custom | `ad1_xor_sweep` | Forensic image XOR decryption |

## Infrastructure (orchestrator/)

| Module | Description |
|--------|-------------|
| `harvester/` | CVE feed ingestion, GitHub PoC scraping, technique extraction |
| `mesh/` | P2P gossip protocol, encrypted routing, peer discovery |
| `privesc/` | 27 LPE vectors, auto-updating GTFOBins/LOLBAS |
| `propagation/` | Subnet discovery, TCP scanning, credential reuse |
| `social/` | Target recon, LLM lure generation, credential harvesting |
| `survivability/` | Snapshots, integrity checks, kill switches, auto-update |
| `weaponizer/` | C/Go/Rust compilation, UPX packing, AES encryption |
| `ttp_playbook/` | 6 adversary-profiled attack chains |

## Implant (agent/)

Multi-platform implant with OPSEC-hardened modules:

| Module | Techniques |
|--------|-----------|
| `syscall.py` | Hell's Gate + Halo's Gate indirect syscall resolution |
| `inject.py` | Process injection via indirect syscalls, PPID spoofing |
| `stealth.py` | HWBP AMSI bypass, ETW-TI suppression, sleep mask, stack spoofing |
| `credtheft.py` | Chrome Linux key decryption, LSASS, SAM, browser harvest |
| `exfil.py` | DNS tunnel, HTTPS camouflage, ICMP tunnel, cloud storage |
| `persistence.py` | systemd, cron, LD_PRELOAD, Registry, WMI, Scheduled Tasks |
| `lateral.py` | SSH, WMI, PSExec, SMB, WinRM, Docker, MSSQL |
| `cleanup.py` | Log wiping (journald, auditd, wevtutil, macOS log) |

## CLI (cli/)

TypeScript/Bun-based CLI with OpenClaude integration:

- 9 command dialogs: autonomous, brain, c2, community, debate, deep-research, exploit, harvester, kali
- 3 personas: stealth, aggressive (z3r0), full-spectrum (ghost)
- Raphael orchestrator provider with SSE streaming
- 6 pentest tools: nmap, sqlmap, bloodhound, metasploit, crackmapexec, chisel

## Services

| Service | Port | Description |
|---------|------|-------------|
| `cai-service/` | 3201 | LLM AI orchestration (Ollama/OpenAI) |
| `mhddos-service/` | 3301 | DDoS simulation engine |
| `cloak-service/` | 3401 | Traffic cloaking & proxy chaining (Tor) |
| `c2-server/` | 3501 | C2 implant management (Sliver) |
| `phishing/` | 3502 | Phishing campaign manager (Gophish) |
| `recon-pipeline/` | 3503 | Automated reconnaissance (Shodan/Spiderfoot) |
| `sword/` | 3600 | Main orchestration engine |
| `kali-tools/` | 3800 | Kali toolset wrapper (netexec, nmap, etc.) |
| `mcp-hub/` | - | MCP server with HMAC auth |
| `bridge/` | - | Python↔TypeScript bridge |

## Quick Start

```bash
# Clone and configure
cp .env.example .env
# Edit .env — set at minimum: TOR_CONTROL_PASS, API_KEY

# Build and start
docker compose build
docker compose up -d

# Check health
curl http://localhost:3900/health

# Or run the brain directly (Python 3.11+)
pip install -r requirements.txt
python -m raphael.main --target <target>
```

## Operational Security

- **Do not run on personal/work machines.** Raphael modifies network config, installs kernel modules, and generates traffic that triggers alarms.
- **Default credentials are placeholders.** Validate with `scripts/validate_env.py`.
- **CDN fronting and TLS SNI spoofing** use placeholder domains — configure your own fronting infra.
- **Agent communications** are encrypted. Set `EGRESS_VERIFY_CERT=true` for MITM protection.
- **Logs** capture C2 traffic at DEBUG level. Commands matching `REDACT_PATTERNS` are redacted.

## Key Design Decisions

- **Cognitive organism, not a tool** — organs run at different cadences, communicate through shared state, reflection loop rewrites decision logic
- **Two technique classes** — recon (generates affordances, prior 0.6) and exploit (requires affordances, prior 0.3)
- **Memory is episodic** — full narratives via case-based reasoning, not just semantic priors
- **Stuck handling** — parallel ModelRefiner + Hypothesizer via asyncio.wait(FIRST_COMPLETED)
- **Exhaustion tracking** — `_exhaustion_count` per technique, threshold 2 consecutive no-change runs
- **Negative cache** — technique stays dead until profile changes relevant to its blockers
- **Brain is never idle** — when no technique executable → ModelRefiner ∥ Hypothesizer → heuristic fallback → report stuck

## Legal & Ethical Use

This software is intended for **authorized security testing only**. You must:
1. Have written permission from the target system owner
2. Comply with all applicable laws (CFAA, Computer Misuse Act, etc.)
3. Never use against systems you do not own or have explicit permission to test
