from os import path
from core import API

import pathlib

app_directory = pathlib.Path(__file__).parent.resolve()

source_api = API.GitHub
source_api_url = ""
source_api_user = ""
source_api_access_token = ""

mirror_api = API.GitHub
mirror_api_url = ""
mirror_api_user = ""
mirror_api_access_token = "" # Scope(repo: Full control of private repositories)
mirror_api_enabled = False

mirror_api_2 = API.GitHub_Enterprise
mirror_api_url_2 = ""
mirror_api_user_2 = ""
mirror_api_access_token_2 = "" # Scope(repo: Full control of private repositories)
mirror_api_enabled_2 = False

mirror_api_3 = API.GitLab
mirror_api_url_3 = ""
mirror_api_user_3 = ""
mirror_api_access_token_3 = "" # Scope(api, read_repository, write_repository)
mirror_api_enabled_3 = False

mirror_api_4 = API.GitLab_On_Premise
mirror_api_url_4 = ""
mirror_api_user_4 = ""
mirror_api_access_token_4 = ""
mirror_api_enabled_4 = False

mirror_api_5 = API.Bitbucket
mirror_api_url_5 = ""
mirror_api_user_5 = ""
mirror_api_access_token_5 = ""
mirror_api_enabled_5 = False