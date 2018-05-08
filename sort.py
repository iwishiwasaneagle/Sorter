from __future__ import print_function
import os, json
from subprocess import call

class sort:
    def __init__(self):
        self.toIgnore = ["sort.py", "sort.json", ".git"]
        self.cats = ["Code", "Zip", "Image", "Video", "Doc", "Ignore"]
        self.files = [f for f in os.listdir(os.getcwd()) if (not os.path.isdir(f) and f not in self.toIgnore)]
        self.dirs = [f for f in os.listdir(os.getcwd()) if (os.path.isdir(f) and f not in self.toIgnore and f not in self.cats and f!="Folders")]
        self.default = {'Doc': ['xlsx', 'pdf', 'docx'], 'Image': ['png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG'], 'Code': ['py', 'c'], 'Video': ['mp4', 'avi', 'mkv'], "Zip": ["zip", "tar", "rar", "gz", "xz", "iso", "deb", "rpm"], "Ignore": []}
        self.sort = {}

        self.confFile = "sort.json"

        if not os.path.isfile(self.confFile):
            with open(self.confFile, 'w') as file:
                json.dump(self.default, file)
            self.sort = self.default
        else:
            with open(self.confFile, 'r') as file:
                self.sort = json.load(file)

        for c in self.cats:
            if c not in os.listdir(os.getcwd()) and c != "Ignore":
                os.makedirs(c)

    def sorter(self):
        temp = self.files
        for key in self.cats:
            toMove = [f for f in self.files if f.split('.')[-1] in self.sort[key]]
            if key == "Ignore":
                for file in toMove:
                    temp.remove(file)
            else:
                for file in toMove:
                    os.rename(os.path.join(os.getcwd(),file), os.path.join(os.getcwd(), key, file))
                    temp.remove(file)


        self.nah = temp

    def moveBitchAkaMoveFolders(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "Folders")):
            os.makedirs(os.path.join(os.getcwd(), "Folders"))

        for folder in self.dirs:
            os.rename(os.path.join(os.getcwd(), folder), os.path.join(os.getcwd(), "Folders", folder))

    def doesntExist(self, wut):

        formats = list(set([f.split('.')[-1] for f in wut if (not os.path.isdir(f))]))

        print ("Some file extensions haven't been recognized. Would you like to add them to the database? [Y]es/[N]o")
        choice = raw_input("-> ").lower()
        if choice == 'n':
            pass
        elif choice == 'y':
            print("\n Each file extension will be print. Enter a number corresponding to the catagory from the list below and press enter.")
            temp = {}
            for key in range(len(self.cats)):
                if not self.cats[key] == "Ignore":
                    print (str(key)+")", self.cats[key])
                    temp[key] = self.cats[key]
            print("To permanently ignore a format, enter ", len(self.cats)-1)
            print("To exit, press \"Q\"")
            for form in formats:
                whereTo = (raw_input(form+": "))
                if whereTo.lower() == "q":
                    break
                whereTo = int(whereTo)
                while whereTo not in range(len(self.cats)):
                    print ("Sorry that isn't a valid option. Would you like to try again for type "+str(form)+"? [Y]es/[N]o")
                    choice = raw_input("-> ")
                    while choice.lower() not in ["y", "n"]:
                        print ("Sorry that isn't a valid option. Would you like to try again for type "+str(form)+"? [Y]es/[N]o")
                        choice = raw_input("-> ")

                    if choice.lower() == "n":
                        break
                    else:
                        whereTo = int(raw_input(form+": "))
                self.sort[temp[whereTo]].append(form)

        with open(self.confFile, 'w') as file:
            json.dump(self.sort, file)

        self.sorter()

    def main(self):
        self.sorter()
        self.moveBitchAkaMoveFolders()
        if len(self.nah) > 0:
            self.doesntExist(self.nah)


if __name__ == "__main__":
    sort_ = sort()
    sort_.main()
