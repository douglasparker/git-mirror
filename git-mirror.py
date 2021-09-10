#!/usr/bin/env python3

from enum import Enum

import json
import os
import requests # Apache 2.0 License: https://docs.python-requests.org/en/master/
import shutil
import subprocess

import cfg as configuration

if not os.path.isfile(f"{configuration.app_directory}/cfg.py"):
    shutil.copy(f"{configuration.app_directory}/cfg.template.py", f"{configuration.app_directory}/cfg.py")
    print("A configuration file was created. Please edit this file and then rerun the program.")
    exit(1)


from core import API, CloneProjects, CreateMirrorProjects, MirrorProjects, Cleanup

CloneProjects(configuration.source_api, configuration.source_api_url, configuration.source_api_user, configuration.source_api_access_token)

CreateMirrorProjects(configuration.mirror_api, configuration.mirror_api_url, configuration.mirror_api_user, configuration.mirror_api_access_token, configuration.mirror_api_enabled)
MirrorProjects(configuration.mirror_api, configuration.mirror_api_url, configuration.mirror_api_user, configuration.mirror_api_access_token, configuration.mirror_api_enabled)

CreateMirrorProjects(configuration.mirror_api_2, configuration.mirror_api_url_2, configuration.mirror_api_user_2, configuration.mirror_api_access_token_2, configuration.mirror_api_enabled_2)
MirrorProjects(configuration.mirror_api_2, configuration.mirror_api_url_2, configuration.mirror_api_user_2, configuration.mirror_api_access_token_2, configuration.mirror_api_enabled_2)

CreateMirrorProjects(configuration.mirror_api_3, configuration.mirror_api_url_3, configuration.mirror_api_user_3, configuration.mirror_api_access_token_3, configuration.mirror_api_enabled_3)
MirrorProjects(configuration.mirror_api_3, configuration.mirror_api_url_3, configuration.mirror_api_user_3, configuration.mirror_api_access_token_3, configuration.mirror_api_enabled_3)

CreateMirrorProjects(configuration.mirror_api_4, configuration.mirror_api_url_4, configuration.mirror_api_user_4, configuration.mirror_api_access_token_4, configuration.mirror_api_enabled_4)
MirrorProjects(configuration.mirror_api_4, configuration.mirror_api_url_4, configuration.mirror_api_user_4, configuration.mirror_api_access_token_4, configuration.mirror_api_enabled_4)

CreateMirrorProjects(configuration.mirror_api_5, configuration.mirror_api_url_5, configuration.mirror_api_user_5, configuration.mirror_api_access_token_5, configuration.mirror_api_enabled_5)
MirrorProjects(configuration.mirror_api_5, configuration.mirror_api_url_5, configuration.mirror_api_user_5, configuration.mirror_api_access_token_5, configuration.mirror_api_enabled_5)

Cleanup()