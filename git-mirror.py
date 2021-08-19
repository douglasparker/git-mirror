#!/usr/bin/env python3

import json
import os
import requests # Apache 2.0 License: https://docs.python-requests.org/en/master/
import shutil
import subprocess
from enum import Enum

if not os.path.isfile("cfg.py"):
    shutil.copy("cfg.template.py", "cfg.py")
    print("A configuration file was created. Please edit this file and then rerun the program.")
    exit(1)

import cfg as configuration
from core import API, CloneProjects, MirrorProjects, Cleanup

CloneProjects(configuration.source_api, configuration.source_api_url, configuration.source_api_user, configuration.source_api_access_token)

MirrorProjects(configuration.mirror_api, configuration.mirror_api_url, configuration.mirror_api_user, configuration.mirror_api_access_token)

Cleanup()