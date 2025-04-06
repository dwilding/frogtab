#!/usr/bin/env python

from pathlib import Path
import os

import frogtab


def main():
    ports_path = Path(os.getenv("SNAP_COMMON")) / "ports"
    ports = ports_path.read_text().splitlines()
    ports_path.write_text("")
    for port in ports:
        try:
            frogtab.stop(int(port))
        except frogtab.WrongAppError:
            pass


if __name__ == "__main__":
    main()
