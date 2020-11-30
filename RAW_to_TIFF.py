import rawpy
import imageio
import subprocess
import os.path
import logging
import glob

def check_for_path(path):
    if ~os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            return False
    return True

def filesearch(word=""):
    """Returns a list with all files with the word/extension in it"""
    logger.info('Starting filesearch')
    file = []
    for f in glob.glob("*"):
        if word[0] == ".":
            if f.endswith(word):
                file.append(f)

        elif word in f:
            file.append(f)
            #return file
    logger.debug(file)
    return file

def Change_Working_Path(path):
    # Check if New path exists
    if os.path.exists(path):
        # Change the current working Directory
        try:
            os.chdir(path)  # Change the working directory
        except OSError:
            logger.error("Can't change the Current Working Directory", exc_info = True)
    else:
        print("Can't change the Current Working Directory because this path doesn't exits")

def convert_raw_to_tiff(outputpath, filename):
    logger.info('Starting convert_raw_to_tiff: ' + filename)
    with rawpy.imread(filename) as raw:
        rgb = raw.postprocess()

    imageio.imsave(outputpath + filename.replace('.CR3', '.tiff'), rgb)
    process = subprocess.run(['exiftool', '-TagsFromFile', outputpath, filename.replace('.CR3', '.tiff')],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
def main():
    path = './RAW'
    filenames = filesearch('.CR3')
    outputpath = '../tiff/'

    check_for_path (outputpath)
    Change_Working_Path(path)

    for filename in filenames:
        convert_raw_to_tiff(outputpath, filename)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    # Setup Logging
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)

    main()