import lib.core as core
import glob as glob


def readImage(file, **options):
    if not isinstance(file, str):
        raise Exception('[Coconut] Invalid file path.')
    core.processImages([file], options)


def readImages(files, **options):
    if not isinstance(files, list):
        raise Exception('[Coconut] Invalid files.')
    core.processImages(files, options)


def readFolder(folder, **options):
    if not isinstance(folder, str):
        raise Exception('[Coconut] Invalid folder.')
    files = glob.glob(f'{folder}/*')
    core.processImages(files, options)
