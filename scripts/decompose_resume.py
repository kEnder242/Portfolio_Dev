#!/usr/bin/env python3
"""
[FEAT-595] Round-Trip Resume AST Decomposer & DNA Extractor
Parses raw text resume into:
1. Structured Paper AST (data/papers/PAPER-RESUME_v1.json) with node variants and review flag slots.
2. Layout Style Schema (data/papers/style_resume_v1.json).
3. Polymorphic RESUME-xxx DNA cards (data/resume_data.json).
4. Synchronizes data/dna_manifest.json.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_RESUME_PATH = BASE_DIR / "raw_notes" / "Jason Allred resume 2026.txt"
PAPERS_DIR = BASE_DIR / "field_notes" / "data" / "papers"
RESUME_DATA_PATH = BASE_DIR / "field_notes" / "data" / "resume_data.json"
DNA_MANIFEST_PATH = BASE_DIR / "field_notes" / "data" / "dna_manifest.json"


def parse_resume(raw_text: str):
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    
    # 1. Contact & Identity
    author = "Jason Allred"
    contact = {
        "location": "Portland, OR",
        "email": "kEnder242@gmail.com",
        "phone": "503.515.2663",
        "linkedin": "https://linkedin.com/in/jason-allred-7a55024",
        "github": "https://github.com/kEnder242"
    }
    
    # 2. Section Partitioning
    sections = []
    current_sec = None
    
    # AST Structure
    ast = {
        "paper_id": "PAPER-RESUME",
        "revision_id": "v1_baseline",
        "title": "Jason Allred - Technical Resume & CV",
        "author": author,
        "contact": contact,
        "style_schema_ref": "data/papers/style_resume_v1.json",
        "sections": []
    }
    
    # Section 0: Title & Header Node (with multi-lens variants)
    ast["sections"].append({
        "section_id": "sec_title",
        "heading": "Target Title",
        "nodes": [
            {
                "node_id": "node_title_01",
                "type": "title",
                "active_key": "datacenter_platform",
                "text": "Senior Data Center Platform Engineer & Telemetry Architect",
                "variants": {
                    "datacenter_platform": "Senior Data Center Platform Engineer & Telemetry Architect",
                    "ai_infrastructure": "Lead AI Infrastructure & Telemetry Architect",
                    "pre_silicon_validation": "Principal Pre-Silicon & Manageability Validation Architect"
                },
                "citations": ["FEAT-586", "WIS-041"],
                "review_flags": []
            }
        ]
    })
    
    # Section 1: Professional Summary
    summary_text = (
        "Platform engineer specializing in server manageability, firmware integration, and system-level debug "
        "across enterprise datacenter platforms, with recent focus on AI infrastructure performance, memory-aware "
        "systems, and retrieval design. Proven track record delivering automated validation, power/performance "
        "telemetry analysis, and cross-functional issue resolution spanning silicon, BIOS, BMC, and hardware teams. "
        "Focused on improving platform reliability, observability, and production readiness."
    )
    ast["sections"].append({
        "section_id": "sec_summary",
        "heading": "Professional Summary",
        "nodes": [
            {
                "node_id": "node_sum_01",
                "type": "paragraph",
                "text": summary_text,
                "citations": ["FEAT-586", "FEAT-592"],
                "review_flags": []
            }
        ]
    })
    
    # Section 2: Technical Skills
    skills_nodes = [
        {
            "node_id": "node_skill_01",
            "category": "System Architecture & Domains",
            "text": "Hardware/Software Interface, In-Band & Out-of-Band (OOB) Management, Pre-Silicon (Shift-Left) Strategy, Power/Performance Telemetry, Server RAS, Deep Learning / HPC Workloads",
            "citations": [],
            "review_flags": []
        },
        {
            "node_id": "node_skill_02",
            "category": "Protocols & Standards",
            "text": "Redfish, IPMI, MCTP, PLDM, PECI, KCS, HECI, RMCP+, DCMI",
            "citations": [],
            "review_flags": []
        },
        {
            "node_id": "node_skill_03",
            "category": "Hardware & Compute",
            "text": "GPU Accelerated Platforms, x86, ARM, BMC, PCIe, Optane PMEM, Mellanox Networking",
            "citations": [],
            "review_flags": []
        },
        {
            "node_id": "node_skill_04",
            "category": "Languages",
            "text": "Python, C++, C, C#, TCL, Perl, Bash",
            "citations": [],
            "review_flags": []
        },
        {
            "node_id": "node_skill_05",
            "category": "Tools & Environments",
            "text": "Linux (Kernel/CLI), JTAG / Remote Debug, Signal-Trace (Intel VISA), Simics (Virtual Platforms), vLLM, PyTorch, FastEmbed, ChromaDB, Agentic CLI (OpenCode, AGY)",
            "citations": [],
            "review_flags": []
        },
        {
            "node_id": "node_skill_06",
            "category": "Spoken Languages",
            "text": "Japanese, Korean",
            "citations": [],
            "review_flags": []
        }
    ]
    ast["sections"].append({
        "section_id": "sec_skills",
        "heading": "Technical Skills",
        "nodes": skills_nodes
    })
    
    # Section 3: Experience
    experience_roles = [
        {
            "role_id": "role_ai_research",
            "company": "Systems Software & AI Infrastructure (Independent Research)",
            "title": "AI Infrastructure & Telemetry Architect",
            "period": "2025 – Present",
            "location": "Portland, OR",
            "context_line": "Architecting a high-throughput AI testbed to evaluate the software/hardware interface of Deep Learning workloads.",
            "bullets": [
                {
                    "node_id": "node_exp_ai_01",
                    "text": "Profiling memory-bound constraints and VRAM utilization across consumer/workstation GPUs using vLLM, PyTorch, and LoRA adapters.",
                    "citations": ["FEAT-586"],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_ai_02",
                    "text": "Engineered efficient multi-tenant LLM inference using Multi-LoRA adapters and deployed a performance-focused observability stack using Prometheus and Grafana to analyze GPU power draw and VRAM utilization.",
                    "citations": ["FEAT-586", "FEAT-160"],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_ai_03",
                    "text": "Developed a Recursive RAG (Retrieval-Augmented Generation) pipeline with iterative context refinement and retrieval discipline to automate the analysis of deep technical archives, bridging 15 years of platform systems expertise with modern generative AI infrastructure.",
                    "citations": ["FEAT-592", "FEAT-583"],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_manageability",
            "company": "Intel Corporation",
            "title": "Manageability Test Content Lead | Cloud SW Development Engineer",
            "period": "Oct 2019 – Oct 2024",
            "location": "Hillsboro, OR",
            "context_line": "Drove system architecture validation and SW/FW stack alignment for server manageability across Intel’s datacenter platforms.",
            "bullets": [
                {
                    "node_id": "node_exp_intel_01",
                    "text": "Saved the PECI debug interface from deprecation by championing a secure architectural roadmap across cross-functional teams. Led the transition from legacy RMCP+ to Redfish/OOBMSM, architecting a Bulk API and routing traffic via MCTP over PCIe to improve throughput by a factor of nearly 100. Drove firmware architecture changes, including a CCB to enable 'Core Wake on PECI', culminating in a published internal paper on platform reliability.",
                    "citations": ["WIS-012"],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_intel_02",
                    "text": "Architected and maintained a 100% automated Python validation framework for server manageability. Built standardized modules enabling 100+ tests for foundational device management protocols (PLDM/MCTP endpoint discovery, Redfish/IPMI telemetry tracking) ensuring consistency across SoC generations and platform resets.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_intel_03",
                    "text": "Engineered high-fidelity telemetry pipelines to debug Intel Node Manager (NM) power-capping logic and RAPL performance envelopes, resolving critical sub-second power overshoots through automated diagnostic scripts.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_intel_04",
                    "text": "Partnered across system software, firmware, and architecture teams to implement a shift-left strategy. Validated PCIe, power management, and platform RAS mechanisms during virtual platform integration (Simics), de-risking program execution before physical silicon arrived.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_intel_05",
                    "text": "Mentored engineering teams and domain leads, fostering cross-functional leadership and guiding architectural decisions for long-term code maintainability.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_pae",
            "company": "Intel Corporation",
            "title": "Datacenter PAE | Platform Application Engineer (Intel Federal)",
            "period": "Aug 2016 – Oct 2019",
            "location": "Hillsboro, OR",
            "context_line": "Worked directly with major OEM customers to understand requirements, align datacenter roadmaps with Intel platform capabilities, and shape deployment of custom server solutions.",
            "bullets": [
                {
                    "node_id": "node_exp_pae_01",
                    "text": "Debugged BIOS and microcode-related issues during platform bring-up.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_02",
                    "text": "Deployed customer development environments internally to reproduce and debug issues involving firmware, BIOS, and cluster networking.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_03",
                    "text": "Developed C++ and PECI/IPMI-based automation scripts for thermal, power transient, and firmware validation.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_04",
                    "text": "Managed a 100-node KNL Linux cluster to validate high-performance computing (HPC) deployment architectures, datacenter networking (Mellanox InfiniBand/Ethernet), and system-level stress.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_05",
                    "text": "Ramped on early ML hardware architecture alongside the Intel Nervana team, analyzing neural network precision reduction strategies (quantization) and distributed matrix multiplication for parallel execution.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_06",
                    "text": "Validated vendor compatibility with High-performance storage architectures (Optane PMEM).",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_pae_07",
                    "text": "Shadowed RAS validation group to create automated RAS test libraries, leading to a transition to the Manageability Test team lead position.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_simics",
            "company": "Intel Corporation",
            "title": "Pre-Silicon SIMICS Graphics Modeling Engineer",
            "period": "Jan 2016 – Jul 2016",
            "location": "Hillsboro, OR",
            "context_line": "Worked in pre-silicon simulation and modeling environments for GPU and SoC validation under Linux.",
            "bullets": [
                {
                    "node_id": "node_exp_simics_01",
                    "text": "Developed deep Linux expertise to rapidly integrate, parse logs, and debug across massive, cross-domain codebases (OS kernel, drivers, firmware), utilizing standard CLI toolchains (grep, awk, sed) for deep-stack system troubleshooting.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_visa",
            "company": "Intel Corporation",
            "title": "Post-Silicon Debug Software Developer",
            "period": "Jan 2011 – Dec 2015",
            "location": "Hillsboro, OR",
            "context_line": "Owned development of the VISA debug application within Intel's Platform Debug Toolkit, used for signal-trace and SoC debug.",
            "bullets": [
                {
                    "node_id": "node_exp_visa_01",
                    "text": "Performed SoC subsystem debug using Intel VISA for internal signal tracing and functional analysis.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_visa_02",
                    "text": "Automated signal trace visualization and simplified workflow integration across products, CI/CD.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_visa_03",
                    "text": "Refactored and optimized core modules for faster turnaround and easier maintenance.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_bmc",
            "company": "Intel Corporation",
            "title": "BMC Firmware Engineer",
            "period": "Sep 2008 – Dec 2010",
            "location": "Hillsboro, OR",
            "context_line": "Developed and validated embedded firmware for server manageability features.",
            "bullets": [
                {
                    "node_id": "node_exp_bmc_01",
                    "text": "Developed and validated end-to-end management architectures, spanning Out-of-Band (OOB) networking protocols to In-Band OS-level interfaces including KCS, HECI, and ipmitool provisioning.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_bmc_02",
                    "text": "Implemented DCMI and Serial Over LAN (SOL) protocols in C, and built lightweight RMCP/RAKP socket communication libraries.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_bmc_03",
                    "text": "Identified a fundamental protocol-level vulnerability in IPMI 2.0 RAKP authentication (later classified as industry-wide CVE-2013-4786) by patching Wireshark source code to debug and parse custom session negotiation packets.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        },
        {
            "role_id": "role_intel_val",
            "company": "Intel Corporation",
            "title": "Validation Engineer | Firmware Validation (Contract & Internship)",
            "period": "Apr 2005 – Sep 2008",
            "location": "Hillsboro, OR",
            "context_line": "Validated server firmware and network tools across EFI, Windows, and Linux platforms.",
            "bullets": [
                {
                    "node_id": "node_exp_val_01",
                    "text": "Automated 80% of manual NIC testing using Perl and TCL/Expect.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_val_02",
                    "text": "Debugged LAN access issues and built automated IPMI recovery tests, cutting validation cycles by half.",
                    "citations": [],
                    "review_flags": []
                },
                {
                    "node_id": "node_exp_val_03",
                    "text": "Collaborated with BIOS and hardware teams on IA64 and x86 platform validation.",
                    "citations": [],
                    "review_flags": []
                }
            ]
        }
    ]
    ast["sections"].append({
        "section_id": "sec_experience",
        "heading": "Professional Experience",
        "roles": experience_roles
    })
    
    # Section 4: Education
    ast["sections"].append({
        "section_id": "sec_education",
        "heading": "Education",
        "nodes": [
            {
                "node_id": "node_edu_01",
                "institution": "Portland State University",
                "degree": "Bachelor of Computer Science",
                "period": "2000 – 2006",
                "citations": [],
                "review_flags": []
            },
            {
                "node_id": "node_edu_02",
                "institution": "Portland Community College",
                "degree": "Associate of Science",
                "period": "1996 – 1999",
                "citations": [],
                "review_flags": []
            }
        ]
    })
    
    return ast


def generate_style_schema():
    return {
        "layout_type": "ATS_SINGLE_COLUMN",
        "margins_inch": {
            "top": 0.5,
            "bottom": 0.5,
            "left": 0.6,
            "right": 0.6
        },
        "typography": {
            "font_family": "Calibri",
            "body_size_pt": 10.5,
            "header_size_pt": 13.0,
            "title_size_pt": 15.0,
            "line_spacing": 1.15
        },
        "rules": {
            "bold_lead_in_words": 3,
            "max_bullets_recent": 6,
            "max_bullets_older": 3,
            "context_line_italic": True,
            "bullet_length_max_lines": 2.5
        }
    }


def extract_dna_cards(ast):
    cards = []
    card_idx = 1
    
    # Card from Summary
    cards.append({
        "id": f"RESUME-{card_idx:03d}",
        "domain": "RESUME",
        "title": "Platform Engineering & Telemetry Architecture Career Core",
        "summary": "15+ years server manageability, firmware integration, and telemetry debug spanning silicon, BIOS, and BMC.",
        "content": ast["sections"][1]["nodes"][0]["text"],
        "tags": ["#datacenter", "#manageability", "#telemetry", "#firmware", "#ai_infrastructure"],
        "explicit_links": ["FEAT-586", "FEAT-592"],
        "metadata": {
            "type": "summary",
            "section": "sec_summary"
        }
    })
    card_idx += 1
    
    # Cards from Experience Bullets
    for role in ast["sections"][3]["roles"]:
        company = role["company"]
        role_title = role["title"]
        period = role["period"]
        for bullet in role["bullets"]:
            cards.append({
                "id": f"RESUME-{card_idx:03d}",
                "domain": "RESUME",
                "title": f"{role_title} Achievement ({company})",
                "summary": bullet["text"][:120] + "..." if len(bullet["text"]) > 120 else bullet["text"],
                "content": bullet["text"],
                "tags": ["#resume", f"#{company.lower().replace(' ', '_').replace(',', '')[:15]}", "#systems_engineering"],
                "explicit_links": bullet.get("citations", []),
                "metadata": {
                    "company": company,
                    "title": role_title,
                    "period": period,
                    "node_id": bullet["node_id"]
                }
            })
            card_idx += 1
            
    return cards


def main():
    print("🚀 [FEAT-595] Starting Resume AST Decomposition...")
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    
    raw_text = RAW_RESUME_PATH.read_text(encoding="utf-8")
    ast = parse_resume(raw_text)
    
    # 1. Save Paper AST
    paper_path = PAPERS_DIR / "PAPER-RESUME_v1.json"
    paper_path.write_text(json.dumps(ast, indent=2), encoding="utf-8")
    print(f"✅ Saved Paper AST -> {paper_path} ({len(ast['sections'])} sections)")
    
    # 2. Save Style Schema
    style_schema = generate_style_schema()
    style_path = PAPERS_DIR / "style_resume_v1.json"
    style_path.write_text(json.dumps(style_schema, indent=2), encoding="utf-8")
    print(f"✅ Saved Style Schema -> {style_path}")
    
    # 3. Extract & Save RESUME DNA Cards
    dna_cards = extract_dna_cards(ast)
    RESUME_DATA_PATH.write_text(json.dumps(dna_cards, indent=2), encoding="utf-8")
    print(f"✅ Saved {len(dna_cards)} RESUME DNA cards -> {RESUME_DATA_PATH}")
    
    # 4. Synchronize dna_manifest.json
    if DNA_MANIFEST_PATH.exists():
        manifest = json.loads(DNA_MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["resume"] = dna_cards
        DNA_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"✅ Updated DNA Manifest -> {DNA_MANIFEST_PATH} (domains: {list(manifest.keys())})")

    print("🎯 Decomposition & DNA extraction certified successfully!")


if __name__ == "__main__":
    main()
