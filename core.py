import json
import os
import requests # Apache 2.0 License: https://docs.python-requests.org/en/master/
import shutil
import subprocess
import time
from enum import Enum

from requests.models import Response

class API(Enum):
    GitHub = 1
    GitHub_Enterprise = 2
    GitLab = 3
    GitLab_On_Premise = 4
    Bitbucket = 5

def GetProjects(api, api_url, api_user, api_token):
    print(f"  Getting Projects  from {api.name}...")
    if not api:
        print("Error: An API endpoint must be configured.")
        return 1
    
    if api is API.GitHub_Enterprise and not api_url or api is API.GitLab_On_Premise and not api_url:
        print("An API URL must be configured for the specified API endpoint.")
        return 1

    if not api_user:
        print("Error: A user must be configured for the specified API endpoint.")
        return 1
    
    if not api_token:
        print("Error: An API token must be configured for the specified API endpoint.")
        return 1

    if not isinstance(api, API):
        raise TypeError("Type Error: api must be of type: API(Enum)")
        return 1

    else:
        if(api == API.GitHub):
            request = requests.get("https://api.github.com/user/repos", headers = {"Authorization": f"token {api_token}"})

            print("HTTP Status: " + str(request.status_code) + " - " + request.url)
            print("HTTP Response: " + request.text)

            if request.status_code == 401:
                return 1

            json_object = json.loads(request.text)

            project_urls = []
            project_namespaces = []
            project_names = []
            
            for project in json_object:
                for key, value in project.items():

                    if project["clone_url"] not in project_urls:
                        project_urls.append(project["clone_url"])
                        project_namespaces.append(project["owner"]["login"])
                        project_names.append(project["name"])

            return [project_urls, project_namespaces, project_names]

        elif(api == API.GitHub_Enterprise):
            request = requests.get(api_url + "/user/repos", headers = {"Authorization": f"token {api_token}"})

            print("HTTP Status: " + str(request.status_code) + " - " + request.url)
            print("HTTP Response: " + request.text)

            if request.status_code == 401:
                return 1

            json_object = json.loads(request.text)

            project_urls = []
            project_namespaces = []
            project_names = []
            
            for project in json_object:
                for key, value in project.items():

                    if project["clone_url"] not in project_urls:
                        project_urls.append(project["clone_url"])
                        project_namespaces.append(project["owner"]["login"])
                        project_names.append(project["name"])

            return [project_urls, project_namespaces, project_names]

        elif(api == API.GitLab):
            request = requests.get("https://gitlab.com/api/v4/projects?owned=true&pagination=keyset&per_page=100&order_by=id&sort=asc", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            print("HTTP Status: " + str(request.status_code) + " - " + request.url)
            print("HTTP Response: " + request.text)

            if request.status_code == 401:
                return 1

            json_object = json.loads(request.text)

            project_urls = []
            project_namespaces = []
            project_names = []
            
            for project in json_object:
                for key, value in project.items():

                    if project["http_url_to_repo"] not in project_urls:
                        project_urls.append(project["http_url_to_repo"])
                        project_namespaces.append(project["namespace"]["path"])
                        project_names.append(project["path"])

            return [project_urls, project_namespaces, project_names]

        elif(api == API.GitLab_On_Premise):
            request = requests.get(api_url + "/api/v4/projects?owned=true&pagination=keyset&per_page=100&order_by=id&sort=asc", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            print("HTTP Status: " + str(request.status_code) + " - " + request.url)
            print("HTTP Response: " + request.text)

            if request.status_code == 401:
                return 1

            json_object = json.loads(request.text)

            project_urls = []
            project_namespaces = []
            project_names = []
            
            for project in json_object:
                for key, value in project.items():

                    if project["http_url_to_repo"] not in project_urls:
                        project_urls.append(project["http_url_to_repo"])
                        project_namespaces.append(project["namespace"]["path"])
                        project_names.append(project["path"])

            return [project_urls, project_namespaces, project_names]

        elif(api == API.Bitbucket):
            print("Bitbucket is not currently supported.")

def CloneProjects(api, api_url, api_user, api_token):
    print(f"Cloning Projects from {api.name}...")

    if not api:
        print("  [Error]: An API endpoint must be configured.")
        return 1
    
    if api is API.GitHub_Enterprise and not api_url or api is API.GitLab_On_Premise and not api_url:
        print("  [Error]: An API URL must be configured for the specified API endpoint.")
        return 1

    if not api_user:
        print("  [Error]: A user must be configured for the specified API endpoint.")
        return 1
    
    if not api_token:
        print("  [Error]: An API token must be configured for the specified API endpoint.")
        return 1

    if not isinstance(api, API):
        raise TypeError("  [Error]: api must be of type: API(Enum)")
        return 1

    else:
        project_data = GetProjects(api, api_url, api_user, api_token)

        for project_url in project_data[0]:
                namespace = project_data[1][project_data[0].index(project_url)]
                project = project_data[2][project_data[0].index(project_url)]

                # Add api_user:token@ between https:// and the url
                clone_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]

                # WIP: Fix this
                #if project_url.find("https://"):
                #    clone_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]
                #else:
                #    clone_url = project_url[0: 7:] + api_user + ":" + api_token + "@" + project_url[7:]

                if not os.path.exists("repositories"): os.mkdir("repositories")
                if not os.path.exists(f"repositories/{namespace}"): os.mkdir(f"repositories/{namespace}")

                subprocess.call(f"git clone --mirror {clone_url} {project}", cwd=f"repositories/{namespace}", shell=True)
                subprocess.call(f"git lfs fetch --all", cwd=f"repositories/{namespace}/{project}", shell=True)

def CreateMirrorProjects(api, api_url, api_user, api_token, api_enabled):
    print(f"Creating Mirror Projects for {api.name}...")
    if not api_enabled:
        print("  [Info]: This API endpoint is disabled.")
        return 0

    if not api:
        print("  [Error]: An API endpoint must be configured.")
        return 1
    
    if api is API.GitHub_Enterprise and not api_url or api is API.GitLab_On_Premise and not api_url:
        print("  [Error]: An API URL must be configured for the specified API endpoint.")
        return 1

    if not api_user:
        print("  [Error]: A user must be configured for the specified API endpoint.")
        return 1
    
    if not api_token:
        print("  [Error]: An API token must be configured for the specified API endpoint.")
        return 1

    if not isinstance(api, API):
        raise TypeError("Type Error: api must be of type: API(Enum)")
        return 1

    else:
        for namespace in os.scandir("repositories/"):
            namespace = namespace.name
            for project in os.scandir(f"repositories/{namespace}"):
                project = project.name
                
                if(api == API.GitHub):
                    request = requests.post(f"https://api.github.com/orgs/{namespace}/repos", headers = {"Authorization": f"token {api_token}"}, data = json.dumps({"name": f"{project}", "description": "", "private": "true", "org": f"{namespace}", "has_issues": "false", "has_projects": "false", "has_wiki": "false"}))
                    
                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                    if request.status_code == 404:
                        request = requests.post(f"https://api.github.com/user/repos", headers = {"Authorization": f"token {api_token}"}, data = json.dumps({"name": f"{project}", "description": "", "private": "true", "has_issues": "false", "has_projects": "false", "has_wiki": "false"}))
                        
                        print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                        print("HTTP Response: " + request.text)
                
                elif(api == API.GitHub_Enterprise):
                    request = requests.post(api_url + f"/orgs/{namespace}/repos", headers = {"Authorization": f"token {api_token}"}, data = json.dumps({"name": f"{project}", "description": "", "private": "true", "org": f"{namespace}", "has_issues": "false", "has_projects": "false", "has_wiki": "false"}))
                    
                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                    if request.status_code == 404:
                        request = requests.post(api_url + f"/user/repos", headers = {"Authorization": f"token {api_token}"}, data = json.dumps({"name": f"{project}", "description": "", "private": "true", "has_issues": "false", "has_projects": "false", "has_wiki": "false"}))
                        
                        print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                        print("HTTP Response: " + request.text)
                    
                elif(api == API.GitLab):
                    request = requests.get(f"https://gitlab.com/api/v4/namespaces?search={namespace}", headers = {"PRIVATE-TOKEN": f"{api_token}"})

                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                    json_object = json.loads(request.text)
                    
                    for user in json_object:
                        for key, value in user.items():
                            namespace_id = user["id"]

                    request = requests.post("https://gitlab.com/api/v4/projects", headers = {"PRIVATE-TOKEN": f"{api_token}"}, data = {"path": f"{project}", "namespace_id": f"{namespace_id}", "visibility": "private", "lfs_enabled": "true"})

                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                elif(api == API.GitLab_On_Premise):
                    request = requests.get(api_url + f"/api/v4/namespaces?search={namespace}", headers = {"PRIVATE-TOKEN": f"{api_token}"})

                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                    json_object = json.loads(request.text)
                    
                    for user in json_object:
                        for key, value in user.items():
                            namespace_id = user["id"]

                    request = requests.post("https://gitlab.com/api/v4/projects", headers = {"PRIVATE-TOKEN": f"{api_token}"}, data = {"path": f"{project}", "namespace_id": f"{namespace_id}", "visibility": "private", "lfs_enabled": "true"})
                    
                    print("HTTP Status: " + str(request.status_code) + " - " + request.url)
                    print("HTTP Response: " + request.text)

                    if request.status_code == 401:
                        return 1

                elif(api == API.Bitbucket):
                    print("Bitbucket is not currently supported.")

def MirrorProjects(api, api_url, api_user, api_token, api_enabled):
    print(f"Mirroring Projects for {api.name}...")
    if not api_enabled:
        print("  [Info]: This API endpoint is disabled.")
        return 0

    if not api:
        print("  [Error]: An API endpoint must be configured.")
        return 1
    
    if api is API.GitHub_Enterprise and not api_url or api is API.GitLab_On_Premise and not api_url:
        print("  [Error]: An API URL must be configured for the specified API endpoint.")
        return 1

    if not api_user:
        print("  [Error]: A user must be configured for the specified API endpoint.")
        return 1
    
    if not api_token:
        print("  [Error]: An API token must be configured for the specified API endpoint.")
        return 1

    if not isinstance(api, API):
        raise TypeError("  [Error]: api must be of type: API(Enum)")
        return 1

    else:
        project_data = GetProjects(api, api_url, api_user, api_token)
        for project_url in project_data[0]:
            namespace = project_data[1][project_data[0].index(project_url)]
            project = project_data[2][project_data[0].index(project_url)]

            if(os.path.exists(f"repositories/{namespace}/{project}")):
                
                mirror_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]

                # Push LFS objects first, or pushing the mirror will fail.
                subprocess.call(f"git lfs push --all {mirror_url}", cwd=f"repositories/{namespace}/{project}", shell=True)
                subprocess.call(f"git push --mirror {mirror_url}", cwd=f"repositories/{namespace}/{project}", shell=True)

def GetProject(api, url):
    # Return array of project http_url_to_repo (json)
    # curl --header "PRIVATE-TOKEN: <your_access_token>" "https://gitlab.com/api/v4/projects/:id"
    print("GetProject() is not implemented.")

def CloneProject(url, lfs = False):
    print("CloneProject() is not implemented.")
    
def MirrorProject():
    print("MirrorProject() is not implemented.")

def Cleanup():
    if os.path.exists("repositories/"):
        shutil.rmtree("repositories/")