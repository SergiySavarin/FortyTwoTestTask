import os

from PIL import Image


def size(path):
    """ Function calculate photo size.
        args:
            path: path to photo.
        returns:
            True: if photo is in 200x200px size.
            False: if photo is more than 200x200px size.
    """
    try:
        original = Image.open(path)
        width = original.size[0]
        heigth = original.size[1]
        if width > 200 or heigth > 200:
            return False
        return True
    except IOError as err:
        return err


def resize(path, testpath=None):
    """ Function for resizing photo
        if it size more than 200x200px.
        args:
            path: path to photo.
            testpath: path for test this method work or not
        returns:
            True: if photo resized and saved successfuly.
            False: if something going wrong.
    """
    try:
        original = Image.open(path)
        width = original.size[0]
        heigth = original.size[1]
        # calculate ratio
        ratio = min(200.0 / width, 200.0 / heigth)
        # colculate new size
        size = (width * ratio, heigth * ratio)
        # scale image
        original.thumbnail(size, Image.ANTIALIAS)
        if testpath:
            original.save(testpath)
        else:
            original.save(path)
        return True
    except IOError as err:
        return err


def empty_dat():
    """ Function check if .dat file is empty after run bash
        script ./print_mod.sh
    """
    # run bash script
    os.system('./print_mod.sh')
    # find saved file in and check for result
    file_names = os.popen('ls').read().split()
    output_file = [name for name in file_names if '.dat' in name]
    with open(output_file[0]) as out:
        out = out.read()
        if out == '\n' or out == '':
            return True
        return False
