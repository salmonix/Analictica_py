import os.path

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
