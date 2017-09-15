import os
import argparse
import logging
import sys

logger = logging.getLogger('my_cleaner')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(ch)


def overwrite(f):
    """Overwrite a file with zeroes.

    Arguments:
        f -- name of the file
    """
    stat = os.stat(f)
    with open(f, 'r+') as fs:
        fs.write('\0' * stat.st_size)
        fs.flush()


def clean_file(path, count):
    """Overwrites a file count times and deletes it.

    Arguments:
        path -- path of the file to be overwritten
        count -- the amount of overwrites
    """
    if os.path.exists(path):
        for i in range(count):
            overwrite(path)
        os.remove(path)
        logger.info('Successfully removed file {0}'.format(path))
    else:
        logger.error('No such path: {0}'.format(path))


def clean_directory(path, count):
    """Recursively overwrites file in dir and removes them and its directories.

    Arguments:
        path -- path of the file to be overwritten
        count -- the amount of overwrites
    """

    if os.path.exists(path):
        for (dirpath, dirnames, filenames) in os.walk(path, topdown=False):
            for file in filenames:
                clean_file(os.path.join(dirpath, file), count)
            os.rmdir(dirpath)
            logger.info('Successfully removed directroy {0}'.format(dirpath))
    else:
        logger.error('No such path: {0}'.format(path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Attempt to remove directories as well as other types of files.",
                        action="store_true")
    parser.add_argument("-c", "--count", type=int, default=1, help="The amount of rewrites")
    parser.add_argument("path", type=str, help="The path to be removed")
    args = parser.parse_args()

    if args.directory:
        clean_directory(args.path, args.count)
    else:
        clean_file(args.path, args.count)
