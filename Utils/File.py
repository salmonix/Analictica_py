import os.path
import yaml


# also make here a file opener with the necessary error messages

def check_path(fpath, *args):
    """Checks for the existence of a path. The arguments are joined into one path string."""

    if args:
        fpath = os.path.join(fpath, *args)

    if os.path.exists(fpath):
        return fpath
    else:
        # warnings.warn("Not existing: " + fpath)
        raise IOError(fpath + " does not exist for corpus '" + self.corpus + "' of type '" + self.sourcetype + "'")
        return None


def get_path_iterator(path):
    """Takes a path and if exists returns an iterator with the files. If path is a file, then 
    the iterator iterates only one element."""

    if os.path.isdir(path):
        try:
            for f in os.listdir(path):
                checked = check_path(path, f)

                if checked:
                    yield checked
                else:
                    print('LOG: %s %s does not exists' % (path, f))
                    continue

        except:
            print(' We have some error... ?')
    else:
        yield check_path(path)


# also need csv writing possibly replace the csv writer in Representations.Tables
def write_file(text, filename, writemode='w', type=None):
    """Writes out the passed text to the filename. If 'text' is an array, it is treated as an array of strings.
    Optional parameter: writemode ='a'(append), default: 'w' """

    if not type:
       type = os.path.splitext(filename)[1]

    with open(filename, writemode) as file:

        if type == 'yaml' or type == 'yml':
            file.write(yaml.dump(text))

        elif type == "txt":

            if hasattr(text, '__iter__'):
                file.write("\n".join(text))
            else:
                file.write(text)

    file.close()


# TODO: we may add some other possibilities to read csv format after suffix recognition
def file_slurp(filename, type=None):
   """Reads in the string of the given filename.
   It guesses the type from the extension, unless the optional parameter 'txt' overwirtes it."""

   if not type:
       type = os.path.splitext(filename)[1]

   data = None
   with open(filename, 'r') as file:

       if type == 'txt':
           data = file.read()
       elif type == 'yaml' or type == 'yml':
           data = yaml.load(file)

   file.close()
   return data
