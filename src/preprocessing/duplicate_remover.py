import os
import hashlib
from tqdm import tqdm
import argparse
import pathlib


# gets the md5 hash for the given file
def get_md5_hash(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()


# counts and deletes the duplicate files in the dataset
def count_delete_duplicates(hash_dict, delete):
    unique = set()
    num_duplicates = 0
    for key, value in tqdm(hash_dict.items(), bar_format='{l_bar}{bar:20}', desc='Counting duplicate files'):
        if value in unique:
            num_duplicates += 1
            if delete:
                os.remove(key)
        else:
            unique.add(value)
    return num_duplicates


# returns a list of all files in dir and subdirs
def get_list_of_files(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for file in listOfFile:
        if file.startswith('.'):
            continue
        else:
            # Create full path
            fullPath = os.path.join(dirName, file)
            # If file is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + get_list_of_files(fullPath)
            else:
                allFiles.append(fullPath)
    return allFiles


def remove_duplicates(dataset_name, delete):
    num_of_files = 0
    hash_dict = {}
    for file_path in tqdm(get_list_of_files(dataset_name), bar_format='{l_bar}{bar:20}',desc='Getting hash values'):
        hash_dict[file_path] = get_md5_hash(file_path)
        num_of_files += 1
    print('Total number of files:',num_of_files)
    if delete:
        print('Duplicate files delete:',count_delete_duplicates(hash_dict,delete))
    else:
        print('Number of duplicate files:', count_delete_duplicates(hash_dict,delete))


def get_arguments():
    parser = argparse.ArgumentParser(description='Removes duplicate files from directory.')
    parser.add_argument('action', help='delete or count duplicates', choices=['del','count'])
    parser.add_argument('datapath', help='path to dataset',type=pathlib.Path)
    args = parser.parse_args()
    datapath = args.datapath
    action = args.action
    return  datapath,action


def main():
    datapath,action = get_arguments()
    if action == 'del':
        # delete duplicates
        remove_duplicates(datapath, delete=True)
    elif action == 'count':
        # print number of duplicates
        remove_duplicates(datapath, delete=False)


if __name__ == '__main__':
    main()