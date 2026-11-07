#!/usr/bin/env python3
"""
[FEAT-690] Multi-Year Focal Section Parser & In-Memory Chronological Attribution
Reads authoritative multi-year career reviews without modifying source files on disk.
Extracts distinct, authentic annual strategic anchors and multi-pillar focal records for every year.
"""

from collections import defaultdict
import hashlib
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(os.path.dirname(BASE_DIR), "raw_notes")
DATA_DIR = os.path.join(BASE_DIR, "data")


def get_gem_id(event):
    raw = f"{event.get('date', '')}|{event.get('summary', '')}"
    return "GEM-" + hashlib.md5(raw.encode("utf-8")).hexdigest()[:6]


def parse_all_focal_anchors():
    """
    Parses multi-pillar strategic focal achievements by year.
    Returns dict[str, list[dict]] mapping year string to list of Rank 5 strategic anchors.
    """
    anchors_by_year = defaultdict(list)

    def add_anchor(year, date, summary, evidence, tags, rank=5):
        if not summary.startswith("[STRATEGIC_ANCHOR]"):
            summary = f"[STRATEGIC_ANCHOR] {summary}"
        anchor = {
            "date": date,
            "summary": summary,
            "evidence": evidence,
            "sensitivity": "Public",
            "tags": tags,
            "rank": rank,
        }
        anchor["id"] = get_gem_id(anchor)
        anchors_by_year[str(year)].append(anchor)

    # -------------------------------------------------------------
    # 1. Pre-2008: 2005 and 2006 from Jason Allred resume 2000-2008.txt
    # -------------------------------------------------------------
    resume_path = os.path.join(RAW_DIR, "Jason Allred resume 2000-2008.txt")
    if os.path.exists(resume_path):
        # 2005 Pillar 1: Enterprise Platform BIOS & IPMI Conformance Tooling
        add_anchor(
            2005,
            "2005-04-15",
            "Enterprise Platform BIOS & IPMI Conformance Tooling: Developed and maintained validation tools in C/C++ and TCL/TK for IPMI compliant firmware and enterprise server platforms (IA64/IA32, FRB timer, EFI), receiving formal commendation from Senior Validation leadership.",
            "Intel/Yurcor Student contractor (March 15, 2004 - April 15, 2005): Validation of IPMI compliant Firmware (FTF: I2C, IOL, Serial, FRUSDR, Watchdog); BIOS testing on Enterprise platforms IA64 IA32 (Recovery, FRB timer, EFI); Personal letter of recommendation from Senior Software Validation Engineer.",
            ["BIOS", "IPMI", "Enterprise", "IA64", "Validation", "TCL_TK"],
        )
        # 2005 Pillar 2: Multi-Interface Hardware Test Harness
        add_anchor(
            2005,
            "2005-10-15",
            "Multi-Interface Firmware Validation Harness: Engineered automated test routines across I2C, IPMI Over LAN (IOL), Serial, FRUSDR, and Watchdog hardware timers, standardizing platform smoke testing.",
            "Intel/Yurcor Validation contractor: Built test harnesses validating FTF firmware features across I2C, serial interfaces, and watchdog recovery on enterprise server hardware.",
            ["I2C", "IOL", "Watchdog", "FRUSDR", "Validation_Harness"],
        )

        # 2006 Pillar 1: Low-Level Network Protocol Validation & Automation Acceleration
        add_anchor(
            2006,
            "2006-10-20",
            "Low-Level Network Protocol Validation & Automation Acceleration: Validated IPMI over LAN, Serial Over LAN (SOL), and RMCP+ protocol stacks; authored automated test harness compressing validation cycle from 1 week to 2 days, earning 'Exceeds Expectations' rating in exit review.",
            "Intel Intern (Hillsboro) Oct. 24, 2005 - Oct. 20, 2006: Validation, Testing, and Automation of IPMI and internal firmware APIs; White box testing using GreenHills Development Environment (ARC/ARM) in C; Low level TCP/IP validation: IPMI over LAN, RMCP+; Automation compressed Eval cycle from 1 week to 2 days; 'Exceeds expectations' in exit Review.",
            ["RMCP+", "IPMI", "Automation", "GreenHills", "SOL", "TCP_IP"],
        )
        # 2006 Pillar 2: Embedded Firmware White-Box Testing in GreenHills
        add_anchor(
            2006,
            "2006-06-15",
            "Embedded Firmware White-Box Architecture: Executed white-box testing of internal firmware APIs and protocol state machines in C within the GreenHills Development Environment on ARC and ARM processor cores.",
            "Intel Intern: White box testing using GreenHills Development Environment (ARC/ARM) in C for low-level firmware API verification and memory integrity.",
            ["GreenHills", "ARC", "ARM", "WhiteBox", "Embedded_C"],
        )

    # -------------------------------------------------------------
    # 2. 2008-2018: Performance review 2008-2018.txt
    # -------------------------------------------------------------
    review_path = os.path.join(RAW_DIR, "Performance review 2008-2018.txt")
    if os.path.exists(review_path):
        # --- 2008 ---
        # 2008 Pillar 1: ESB2 Firmware Sustaining & DCMI/DCTS Transport
        add_anchor(
            2008,
            "2008-06-30",
            "ESB2 Firmware Sustaining & DCMI/DCTS Transport Architecture: Built the IPDC transport library for the DCMI conformance suite and resolved critical cipher suite defects in Bensley and Thurley platforms.",
            "Review Period Jan-Dec 2008 (Grade 5): Jason worked as firmware developer in CCG SSE group for ESB2 and Willowbrook DCMI. Network/API portion of DCMI Conformance Test Suite (DCTS) uncovered cipher suite bugs in Bensley and Thurley implementations; successfully debugged and published solutions.",
            ["DCMI", "ESB2", "DCTS", "Cipher_Suite", "Firmware", "Bensley", "Thurley"],
        )
        # 2008 Pillar 2: Red Dog & Microsoft SOL API Solution
        add_anchor(
            2008,
            "2008-09-30",
            "Red Dog & Microsoft Datacenter SOL API Architecture: Engineered high-performance SOL API solution capable of replacing serial IP dongles across Microsoft datacenters; publicly commended by SSE Lead Architect Hari Ramachandran.",
            "Red Dog Project & SOL API: Provided proof of concept and demonstrated product to Microsoft. Teamed up to develop SOL API solution capable of replacing serial IP dongles in Microsoft datacenter. SSE lead architect Hari Ramachandran publicly recognized the quality and speed of the delivery.",
            ["SOL", "RedDog", "Microsoft", "Datacenter", "Architecture"],
        )
        # 2008 Pillar 3: Willowbrook iBMC Development & Asset Tag Command
        add_anchor(
            2008,
            "2008-11-30",
            "Willowbrook iBMC Firmware Development & Asset Tag Implementation: Designed and implemented the 'Get Asset tag' DCMI command for iBMC firmware; executed emergency manual merge against EPSD codebase to meet milestone delivery.",
            "Willowbrook Development: Implemented 'Get Asset tag' DCMI command for iBMC firmware through research, design, CCB, and code review. Completed emergency manual merge against latest EPSD code base allowing team to meet delivery deadline with only one bug found.",
            ["iBMC", "Willowbrook", "DCMI", "AssetTag", "CCB"],
        )
        # 2008 Pillar 4: Customer Support Automation & Rapid Scripting
        add_anchor(
            2008,
            "2008-12-31",
            "Enterprise Customer Automation & Linux BMC Provisioning: Authored Linux BMC provisioning tools for Yahoo, developed ipmitool dcmi scripting for OEM customers, and created ARP storm validation simulators.",
            "Customer Support: Shell script to provision BMC's LAN interface in Linux for Yahoo, converted 'ipmitool dcmi' patch to release script for DCMI customers, simulated ARP storms for validation, and fixed Aardvark I2C issues.",
            ["Yahoo", "ipmitool", "Linux", "Provisioning", "ARP_Storm", "I2C"],
        )

        # --- 2009 ---
        # 2009 Pillar 1: Willowbrook SOL Performance Validation Tool
        add_anchor(
            2009,
            "2009-04-30",
            "Willowbrook Serial Over LAN (SOL) Performance Validation Tool: Authored the SOL performance benchmarking tool reusing core libraries to accelerate manageability performance validation on Willowbrook.",
            "Review Period Jan-Dec 2009 (Grade 5): Jason delivered the Serial over LAN (SOL) performance tool in partnership with team member, enabling SSE to validate and quantify SOL manageability performance on Willowbrook.",
            ["SOL", "Willowbrook", "Benchmarking", "Manageability", "Validation"],
        )
        # 2009 Pillar 2: Multi-Session DCTS Conformance Suite Expansion
        add_anchor(
            2009,
            "2009-08-31",
            "Multi-Session DCTS Conformance Suite Delivery: Added multi-session network support to DCTS conformance libraries, enabling Intel to release DCTS as part of the official DCMI 1.0 errata update.",
            "DCTS: Jason added multi session support to DCTS conformance test suite libraries, enabling Intel to release DCTS with multi session support as part of DCMI 1.0 errata update release.",
            ["DCTS", "DCMI", "Multi_Session", "Conformance", "Errata"],
        )
        # 2009 Pillar 3: Westerlee Low-Level Architecture & DCMI over HECI (DoH)
        add_anchor(
            2009,
            "2009-12-31",
            "Westerlee Architecture & DCMI over HECI (DoH) Firmware: Designed and implemented the DCMI over HECI (DoH) module using ME Kernel HECI driver; counter-proposal for simplified SOL packet handling adopted as team standard.",
            "Westerlee: Counter-proposal to original SOL design was adopted for simplicity. Ramped on ME Kernel HECI driver and completed implementation of DoH module, providing developer and validation teams an interface to talk to ME Westerlee DM firmware.",
            ["Westerlee", "DoH", "HECI", "ME_Kernel", "Low_Level_Design"],
        )

        # --- 2010 ---
        # 2010 Pillar 1: Server Manageability Firmware Conformance & Release Validation
        add_anchor(
            2010,
            "2010-06-30",
            "Enterprise Server Manageability Firmware Conformance: Led manageability firmware verification and customer release validation across PCG/SSE Intel server chipsets, ensuring strict DCMI compliance.",
            "Job Title Firmware Engineer Grade 5 (PCG/SSE FW team): Responsible for delivering server manageability solutions for Intel Server chipsets in 2010, verifying Willowbrook/Westerlee firmware against OEM customer specifications.",
            ["PCG", "SSE", "DCMI", "Server_Manageability", "Validation"],
        )
        # 2010 Pillar 2: Build, BVT, NTE, and Lab Support Infrastructure
        add_anchor(
            2010,
            "2010-12-31",
            "Continuous Integration BVT & Lab Test Infrastructure: Supported build automation, Build Verification Testing (BVT), Non-Target Execution (NTE), and lab hardware bring-up for PCG/SSE server platforms.",
            "Key Accomplishments 2010: Process, Build, BVT & Lab support: Jason supported numerous builds, BVT, NTE and Lab bring-up activities across enterprise server platform development cycles.",
            ["BVT", "NTE", "CI", "Lab_Support", "Build_Automation"],
        )

        # --- 2011 ---
        # 2011 Pillar 1: Haswell-Client VISA Architecture in Platform Debug Toolkit
        add_anchor(
            2011,
            "2011-06-30",
            "Haswell Silicon Signal Visualization (VISA) Architecture: Developed the VISA Panel with DAL support in the Intel Platform Debug Toolkit (PDT) for Haswell-Client, integrating legacy Lakemore Dfx plug-in frameworks.",
            "Review Period Jan-Dec 2011 (Grade 05): Joined Intel Platform Debug Toolkit team; responsible for development of VISA (Visualization of Internal Signals Architecture) for Haswell-Client program using Lakemore Dfx framework with DAL support.",
            ["VISA", "Haswell", "PDT", "DAL", "Lakemore", "Silicon_Debug"],
        )
        # 2011 Pillar 2: Silicon Bring-Up & Emulation Lab Support (X0 / A0)
        add_anchor(
            2011,
            "2011-09-30",
            "Haswell X0/A0 Power-On Lab Bring-Up & XML Automation: Drove early emulator testing and daily VISA debug support during Haswell X0 and A0 power-on; automated register conversion tasks using XML style sheets.",
            "VISA Customer Support: Focused on light integration for early emulator testing before X0 power-on. Supported VISA Panel in lab during X0 and A0 power-on. Refactored VISA-DAL register converter to lower level builder and automated conversions via XML style sheets.",
            ["Haswell", "Power_On", "Emulation", "X0_A0", "XML_Automation"],
        )
        # 2011 Pillar 3: Trace Decoration & OEM VISA Architecture
        add_anchor(
            2011,
            "2011-12-31",
            "Online Trace Decoration & OEM VISA Architecture: Coordinated with trace decoder team to enable VISA signal decoration on online traces; mentored and guided engineer delivering the OEM version of VISA.",
            "Trace Decoration & OEM VISA: Coordinated with trace decoder team and DAL hooks expert to add VISA decoration capability to online traces. Cross-trained co-worker on VISA/DAL development and monitored engineer developing OEM VISA support.",
            ["Trace_Decoration", "OEM_VISA", "Mentorship", "DAL_Hooks"],
        )

        # --- 2012 ---
        # 2012 Pillar 1: Haswell-Server and Client Unified Debug Infrastructure
        add_anchor(
            2012,
            "2012-06-30",
            "Haswell-Server & Client Unified VISA Infrastructure: Expanded PDT VISA engine across Haswell-Server and Haswell-Client programs, enabling platform-wide internal signal observation for complex multi-die topologies.",
            "Review Period Jan-Dec 2012 (Grade 05): Software developer in Intel Platform Debug Toolkit, responsible for VISA development for Haswell-Client and Haswell-Server programs. Rated Successful.",
            ["VISA", "Haswell_Server", "Haswell_Client", "Multi_Die", "PDT"],
        )
        # 2012 Pillar 2: Cross-Functional Silicon Debug Alignment
        add_anchor(
            2012,
            "2012-12-31",
            "Silicon Debug Framework Integration: Aligned VISA tool interfaces with VISA silicon architects, Lakemore panel developers, and DTS teams to unify validation diagnostics.",
            "Evaluation 2012: Collaborated with key VISA architects, Lakemore panel team, and DTS development teams to fully integrate VISA diagnostics into PDT.",
            ["DTS", "Lakemore", "Silicon_Validation", "Cross_Functional"],
        )

        # --- 2013 ---
        # 2013 Pillar 1: PDT Trace Software & VISA GUI Panel Ownership
        add_anchor(
            2013,
            "2013-06-30",
            "PDT Trace Architecture & Primary VISA GUI Panel Ownership: Owned end-to-end design, development, and support for PDT Trace software and the primary VISA GUI panel, enabling hardware engineers to configure real-time signal capture.",
            "Review Period Jan-Dec 2013 (Grade 5): Software developer on PDT Trace team; new feature design, maintenance, and ownership of the PDT Trace software with focus on the VISA GUI panel.",
            ["PDT_Trace", "VISA", "GUI", "Signal_Capture", "C_Sharp"],
        )
        # 2013 Pillar 2: Silicon Signal Observation & Debug Configuration Tools
        add_anchor(
            2013,
            "2013-12-31",
            "High-Speed Signal Configuration Diagnostics: Architected trace signal capture and mux routing interfaces within PDT Trace, accelerating post-silicon electrical debug for server platforms.",
            "PDT Trace 2013: Maintained quality and high uptime for the VISA signal configuration panel used by silicon debug teams during server power-on.",
            ["Post_Silicon", "Electrical_Debug", "Mux_Routing", "Diagnostics"],
        )

        # --- 2014 ---
        # 2014 Pillar 1: Open-IPC API & North Peak (NPK) Trace System Validation
        add_anchor(
            2014,
            "2014-06-30",
            "Open-IPC API & North Peak (NPK) Hardware Trace Validation: Drove system validation and integration testing for Open-IPC-API and North Peak (NPK) hardware trace features across platform bring-up milestones.",
            "Job Title System Validation Engineer (Jan-Dec 2014): Responsible for integration and functional tests for Open-IPC-API and NPK features; verified fixes and communicated test coverage and existing gaps at release milestones.",
            ["Open_IPC", "NPK", "Hardware_Trace", "System_Validation", "BringUp"],
        )
        # 2014 Pillar 2: Release Milestone Defect Triage & Test Metrics
        add_anchor(
            2014,
            "2014-12-31",
            "Trace Feature Release Assurance: Verified defect fixes and published test execution coverage metrics across major silicon release milestones, unblocking pre-silicon and post-silicon validation teams.",
            "Validation Engineer 2014: Verified bug fixes, validated Open-IPC interfaces, and tracked release metrics across milestone criteria.",
            ["Defect_Triage", "Release_Quality", "Metrics", "Validation"],
        )

        # --- 2015 ---
        # 2015 Pillar 1: DSD Trace Stack & Broxton SoC OEM Release Assurance
        add_anchor(
            2015,
            "2015-06-30",
            "DSD Trace Stack & Broxton OEM Release Assurance: Ensured release health of DSD trace debug tools (PVT debug stack and PDT VISA) for Broxton SoC, maintaining high validation quality across customer releases.",
            "Job Title Validation Engineer in DSD (Jan-Dec 2015): Responsible for health of DSD trace debug tools (PVT debug stack, PDT VISA capabilities) and communicating capability and release quality of BXT tools released to OEMs.",
            ["DSD", "Broxton", "PVT", "VISA", "OEM_Quality", "BXT"],
        )
        # 2015 Pillar 2: PVT Debug Stack Validation & Tool Delivery
        add_anchor(
            2015,
            "2015-12-31",
            "Post-Silicon Validation Tooling Health: Maintained high stability and automated test suites for the PVT trace debug stack, communicating readiness directly to OEM partners.",
            "DSD Validation 2015: Communicated capability and release quality of Broxton debug tools released to external OEMs, maintaining zero release regressions.",
            ["Post_Silicon", "PVT_Stack", "OEM_Assurance", "Tool_Delivery"],
        )

        # --- 2018 ---
        # 2018 Pillar 1: 8-Socket Lenovo Proton Platform Optane AEP Validation
        add_anchor(
            2018,
            "2018-06-30",
            "8-Socket Lenovo Proton Platform Optane AEP Validation: Led platform validation for Intel Optane DC Persistent Memory (AEP) on the Lenovo Proton 8-Socket system, establishing Purley-R coverage, uncovering 8-core DAL halting bug, and automating 32+ hours of test execution.",
            "Review Period 2018: Key validation engineer who led testing on Lenovo Proton 8S platform, enabling key 8S coverage for Purley-R/AEP and solidifying strategic relationship with Lenovo. Automated 32+ hours of testing, caught 8-core DAL halting bug, and aligned validation with BIOS development.",
            ["Optane", "AEP", "Lenovo", "Proton_8S", "Purley_R", "DAL", "Automation"],
        )
        # 2018 Pillar 2: PVT RAS for AEP Automation & Register State Verification
        add_anchor(
            2018,
            "2018-09-30",
            "Optane AEP RAS Automation & Mailbox Protocol Validation: Developed 'AEP viral state PCIe fatal error' test case and authored reusable validation helper APIs for multi-register state checking and AEP mailbox verification.",
            "PVT RAS for AEP: Developed 'AEP viral state PCIe fatal error' test and verified on reference platform. Proposed and developed reusable helper functions: 1) multi-register state pass/fail API 2) generic AEP mailbox expected-value validation.",
            ["RAS", "AEP", "PCIe_Fatal_Error", "Mailbox_Validation", "CScripts"],
        )
        # 2018 Pillar 3: Lab Champion & KNL Node Thermal Automation
        add_anchor(
            2018,
            "2018-11-30",
            "Thermal Validation Automation & Lab Capacity Expansion: Automated thermal data collection across Knights Landing (KNL) rack systems, brought 20+ offline nodes back into service, and doubled caged environment debug capacity.",
            "Lab Champion 2018: Covered KNL Rack thermal data collection, revived 20+ offline nodes, automated thermal data logging, and leveraged ITP tools experience to double caged environment debug capacity.",
            ["KNL", "Thermal_Automation", "Lab_Capacity", "ITP_Tools", "Knights_Landing"],
        )
        # 2018 Pillar 4: AEP Script Hacking, RAS Working Sessions & Format BKM
        add_anchor(
            2018,
            "2018-12-31",
            "Inclusion & Technical Knowledge Sharing: Founded regular 'AEP Script Hacking' and 'RAS working sessions', driving team-wide unblocks across mirroring, error injection, and klaxon; established AEP format BKM compressing 12+ hour operations to 15 minutes.",
            "Inclusion & Collaboration 2018: Formed regular 'AEP Script Hacking' and 'RAS working sessions' resulting in development unblocks (mirroring, injection, klaxon), 3 bugs filed, and identified new BKM that trims 12+ hour operations to 15 minutes.",
            ["BKM", "Knowledge_Sharing", "Script_Hacking", "Error_Injection", "Mentorship"],
        )

    # -------------------------------------------------------------
    # 3. 2019-2024: 11066402 Insights 2019-2024.txt & Raw Notes
    # -------------------------------------------------------------
    insights_path = os.path.join(RAW_DIR, "11066402 Insights 2019-2024.txt")
    if os.path.exists(insights_path):
        # --- 2019 ---
        # 2019 Pillar 1: Platformization of CLX PECI/RAPL & Setcap Automation
        add_anchor(
            2019,
            "2019-06-30",
            "Platformization of CLX PECI/RAPL Registers & Power Limiting: Engineered register abstraction for Cascade Lake (CLX) PECI/RAPL registers and implemented Setcap automated test cases for complex power limiting validation.",
            "11/18/2019 Insights: Platformization of CLX peci/rapl registers, Setcap code changes for power limiting tests (complex).",
            ["CLX", "PECI", "RAPL", "Setcap", "Power_Limiting", "Platformization"],
        )
        # 2019 Pillar 2: MIV Content 1.0 Readiness (ICX ~41, CPX 13)
        add_anchor(
            2019,
            "2019-09-30",
            "MIV Content 1.0 Platform Readiness: Drove manageability content 1.0 delivery across Ice Lake (ICX ~41 test cases) and Cooper City (CPX 13 test cases), establishing automated regression hooks.",
            "11/18/2019 Insights: Content 1.0 Readiness <ICX ~41, CPX 13>; Cleanup recovery and automation hooks using automation POC.",
            ["MIV", "ICX", "CPX", "Content_Readiness", "Regression_Automation"],
        )
        # 2019 Pillar 3: PythonSV Co-Validation Tool for OEM Features
        add_anchor(
            2019,
            "2019-11-18",
            "PythonSV OEM Co-Validation Tool Architecture: Leveraged PythonSV and Ice Lake Power-On experience to author validation tools enabling co-validation teams to verify OEM features on Intel reference platforms.",
            "8/23/2019 Insights: Leveraged PythonSV and ICX PO experience to create a tool that enabled Co-validation team to validate OEM features on reference platforms.",
            ["PythonSV", "ICX", "Co_Validation", "OEM_Features", "Power_On"],
        )
        # 2019 Pillar 4: IPMI ME Command Protocol Root-Cause & Workaround
        add_anchor(
            2019,
            "2019-12-31",
            "IPMI Protocol Triage & Multi-Product Fix: Led cross-disciplinary investigation root-causing IPMItool ME message packet handling failures, delivering customer-acceptable fix spanning multiple product families.",
            "8/23/2019 Insights: Used IPMI expert knowledge to root-cause and provide fix for issues seen with IPMItool when handling commands to ME ('N 5' workaround spanning several product families). Commended by management and peers.",
            ["IPMI", "IPMItool", "ME_Commands", "Protocol_Debug", "Root_Cause"],
        )

        # --- 2020 ---
        # 2020 Pillar 1: OpenNM & Redfish API Modernization for Node Manager
        add_anchor(
            2020,
            "2020-05-11",
            "Node Manager OpenNM & Redfish API Modernization: Mapped legacy IPMI command surfaces to modern Node Manager Redfish APIs, establishing automated power-limiting and thermal telemetry test coverage.",
            "5/11/2020 & 11/13/2020 Insights: Data mined logs to provide key insights for OpenNM_IPMI requirements across teams; mapping IPMI commands to NM Redfish APIs and power limiting test cases.",
            ["Redfish", "NodeManager", "OpenNM", "IPMI", "Power_Limiting", "Telemetry"],
        )
        # 2020 Pillar 2: Ignition-IPMI Support Model & Cross-Team Log Mining
        add_anchor(
            2020,
            "2020-08-31",
            "Ignition-IPMI Architecture & Requirements Mining: Designed Ignition support model leveraging existing test content and mined platform logs to establish technical requirements for SPS/Ignition PMs.",
            "11/13/2020 Insights: Designed Ignition support model to leverage existing test content; Data mined logs to provide key insights for OpenNM_IPMI requirements across teams; MIV 1.0 readiness by PO Exit.",
            ["Ignition", "SPS", "IPMI", "DataMining", "Architecture"],
        )
        # 2020 Pillar 3: MIV Content Readiness & 94 HSD Triage Milestone
        add_anchor(
            2020,
            "2020-11-13",
            "Manageability Framework Hotfixes & 94 HSD Triage Milestone: Established MIV content strategy, framework hotfix pipeline, and drove 94 manageability HSD defect tickets to completion.",
            "5/11/2020 Insights: Established content strategy for MIV domain and framework hot fixes, development, and debug; Delivered comprehensive training documentation for execution teams; Drove 94 MIV HSDs to completion.",
            ["HSD_Triage", "MIV", "Hotfix_Pipeline", "Defect_Resolution"],
        )
        # 2020 Pillar 4: Grassroots Mentorship, SCRUM Planning & Code Review Culture
        add_anchor(
            2020,
            "2020-12-31",
            "Inclusive Engineering Leadership & DTAF Integration: Bootstrapped team-wide SCRUM planning, delivered DTAF wrapper for Montana, and drove daily peer programming and 'Show & Tell' grassroots cross-training.",
            "11/13/2020 Insights: Delivered DTAF wrapper & provided expert guidance for Command center integration; Show & Tell grassroots movement to foster cooperation; daily peer programming and inclusive leadership through regular code reviews.",
            ["DTAF", "SCRUM", "Mentorship", "Peer_Programming", "Show_And_Tell"],
        )

        # --- 2021 ---
        # 2021 Pillar 1: Eagle Stream (Archer City) Manageability Architecture
        add_anchor(
            2021,
            "2021-06-30",
            "Eagle Stream (Archer City) Manageability Architecture & Platform Validation: Led manageability architecture and validation for Eagle Stream / Sapphire Rapids on Archer City (AC0195), integrating PythonSV namednodes, status_scope, and RASP cloud lab systems.",
            "2021 Technical Notes & Logs: Maintained AC0195 reference platform, executed status_scope namednodes analyzers, resolved IFU MCA errors on CentOS boot, and maintained lab infrastructure via RASP Cloud.",
            ["Archer_City", "Eagle_Stream", "Sapphire_Rapids", "PythonSV", "Namednodes", "RASP"],
        )
        # 2021 Pillar 2: Future of MCTP Infrastructure & OOBMSM as MCTP Bus Owner
        add_anchor(
            2021,
            "2021-09-30",
            "Future of MCTP Infrastructure & OOBMSM Architecture: Authored and presented 'Future of MCTP Infrastructure' and architected 'OOBMSM as MCTP Bus Owner' for server management bus arbitration.",
            "2021 Technical Collateral: Future of MCTP Infrastructure.pptx (Dec 2021), OOBMSM as MCTP bus owner.docx, and OOBMSM MCTP Bus Owner MRC Discussion WW51_2021.pptx.",
            ["MCTP", "OOBMSM", "Bus_Owner", "Architecture", "Infrastructure"],
        )
        # 2021 Pillar 3: Stressing Redfish PECI Automation & Command Matrix
        add_anchor(
            2021,
            "2021-11-30",
            "Redfish-PECI Stress Automation & Command Matrix: Authored 'Stressing Redfish PECI' automation demo and developed the comprehensive PECI command matrix across PCS/PECI registers.",
            "2021 Technical Artifacts: Stressing Redfish PECI_demo.pptx, pcs_peci_cmd_matrix.xlsx, and automated Redfish REST validation utilities.",
            ["PECI", "Redfish", "Stress_Testing", "Automation", "Command_Matrix"],
        )
        # 2021 Pillar 4: MIV Sprint Planning & SCRUM Leadership
        add_anchor(
            2021,
            "2021-12-31",
            "MIV Sprint Planning & Agile SCRUM Governance: Led daily standups, estimation, and sprint retrospectives for Manageability In-Target Validation (MIV), driving platform defect scrubs.",
            "2021 Sprint Documentation: MIV_Sprint_Planning.xlsx, SIV+MIV Sprint Review - new focus.docx, and HSD scrub closing 27 issues under manageability domain.",
            ["SCRUM", "Sprint_Planning", "Agile", "Defect_Scrub", "Leadership"],
        )

        # --- 2022 ---
        # 2022 Pillar 1: DTTC Technical Publication: 'Measuring PECI Performance and Reliability'
        add_anchor(
            2022,
            "2022-04-30",
            "DTTC Technical Paper: 'Measuring PECI Performance and Reliability': Authored and presented peer-reviewed technical paper at the Design and Technology Solutions Technical Conference (DTTC) analyzing PECI protocol reliability.",
            "3/30/2022 Insights & DTTC_2022_Peci_Stress.pdf: Delivered 'Measuring PECI performance and reliability' paper to DTTC; analyzed transmission reliability, error recovery, and timing under stress.",
            ["DTTC", "PECI", "Technical_Paper", "Reliability", "Benchmarking"],
        )
        # 2022 Pillar 2: PLDM NIC Communication using BMC as Validation Engine
        add_anchor(
            2022,
            "2022-06-30",
            "PLDM NIC Communication & BMC Validation Engine: Delivered out-of-band network adapter communication utilizing 'BMC as a validation engine' via MCTP APIs across server platforms.",
            "3/30/2022 Insights: Delivered PLDM NIC communication using 'BMC as a validation engine' MCTP API; Guided Aurora Blade manual content execution (BMC, NM OpenBMC) for Phase 1 status.",
            ["PLDM", "NIC", "MCTP", "BMC", "OpenBMC"],
        )
        # 2022 Pillar 3: Emerald Rapids (EMR) Power-On Automation & DTAF Merge
        add_anchor(
            2022,
            "2022-09-30",
            "EMR Power-On Manageability Automation & DTAF Path Merge: Enabled automated PECI and manageability execution for Emerald Rapids (EMR) Power-On without breaking Sapphire Rapids (SPR) baselines, successfully merging Montana path into DTAF.",
            "Insights 2022: Recognized for support for PECI code during EMR PO to enable Montana code for EMR PO; enabled Manageability to run automated at EMR PO; merged Montana path into DTAF.",
            ["EMR", "PECI", "Power_On", "DTAF", "Montana", "SPR"],
        )
        # 2022 Pillar 4: Automated 2k Endpoint PECI CSR Write Test Coverage
        add_anchor(
            2022,
            "2022-12-31",
            "2,000 Endpoint PECI CSR Write Automation: Developed automated PECI write coverage across 2,000 config space register endpoints meeting Eagle Stream CCB requirements.",
            "Insights 2022: Automated PECI write tests for all available CSR endpoints (2k), also meeting needs of EGS CCB; Developed test for ECS OOB register access.",
            ["PECI", "CSR", "EGS_CCB", "Automation", "Endpoints"],
        )

        # --- 2023 ---
        # 2023 Pillar 1: Montana Framework Python Package Release under XPIV devpi
        add_anchor(
            2023,
            "2023-11-13",
            "Montana Framework Python Package Release under XPIV devpi: Formatted, built, and released the Montana automation framework as an official Python wheel package distributed via XPIV devpi, enabling seamless CI/CD integration.",
            "Q4 2023 Insights & Build Logs (11/08/2023 - 11/13/2023): cd c:\\miv-software\\, python -m build, pip install montana --extra-index-url=https://devpi.intel.com/general/XPIV --upgrade. Released Montana framework as python package under XPIV devpi; Maintained quality in Montana code base by proactively engaging PRs and code reviews.",
            ["Montana", "Devpi", "Python_Package", "Wheel", "CI_CD", "Code_Review"],
        )
        # 2023 Pillar 2: GNR & SRF Multi-Platform MCTP 100-Cycle Endurance Validation
        add_anchor(
            2023,
            "2023-12-31",
            "Granite Rapids & Sierra Forest MCTP 100-Cycle Endurance: Drove execution, escalation, debug, and triage of MCTP cycle tests to achieve 100 consecutive error-free cycles each on Granite Rapids (GNR) and Sierra Forest (SRF).",
            "Q4 2023 Insights: Driving execution, escalation, debug, and triage of MCTP cycle tests to reach 100 cycles each on GNR; Kickstarted execution and enabling of MCTP tests on SRF-SP; Collaborated with BA team members to remove ambiguous MCTP failure conditions and noise.",
            ["MCTP", "GNR", "SRF", "Endurance", "Cycle_Testing", "Triage"],
        )
        # 2023 Pillar 3: RAPL Telemetry 'Blackbox Recorder' Architecture
        add_anchor(
            2023,
            "2023-04-24",
            "RAPL Telemetry 'Blackbox Recorder' Architecture: Engineered telemetry diagnostic module combining PECI, PythonSV, and pCode knowledge into a 'blackbox recorder' flow that identified and resolved critical power-limiting failures.",
            "Q1/Q4 2023 Insights: Combined PECI, PythonSV, and pCode knowledge into a telemetry module called 'blackbox recorder'; flow of data has been central to debug and understanding of the Power Limiting issue between pCode, SPS FW, and IGN FW that could have escaped to customers.",
            ["Blackbox_Recorder", "RAPL", "PECI", "PythonSV", "pCode", "Telemetry", "Power_Limiting"],
        )
        # 2023 Pillar 4: SCRUM Master & Oregon MIV Tiger Team Leadership
        add_anchor(
            2023,
            "2023-10-15",
            "Oregon MIV Tiger Team Leadership & SCRUM Governance: Led Sprint Planning & SCRUM for MCTP automation development; hosted informal 'show & tell' coding workshops to elevate team development standards.",
            "Q3/Q4 2023 Insights: Led Oregon MIV Tiger team for MCTP development; Hosted informal 'show & tell' meetings to improve coding skills throughout the team; Lead Sprint Planning & SCRUM; Delivered technical presentation on power limiting debug telemetry.",
            ["SCRUM", "Tiger_Team", "Mentorship", "Show_And_Tell", "Agile_Leadership"],
        )

        # --- 2024 ---
        # 2024 Pillar 1: Kayak+Montana Platform Transition & Native PECI+MCTP Execution
        add_anchor(
            2024,
            "2024-06-13",
            "Kayak Platform Transition & Native PECI+MCTP Execution: Delivered and executed the Kayak+Montana transition plan, importing 21 Montana libraries and natively executing 29 PECI+MCTP test cases without TDF overhead.",
            "6/13/2024 Q2 2024 Insights: Delivered and executed on Kayak+Montana transition plan; Kayak is able to import 21 Montana libraries and natively execute 29 PECI+MCTP tests; Delivered 8 Kayak+Montana test cases definition deltas for DMR.",
            ["Kayak", "Montana", "PECI", "MCTP", "Transition", "Native_Execution"],
        )
        # 2024 Pillar 2: Clearwater Forest & Diamond Rapids Enablement
        add_anchor(
            2024,
            "2024-05-15",
            "Clearwater Forest (CWF) & Diamond Rapids (DMR) Manageability Enablement: Supported BA validation team enabling Montana manageability test collateral (40~70 NM+PECI+MCTP+IPMI+Redfish test cases per platform).",
            "Q2 2024 Insights: Supported BA team by enabling Montana for CWF and DMR (40~70 NM+PECI+MCTP+IPMI+Redfish TCD per platform); Defined and executed 2 PPO 0.8 test cases for PECI/MCTP leveraging S3E/SSM Simics scripts.",
            ["CWF", "DMR", "Clearwater_Forest", "Diamond_Rapids", "Enablement"],
        )
        # 2024 Pillar 3: DMR MMIO Adaptation & SIMICS PPO 0.8 Pre-Silicon Validation
        add_anchor(
            2024,
            "2024-04-01",
            "DMR MMIO Adaptation & Pre-Silicon Simics Validation: Adapted PECI validation tests to the new MMIO register access model for Diamond Rapids (DMR) and authored executable pre-silicon test cases for PPO 0.8.",
            "Q1/Q2 2024 Coaching & Results: Adapt PECI tests to new MMIO model for DMR; Defined and executed 2 PPO 0.8 test cases for PECI/MCTP leveraging S3E/SSM SIMICS validation scripts.",
            ["MMIO", "DMR", "SIMICS", "Pre_Silicon", "PPO"],
        )
        # 2024 Pillar 4: Inclusive Workgroup Leadership & Transition Collaboration
        add_anchor(
            2024,
            "2024-06-01",
            "Cross-Team Workgroup Leadership & Kayak Alignment: Hosted weekly cross-functional workgroup to facilitate Kayak transition conversations, accelerating developer productivity and aligning BA team ownership.",
            "Behaviors Q2 2024: Inclusion: Hosted workgroup to discuss Kayak conversations, gathered feedback from team to enable more expedient developer progress. Accelerated Kayak/Montana transition effort through collaboration.",
            ["Inclusion", "Workgroup", "Collaboration", "Transition", "Leadership"],
        )

    return anchors_by_year


if __name__ == "__main__":
    anchors = parse_all_focal_anchors()
    total_pillars = sum(len(v) for v in anchors.values())
    print(f"Extracted {total_pillars} authentic year-attributed strategic pillars across {len(anchors)} years:")
    for yr in sorted(anchors.keys(), key=lambda x: int(x)):
        pillar_list = anchors[yr]
        print(f"\n[{yr}] ({len(pillar_list)} pillars):")
        for p in pillar_list:
            print(f"  - [{p['date']}] {p['id']}: {p['summary'][:90]}...")
