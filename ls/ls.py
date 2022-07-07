#!/usr/bin/env python3
# Improved ls.
# based on "ls" & "stat".

# Import needed libraries:
import sys, os

# what is color? it is:
class Color():
        black = "\u001b[30m"
        red = "\u001b[31m"
        green = "\u001b[32m"
        yellow = "\u001b[33m"
        blue = "\u001b[34m"
        magenta = "\u001b[35m"
        cyan = "\u001b[36m"
        white = "\u001b[37m"
        reset = "\u001b[0m"

# what is Lister? it is:
class Lister(object):
    """Docstring for Lister. No documention avalable!"""
    def __init__(self):
        super(Lister, self).__init__()

        # initialize attributes:
        self.files_list = "" # "/bin/ls" output
        self.files_list_listed = list() # "/bin/ls" output list type
        self.files_path = "" # parent directory
        self.custom_path = "" # if user wanted other place files
        self.list_all_files = False # if True: "/bin/ls -A path" if False: "/bin/ls path"

        self.total_dir_size = "" # size of parent directory

        self.file = "" # every single file in the parent dir
        self.file_size = ""  # file size

        self.file_permissions = "" # permissions of this single file
        self.file_owner = ""  # owner of this single file
        self.file_is_dir = False # if this single file is a dir
        self.file_is_ln = False # if this single file is a symbol link
        self.file_is_exe = False # if this single file is an executable file
        self.file_has_s_perm = False # if this single file has "setuid" permission

        self.user = os.popen("/bin/echo $USER").read().rstrip()

    # methods:
    # fetch_argv finds out the files path (not validated)
    def fetch_argv(self):
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-a":
                self.list_all_files = True
            if os.path.isdir(sys.argv[i]):
                self.custom_path = sys.argv[i]
                self.custom_path += '/'

    # get the outputs based on argument given
    def fetch_list(self):
        if self.list_all_files == True:
            self.files_list = os.popen(f"/bin/ls -A {self.custom_path}{self.files_path} --color=never").read()
        else:
            self.files_list = os.popen(f"/bin/ls {self.custom_path}{self.files_path} --color=never").read()

        self.total_dir_size = os.popen(f"/bin/ls {self.custom_path} -lAh | /bin/grep total | /bin/cut -b 7-").read().rstrip()

    # convert the string to python list
    def string_to_list(self):
        self.files_list_listed = self.files_list.splitlines()

    # generate the output
    def generator(self):
        print("Total size is: " + Color.red + self.total_dir_size + Color.reset)
        for self.file in self.files_list_listed:
            file = self.file
            self.file_permissions = os.popen(f"/bin/stat -c %A {self.custom_path}{self.files_path}'{file}'").read().rstrip()
            self.perm_analizer()
            if self.file_is_ln:
                self.link_analizer()
            self.name_analizer()
            self.file_size = os.popen(f"/bin/stat -c %s {self.custom_path}{self.files_path}'{file}' | /bin/numfmt --to=iec").read().rstrip()
            self.format_size()
            self.file_owner = os.popen(f"/bin/stat -c '%U' {self.custom_path}{self.files_path}'{file}'").read().rstrip()
            self.owner()


            print(f"{self.file_permissions} {self.file_owner} {self.file_size} {self.file}")
    
    # analize the permissions
    def perm_analizer(self):
        perm = ""
        if "x" in self.file_permissions:
            self.file_is_exe = True
        for i, v in enumerate(self.file_permissions):
            if i == 0 and v == "d":
                perm += Color.blue + "d" + Color.reset
                self.file_is_dir = True
                self.file_is_exe = False
            elif i == 0 and v == "l":
                perm += Color.cyan + "l" + Color.reset
                self.file_is_ln = True
                self.file_is_exe = False
            elif v == "r":
                perm += Color.magenta + "r" + Color.reset
            elif v == "w":
                perm += Color.magenta + "w" + Color.reset
            elif v == "x":
                perm += Color.green + "x" + Color.reset
            elif v == "-":
                perm += Color.reset + "-"
            elif v == "s":
                perm += Color.yellow + "s" + Color.reset
                self.file_has_s_perm = True
                self.file_is_exe = False
            
        self.file_permissions = perm
    
    # analize the single file name
    def name_analizer(self):
        if self.file_is_dir:
            self.file = Color.blue + self.file + Color.reset
            self.file_is_dir = False
        elif self.file_is_ln:
            self.file = Color.cyan + self.file + Color.reset
            self.file_is_ln = False
        elif self.file_is_exe:
            self.file = Color.green + self.file + Color.reset
            self.file_is_exe = False
        elif self.file_has_s_perm:
            self.file = Color.yellow + self.file + Color.reset
            self.file_has_s_perm = False

    # analize the file behind the link
    def link_analizer(self):
        file = os.popen(f"/bin/readlink -f {self.custom_path}{self.files_path}'{self.file}'").read().rstrip()
        self.file = self.files_path + self.file + Color.reset + " -> " + "'" + self.files_path + file + "'"

    # format the size string
    def format_size(self):
        left = 6 - len(self.file_size)
        self.file_size = left*" " + self.file_size

    # check our user is the single file owner
    def owner(self):
        if self.file_owner == self.user:
            self.file_owner = Color.red + self.file_owner + Color.reset

# main function
def main():
    try:
        ls = Lister()
        ls.fetch_argv()
        if ls.custom_path == True:
            ls.validate_path()
        ls.fetch_list()
        ls.string_to_list()
        ls.generator()
        return 0
    except:
        return 1

# Run this code block if executed directly:
if __name__ == "__main__":
    main()
