#!/usr/bin/env python3

import os
import subprocess
import re
import libcalamares
import glob


def detect_resolution():

    try:
        result = subprocess.run(
            ["xrandr", "--current"],
            capture_output=True,
            text=True,
            check=True
        ).stdout
        patern = "primary\\D+(\\d+x\\d+)"
        return re.search(patern, result).group(1)
        
    except Exception as e:
        libcalamares.utils.warning(f"xrandr failed: {e}")



def run():

    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

    if not root_mount_point:
        return "Root mount point not found"

    libcalamares.utils.debug(
        f"Target root: {root_mount_point}"
    )

    # --------------------
    # Detect resolution
    # --------------------

    resolution = detect_resolution()

    if resolution:

        output_file = os.path.join(
            root_mount_point,
            "tmp",
            "grub_res"
        )

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        with open(output_file, "w") as f:
            f.write(resolution)

        libcalamares.utils.debug(
            f"Resolution {resolution} saved"
        )

    else:
        libcalamares.utils.warning(
            "Resolution detection failed"
        )

    # --------------------
    # Install package
    # --------------------

    package_path = "/opt/ezrepo/grub-theme-Nyarch"

    try:

        pkg = glob.glob("/opt/ezrepo/grub-theme-Nyarch*.pkg.tar.zst")[0]

        cmd = [
            "pacman",
            "-U",
            "--noconfirm",
            pkg
        ]


        libcalamares.utils.debug(
            f"Running: {' '.join(cmd)}"
        )
        
        result = libcalamares.utils.target_env_call(cmd)

        if result != 0:
            return "Failed to install grub theme package"

    except Exception as e:
        return f"Pacman failed: {e}"

    return None

