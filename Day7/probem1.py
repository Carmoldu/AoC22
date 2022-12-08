from dataclasses import dataclass
import re
import sys
from tqdm import tqdm

sys.setrecursionlimit(2000)

COMMAND_MARKER = '$'
COMMAND_MARKER_CD = 'cd'
COMMAND_MARKER_LS = 'ls'
COMMAND_LABEL_START = 2
COMMAND_LABEL_END = 3 
COMMAND_CONTENT_START = 5

COMMAND_DIR_UP = '..'
COMMAND_IS_DIR = 'dir'

TOTAL_DISK = 70000000
UPDATE_SPACE = 30000000


def import_input(file: str) -> list[str]:
    with open(file) as f:
        return [line.replace('\n', '') for line in f.readlines()]

@dataclass
class File():
    name: str
    size: int

class Folder():
    existing_folders = []

    def __init__(self, name: str, parent_dir):
        self.name = name
        self.parent_dir = parent_dir
        self.child_folders = []
        self.files = []

    def create_file(self, file: str, size: int) -> None:
        self.files.append(File(file, size))

    def create_child_folder(self, name: str):
        folder = Folder(name, self)
        self.child_folders.append(folder)
        return folder

    def compute_size(self) -> int:
        size = 0
        size += sum([file.size for file in self.files])
        size += sum([folder.compute_size() for folder in self.child_folders])

        return size

    def find_child_folder(self, name):
        return next((folder for folder in self.child_folders if folder.name == name), None)

    def print_folder_structure(self, n_tabs: int = 0) -> None:
        tabs = '\t' * n_tabs
        print(f'{tabs}- {self.name}, (dir)')

        for file in self.files:
            print(f'{tabs}\t- {file.name}, (file, size {file.size})')

        for folder in self.child_folders:
            folder.print_folder_structure(n_tabs + 1)

    def __repr__(self):
        return self.name



def process_input(lines, current_folder: Folder = None, existing_folders = []):
    if len(lines) == 0:
        return current_folder, existing_folders

    current_line = lines.pop(0)
    
    if current_line[COMMAND_LABEL_START:COMMAND_LABEL_END + 1] == COMMAND_MARKER_CD:
        current_folder, existing_folders = manage_cd(current_line[COMMAND_CONTENT_START:], current_folder, existing_folders)

    elif current_line[COMMAND_LABEL_START:COMMAND_LABEL_END + 1] == COMMAND_MARKER_LS:
        pass # Nothing actually happens on ls lines

    else:
        existing_folders = manage_ls_output(current_line, current_folder, existing_folders)

    process_input(lines, current_folder, existing_folders)

    return current_folder, existing_folders

        
def manage_cd(line_command, current_folder, existing_folders):
    # Manage changing directory up
    if line_command == COMMAND_DIR_UP:
        current_folder = current_folder.parent_dir

    # Manage changing to child folder
    else:
        # if there is no current folder we must create it.
        # this should only happen for the root folder
        if current_folder is None:
            current_folder = Folder(line_command, current_folder)
            existing_folders.append(current_folder)
        else:
            current_folder = current_folder.find_child_folder(line_command)

    return current_folder, existing_folders

    
def manage_ls_output(current_line, current_folder, existing_folders):
    if current_line[:3] == COMMAND_IS_DIR:
        new_folder = current_folder.create_child_folder(current_line[4:])
        existing_folders.append(new_folder)
        
    else:
        file_name = re.findall(r'[^\s\d]+', current_line)[0]
        file_size = int(re.findall('\d+', current_line)[0])
        current_folder.create_file(file_name, file_size)

    return existing_folders


def main():
    input_file = 'Day7/input.txt'
    lines = import_input(input_file)
    root_folder, folders = process_input(lines)

    root_folder.print_folder_structure()

    added_size = 0
    folder_sizes = {}
    for folder in tqdm(folders, desc='Processing folder sizes...'):
        folder_sizes[folder] = folder.compute_size()

        if folder_sizes[folder] < 100000:
            added_size += folder_sizes[folder]

    print(added_size)

    total_space_used = folder_sizes[list(folder_sizes.keys())[0]]
    remaining_space = TOTAL_DISK - total_space_used
    extra_space_required = UPDATE_SPACE - remaining_space

    if extra_space_required <= 0:
        raise ValueError('No extra space is required!')

    folder_to_erase = None
    folder_to_erase_size = float('inf')
    for folder, folder_size in folder_sizes.items():
        if (folder_size >= extra_space_required) and (folder_size < folder_to_erase_size):
            folder_to_erase = folder

    print(folder_sizes[folder_to_erase])
    
    




if __name__ == '__main__':
    main()



