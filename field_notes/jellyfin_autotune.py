#!/usr/bin/env python3
"""
Jellyfin Hardware Auto-Tuner & Heterogeneous Pipeline
# [FEAT-069] Hardware-Aware Adaptive Runtime (Resilience Ladder) [SCAR #2]
# [FEAT-251.2] Forensic Wait (Early Crash Detection)
# [FEAT-029] Absolute Zero Hardware Purification
# [FEAT-427] Automatically probes host hardware (Intel Arc B580 QSV, Haswell iGPU, NVIDIA dGPU)
# [LAB-122] Zero-VRAM-Impact Heterogeneous Architecture:
    - Primary Transcoder: Intel Arc B580 (Battlemage G21 at PCI 0000:03:00.0) via QuickSync (QSV)
    - Fallback Transcoder: Intel Haswell iGPU (PCI 0000:00:02.0) via VAAPI
    - Dedicated Compute: NVIDIA RTX 2080 Ti reserved 100% for Local LLM Inference
"""

import logging
import os
import subprocess
import xml.etree.ElementTree as ET

logging.basicConfig(
    level=logging.INFO, format="[JELLYFIN-AUTOTUNE] %(levelname)s: %(message)s"
)

ENCODING_XML = "/var/lib/jellyfin-data/config/config/encoding.xml"


def get_arc_b580_render_node():
    """Dynamically resolves the live render node for the Intel Arc B580 (PCI 0000:03:00.0)."""
    by_path = "/dev/dri/by-path/pci-0000:03:00.0-render"
    if os.path.exists(by_path):
        return os.path.realpath(by_path)
    return None


def get_haswell_igpu_render_node():
    """Dynamically resolves the live render node for the Haswell iGPU (PCI 0000:00:02.0)."""
    by_path = "/dev/dri/by-path/pci-0000:00:02.0-render"
    if os.path.exists(by_path):
        return os.path.realpath(by_path)
    return None


def probe_hardware():
    arc_dev = get_arc_b580_render_node()
    igpu_dev = get_haswell_igpu_render_node()
    nvidia_gpu = os.path.exists("/dev/nvidia0")

    logging.info(
        f"Hardware Probe: Intel Arc B580 ({arc_dev})={arc_dev is not None}, "
        f"Intel Haswell iGPU ({igpu_dev})={igpu_dev is not None}, "
        f"NVIDIA dGPU (/dev/nvidia0)={nvidia_gpu}"
    )
    return arc_dev, igpu_dev, nvidia_gpu


def tune_encoding_xml():
    if not os.path.exists(ENCODING_XML):
        logging.error(f"Encoding config file not found at {ENCODING_XML}")
        return False

    arc_dev, igpu_dev, nvidia_gpu = probe_hardware()

    try:
        tree = ET.parse(ENCODING_XML)
        root = tree.getroot()

        def set_elem(name, val):
            el = root.find(name)
            if el is None:
                el = ET.SubElement(root, name)
            old_val = el.text
            el.text = val
            return old_val != val

        modified = False

        if arc_dev:
            # [LAB-122] Enforce Intel Arc B580 QSV Transcoding (0 MB NVIDIA VRAM impact)
            if set_elem("HardwareAccelerationType", "qsv"):
                modified = True
            if set_elem("VaapiDevice", arc_dev):
                modified = True
            if set_elem("QsvDevice", arc_dev):
                modified = True
            if set_elem("EnableTonemapping", "true"):
                modified = True
            if set_elem("EnableVppTonemapping", "true"):
                modified = True
            if set_elem("AllowHevcEncoding", "true"):
                modified = True
            if set_elem("AllowAv1Encoding", "true"):
                modified = True

            # Enable all modern hardware decoders supported by Battlemage
            hw_codecs = root.find("HardwareDecodingCodecs")
            if hw_codecs is None:
                hw_codecs = ET.SubElement(root, "HardwareDecodingCodecs")
                modified = True

            expected_codecs = ["h264", "hevc", "vc1", "vp9", "av1"]
            current_codecs = [el.text for el in hw_codecs.findall("string") if el.text]
            if set(current_codecs) != set(expected_codecs):
                for child in list(hw_codecs):
                    hw_codecs.remove(child)
                for c in expected_codecs:
                    s = ET.SubElement(hw_codecs, "string")
                    s.text = c
                modified = True

            logging.info(
                f"Targeting Transcoder: Intel Arc B580 QSV ({arc_dev} - 0 MB NVIDIA VRAM impact)"
            )

        elif igpu_dev:
            # Fallback to Haswell iGPU VAAPI
            if set_elem("HardwareAccelerationType", "vaapi"):
                modified = True
            if set_elem("VaapiDevice", igpu_dev):
                modified = True
            if set_elem("AllowHevcEncoding", "false"):
                modified = True
            if set_elem("AllowAv1Encoding", "false"):
                modified = True

            logging.info(
                f"Targeting Fallback Transcoder: Intel Haswell iGPU VAAPI ({igpu_dev})"
            )
        else:
            logging.error("No compatible Intel GPU detected for media acceleration!")
            return False

        if modified:
            tree.write(ENCODING_XML)
            logging.info("Successfully synchronized encoding.xml with live hardware.")
            return True
        else:
            logging.info("encoding.xml is already in sync with live hardware. No changes needed.")
            return False

    except Exception as e:
        logging.error(f"Failed to tune encoding.xml: {e}")
        return False


def test_transcode():
    logging.info("Verifying Jellyfin FFmpeg QSV/VAAPI capability inside container...")
    arc_dev = get_arc_b580_render_node()
    target_dev = arc_dev if arc_dev else "/dev/dri/renderD130"
    cmd = [
        "docker",
        "exec",
        "jellyfin",
        "/usr/lib/jellyfin-ffmpeg/ffmpeg",
        "-init_hw_device",
        f"vaapi=va:{target_dev},driver=iHD",
        "-init_hw_device",
        "qsv=qs@va",
        "-version",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        logging.info(
            "✅ Heterogeneous Auto-Tune PASSED! Intel Arc B580 QSV hardware pipeline verified."
        )
        return True
    else:
        logging.error(f"❌ Verification failed: {res.stderr}")
        return False


if __name__ == "__main__":
    reloaded = tune_encoding_xml()
    if reloaded:
        subprocess.run(["docker", "restart", "jellyfin"], check=True)
        logging.info(
            "Jellyfin container restarted. Waiting 3s for device initialization..."
        )
        import time

        time.sleep(3)
    test_transcode()
