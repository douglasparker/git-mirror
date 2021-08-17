import json
import os
import requests # Apache 2.0 License: https://docs.python-requests.org/en/master/
import shutil
import subprocess
from enum import Enum

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
    else:
        if(api == API.GitHub):
            request = requests.get("https://api.github.com/user/repos", headers = {"Authorization": f"token {api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                return []

            json_object = json.loads(request.text)

            project_urls = []
            for project in json_object:
                for key, value in project.items():

                    if project["clone_url"] not in project_urls:
                        project_urls.append(project["clone_url"])

            return project_urls

        elif(api == API.GitHub_Enterprise):
            request = requests.get(api_url + "/user/repos", headers = {"Authorization": f"token {api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                return []

            json_object = json.loads(request.text)

            project_urls = []
            for project in json_object:
                for key, value in project.items():

                    if project["clone_url"] not in project_urls:
                        project_urls.append(project["clone_url"])

            return project_urls

        elif(api == API.GitLab):
            request = requests.get("https://gitlab.com/api/v4/projects?owned=true", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                return []

            json_object = json.loads(request.text)

            project_urls = []
            for project in json_object:
                for key, value in project.items():

                    if project["http_url_to_repo"] not in project_urls:
                        project_urls.append(project["http_url_to_repo"])

            return project_urls

        elif(api == API.GitLab_On_Premise):
            request = requests.get(api_url + "/api/v4/projects?owned=true", headers = {"PRIVATE-TOKEN": f"{api_token}"})

            if request.status_code == 401:
                print("HTTP Status: " + str(request.status_code))
                return []

            json_object = json.loads(request.text)

            project_urls = []
            for project in json_object:
                for key, value in project.items():

                    if project["http_url_to_repo"] not in project_urls:
                        project_urls.append(project["http_url_to_repo"])

            return project_urls

        elif(api == API.Bitbucket):
            print()

def CloneProjects(api, api_url, api_user, api_token):
    for project_url in GetProjects(api, api_url, api_user, api_token):
        # Add api_user:token@ between https:// and the url
        clone_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]

        # WIP: Fix this
        #if project_url.find("https://"):
        #    clone_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]
        #else:
        #    clone_url = project_url[0: 7:] + api_user + ":" + api_token + "@" + project_url[7:]

        clone_directory = clone_url[clone_url.rfind('/')+1: clone_url.find('.git'):]
        subprocess.call(f"git clone {clone_url} ./repositories/{clone_directory}", shell=True)

def MirrorProjects(api, api_url, api_user, api_token):
    for project_url in GetProjects(api, api_url, api_user, api_token):
        # Get the project name from the project url.
        project_name = project_url[project_url.rfind('/')+1: project_url.find('.git'):]

        for cloned_directory in os.listdir("./repositories"):

            if(cloned_directory == project_name):
                mirror_url = project_url[0: 8:] + api_user + ":" + api_token + "@" + project_url[8:]
                # Make this work with Windows. cd is unix only.
                subprocess.call(f"cd repositories/{cloned_directory} && git remote add mirror {mirror_url} && cd -", shell=True)
                subprocess.call(f"cd repositories/{cloned_directory} && git push mirror master && cd -", shell=True)
                subprocess.call(f"cd repositories/{cloned_directory} && git push mirror release && cd -", shell=True)
                subprocess.call(f"cd repositories/{cloned_directory} && git lfs push --all mirror && cd -", shell=True)

def MirrorCreateProjects(api, api_url, api_user, api_token):
    print("MirrorCreateProjects() is not implemented.")

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