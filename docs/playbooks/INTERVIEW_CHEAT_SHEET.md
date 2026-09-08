# Field Notes: The Ultimate Lookup Sheet (Interview Edition)

**Target:** NVIDIA Senior Platform Telemetry Engineer (JR2002276)  
**Date:** Monday, February 02, 2026

---

## 1. Monday Interview Strategy
**Schedule:**
- **9:00am – 9:45am:** Nick Ramirez
- **10:00am – 10:45am:** Jay Shah
- **11:00am – 11:45am:** Rohith Sudheer

**Core Themes:**
- **Telemetry & Validation:** Focus on Redfish, PECI, and MCTP validation.
- **Tooling:** Emphasize Python automation (PySV, wrappers) and custom C++ tools (SimpleRMCPP).
- **Architecture:** Demonstrate deep understanding of BMC/Host interfaces (OOBMSM, sideband).

---

## 2. Notable Scripts & Projects
*Code you can reference or open quickly.*

### **Telemetry & Stress Tools**
- **`pecistressor.py`** (2022): Python script for generating high-load PECI traffic to stress telemetry paths.
- **`SimpleRMCPP`** (C++): A lightweight RMCP+ (IPMI over LAN) client implementation.
    - *Key Features:* MD5/SHA1 auth, SOL (Serial Over LAN) support, transport plugin architecture.
    - *Location:* `raw_notes/SimpleRMCPP/`
- **`sensor_validator.py`** (2022): Validates OpenBMC sensor readings against expected thresholds.
- **`makechart.py`** (2022): Visualization tool for generating charts from telemetry logs.
- **`scan_NetFunction.py`** (2020): Scans IPMI NetFunctions for compliance/discovery.

### **Automation Wrappers**
- **`redfish_utils.py`** (2021): Utility library for interacting with Redfish APIs (GET/POST/PATCH).
- **`peci_framework_ipmi_example.py`** (2022): Demonstrates bridging PECI commands via IPMI.
- **`mctp_wrapper.cpp`** (2022): C++ wrapper for MCTP packet handling.

---

## 3. Notable Documents
*Key artifacts and specifications.*

### **Papers & Retrospectives**
- **[DTTC_2022_Peci_Stress.pdf](raw_notes/DTTC_2022_Peci_Stress.pdf)**: Your Design & Test Technology Conference paper on PECI stress testing.
- **[Jason Allred - War stories (Work).docx](raw_notes/Jason%20Allred%20-%20War%20stories%20(Work).docx)**: The master collection of engineering anecdotes.
- **[Purley-R Lenovo Collabration Retrospective.pptx](raw_notes/2019/Purley-R%20Lenovo%20Collabration%20Retrospective%20.pptx)**: Retrospective on the Lenovo collaboration (2019).

### **Specifications (Reference)**
- **Intel Intelligent Power Node Manager 4.0 Ext Interface.pdf** (2019): NM 4.0 spec.
- **ipmi-second-gen-interface-spec-v2-rev1-1_qct.pdf** (2021): IPMI Gen2 spec reference.
- **DSP0236_1.3.0_MCTP_base.pdf** (2023): MCTP Base Specification.

---

## 4. Directory Listing (Year-by-Year Scraps)
*A quick index of the "Year" folders containing raw notes and scraps.*

### **2019: Reliability & Power**
`raw_notes/2019/`
- **Focus:** RAS (Reliability, Availability, Serviceability) testing, Lenovo collaboration, Node Manager power testing.
- **Files:**
    - `ICX_PO_Entrance_Exit_Criteria_PV_RAS.xlsx`: Validation criteria for Ice Lake RAS.
    - `ras-einj.txt`, `ras-viral.txt`: Notes on Error Injection and Viral error handling.
    - `workload_profile.py`: Script for profiling system workloads.

### **2020: IPMI & NetFn**
`raw_notes/2020/`
- **Focus:** IPMI NetFunction scanning.
- **Files:**
    - `scan_NetFunction_8-25-2020.py`: The main artifact for this year.

### **2021: MCTP & Redfish Transition**
`raw_notes/2021/`
- **Focus:** Transitioning from IPMI to Redfish/MCTP, OOBMSM (Out-of-Band Manageability Subsystem Module).
- **Files:**
    - `Future of MCTP Infrastructure.pptx`: Strategic deck on MCTP.
    - `OOBMSM_worksheet.xlsx`: Pinout/bus owner tracking for OOBMSM.
    - `redfish_utils.py`: Python library for Redfish interactions.
    - `Stressing Redfish PECI_demo.pptx`: Early demo of the PECI stress methodology.

### **2022: The Year of PECI**
`raw_notes/2022/`
- **Focus:** Heavy PECI validation, telemetry stress testing, custom tooling.
- **Files:**
    - `pecistressor.py`, `peciXtor.py`: The core stress tools.
    - `DTTC_Review.pdf`: (Related) Conference paper drafts.
    - `Jason Aurora Subsystem Execution Tracker.xlsx`: Execution tracking for Aurora program.
    - `miv_package/`: A full Python package for MIV (Manageability Infrastructure Validation).

### **2023: Blackbox & BMC Scripting**
`raw_notes/2023/`
- **Focus:** "Blackbox" recorder analysis, BMC-side scripting.
- **Files:**
    - `BMC SCript/`: Subfolder containing direct-on-BMC scripts (`getCrashdump.py`, `tpmi-peci.sh`).
    - `MIV for Execution.pptx`: Execution strategy deck.
    - `Backup -MIV Blackbox Recorder.pptx`: Documentation on flight recorder analysis.

### **2024: Current State**
`raw_notes/2024/`
- **Focus:** (Empty in raw folder, mostly in active `notes_2024.txt`).

---

## 5. Links
- **Portfolio:** [github.com/kEnder242/Portfolio_Dev](https://github.com/kEnder242/Portfolio_Dev)
- **HomeLabAI:** [github.com/kEnder242/HomeLabAI](https://github.com/kEnder242/HomeLabAI)
- **Decky Trailers:** [github.com/kEnder242/decky-trailers](https://github.com/kEnder242/decky-trailers)

---

## 6. Behavioral Q&A Key (Search Tags)
*Use the "Filter nodes..." box on the Field Manual to instantly find these stories.*

### **1. Obstacles & Persistence**
> "A time when you got stuck 75% through a project? Was it a successful one?"
- **Search Tag:** `stuck`, `obstacle`
- **Key Stories:** *The Cygwin Wall*, *The RAKP Security Catch*, *RMCP+ Socket Optimization*

### **2. Failure & Lessons**
> "Tell me about a time when you failed."
- **Search Tag:** `fail`, `failure`
- **Key Stories:** *The Failed Microsoft Demo*, *The PythonSV API Thrash*, *Negative Testing (Yield)* 

### **3. Ambiguity & Data**
> "Dealing with ambiguous situations / not enough data?"
- **Search Tag:** `ambiguity`, `data-driven`
- **Key Stories:** *Reading Like a Robot*, *Throughput Gotchas*, *The Beating Heart*

### **4. Vision & Strategy**
> "Laid out a vision when there wasn’t one?"
- **Search Tag:** `vision`, `strategy`
- **Key Stories:** *The Texas Power-On*, *To SCM or Not to SCM*, *The VISA Tool Engine*

### **5. Conflict Resolution**
> "Major disagreement with your boss."
- **Search Tag:** `conflict`, `disagreement`
- **Key Stories:** *The Conflict Management Lesson*, *The PythonSV API Thrash*, *Estimates: High vs. Low*

### **6. Growth & Improvement**
> "One thing you wish you’d improve on?"
- **Search Tag:** `improvement`, `growth`
- **Key Stories:** *General Thoughts & Philosophy*, *The Failed Microsoft Demo*

### **7. Challenge & Scale**
> "Most challenging project, program or initiative?"
- **Search Tag:** `challenge`, `scale`
- **Key Stories:** *Flashing 100 Nodes*, *The VISA Tool Engine*, *The RAKP Security Catch*

### **8. Learning Style**
> "How do you learn?"
- **Search Tag:** `learning`, `methodology`
- **Key Stories:** *How to Grok Code*, *Reinventing TI Basic*, *The Beating Heart*

### **9. Why NVIDIA?**
> "Why NVIDIA? / Fit"
- **Search Tag:** `fit`, `nvidia-fit`
- **Key Stories:** *Flashing 100 Nodes* (Scale), *RAPL & Matplotlib* (Telemetry), *Crazy Callbacks* (Performance)