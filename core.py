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
    # Return array of project ids
    if not isinstance(api, API):
        raise TypeError("TypeError: api must be of type: API(Enum)")
        exit(1)
    else:
        if(api == API.GitHub):
            request = requests.get("https://api.github.com/user/repos", headers = {"Authorization": f"token {api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                exit(1)

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

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                exit(1)

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
            request = requests.get("https://gitlab.com/api/v4/projects?owned=true", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                exit(1)

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
            request = requests.get(api_url + "/api/v4/projects?owned=true", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                return []

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
            print()

def CloneProjects(api, api_url, api_user, api_token):
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

def CreateMirrorProjects(api, api_url, api_user, api_token):
    if not isinstance(api, API):
        raise TypeError("TypeError: api must be of type: API(Enum)")
        exit(1)
    else:
        for namespace in os.scandir("repositories/"):
            namespace = namespace.name
            for project in os.scandir(f"repositories/{namespace}"):
                project = project.name
                
                if(api == API.GitHub):
                    request = requests.post("https://api.github.com/user/repos", headers = {"Authorization": f"token {api_token}"})

                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)
                
                elif(api == API.GitHub_Enterprise):
                    request = requests.post(api_url + "/user/repos", headers = {"Authorization": f"token {api_token}"})

                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)
                    
                elif(api == API.GitLab):
                    request = requests.get(f"https://gitlab.com/api/v4/namespaces?search={namespace}", headers = {"PRIVATE-TOKEN": f"{api_token}"})

                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)

                    json_object = json.loads(request.text)
                    
                    for user in json_object:
                        for key, value in user.items():
                            namespace_id = user["id"]

                    request = requests.post("https://gitlab.com/api/v4/projects", headers = {"PRIVATE-TOKEN": f"{api_token}"}, data = {"path": f"{project}", "namespace_id": f"{namespace_id}", "visibility": "private", "lfs_enabled": "true"})
                    
                    print(request.text)
                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)

                elif(api == API.GitLab_On_Premise):
                    request = requests.get(api_url + f"/api/v4/namespaces?search={namespace}", headers = {"PRIVATE-TOKEN": f"{api_token}"})

                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)

                    json_object = json.loads(request.text)
                    
                    for user in json_object:
                        for key, value in user.items():
                            namespace_id = user["id"]

                    request = requests.post("https://gitlab.com/api/v4/projects", headers = {"PRIVATE-TOKEN": f"{api_token}"}, data = {"path": f"{project}", "namespace_id": f"{namespace_id}", "visibility": "private", "lfs_enabled": "true"})
                    
                    print(request.text)
                    if request.status_code == 401:
                        print("HTTP Status: " + str(request.status_code))
                        exit(1)

                elif(api == API.Bitbucket):
                    print()

        # Loop namespace by folder.
            # Loop projects by folder
                # Create project
                    # POST /projects (https://docs.gitlab.com/ee/api/projects.html#create-project)
                    # path
                    # namespace_id

def MirrorProjects(api, api_url, api_user, api_token):
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