#! /usr/bin/env python
import time


def shell_run():
    import os
    import subprocess


    cmd = "~/catkin_ws/devel/test_sh.sh"
    rc = subprocess.run(cmd, shell = True)


if __name__ == "__main__":
    shell_run()