# remove_identical_files
This Python3 script removes any file from SOURCE if it matches the relative path and SHA1 hash with a file in TARGET.

## Syntax
`python remove_identical_files.py SOURCE TARGET [-r]`

1) Scans folder `SOURCE` and creates a hashlist of the contained files together with their relative paths
2) Scans folder `TARGET` and compares the files' hash/relpath with the dict built in step 1
3) Files whose hash/relpath matches are listed
4) User can choose to delete these files in `SOURCE`

### Additional arguments
-r: perform action recursively on the folders

#### Attention
At the current stage no error handling is performed. This script was made for internal use.
