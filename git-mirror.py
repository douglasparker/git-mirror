#!/usr/bin/env python3

import json
import requests # Apache 2.0 License: https://docs.python-requests.org/en/master/
import subprocess
from enum import Enum
from core import API, CloneProjects, MirrorProjects, Cleanup

source_api = API.GitHub
source_api_url = ""
source_api_user = ""
source_api_access_token = ""

mirror_api = API.GitLab
mirror_api_url = ""
mirror_api_user = ""
mirror_api_access_token = ""

CloneProjects(source_api, source_api_url, source_api_user, source_api_access_token)

MirrorProjects(mirror_api, mirror_api_url, mirror_api_user, mirror_api_access_token)

Cleanup()