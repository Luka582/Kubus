import os
import json

class Project():
    def __init__(self, path:str, static_url):
        self.id = 0
        images_list = os.listdir(os.path.join(path,"img"))
        images_list.sort()
        self.images = [os.path.join(path,"img",x).replace(static_url + "/", "") for x in images_list]
        with open(os.path.join(path,"data.json")) as data:
            self.data = json.load(data)
    def set_id(self,id):
        self.id = id

if __name__ == "__main__":
    example_project = Project("static/project_1")
    print(example_project.images)
    print(example_project.data)