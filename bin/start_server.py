#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from server.server_main import main

if __name__ == "__main__":
    main()