import sys
import os
import hashlib

# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

# https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them
def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

# inspired by https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them
def remove_identical_files(path_from, path_to, other_args = None, hash=hashlib.sha1):
    hashes = {}

    if other_args == '-r':
        allTargetFiles = getListOfFiles(path_to)
        allSourceFiles = getListOfFiles(path_from)
    else:
        allTargetFiles = [os.path.join(path_to, f) for f in os.listdir(path_to) if os.path.isfile(os.path.join(path_to, f))]
        allSourceFiles = [os.path.join(path_from, f) for f in os.listdir(path_from) if os.path.isfile(os.path.join(path_from, f))]

    for filepath in allTargetFiles:
        hashobj = hash()
        for chunk in chunk_reader(open(filepath, 'rb')):
            hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(filepath), os.path.relpath(filepath, path_to))
        hashes[file_id] = filepath

    files_to_delete = []

    for filepath in allSourceFiles:
        hashobj = hash()
        for chunk in chunk_reader(open(filepath, 'rb')):
            hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(filepath), os.path.relpath(filepath, path_from))
        duplicate = hashes.get(file_id, None)
        if duplicate:
            print('"{}"'.format(filepath))
            print('<==> "{}"'.format(duplicate))            
            files_to_delete.append(filepath)

    print()
    print('Summary:')
    for f in files_to_delete:
        print(f)

    c = input("Remove these files? [y/n] ")
    if c == 'y':
        for f in files_to_delete:
            os.remove(f)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('usage: python remove_identical_files.py SOURCE TARGET [-r]')
        print()
        print('The script performs these steps:')
        print('1) Scan folder TARGET and create a hashlist of the contained files together with their relative paths')
        print("2) Scan folder SOURCE and compare the files' hash/relpath with the dict built in step 1.")
        print('3) Files whose hash/relpath matches are listed')
        print('4) User can choose to delete these files in SOURCE')
        print()
        print('-r: perform action recursively on the folders')
    if len(sys.argv) == 3:
        remove_identical_files(sys.argv[1], sys.argv[2], other_args = None)
    elif len(sys.argv) == 4:
        remove_identical_files(sys.argv[1], sys.argv[2], other_args = sys.argv[3])
    else:
        print('Wrong number of arguments.')