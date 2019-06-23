import hashlib
import os
import sys
import getopt
import time


class Hasher:
    def __init__(self, hash_method='md5', read_buff_size=pow(2, 18), quiet=False, first_n=-1):
        if hash_method == 'md5':
            self.hash_tool = hashlib.md5()
        elif hash_method == 'sha1':
            self.hash_tool = hashlib.sha1()
        elif hash_method == 'sha256':
            self.hash_tool = hashlib.sha256()
        elif hash_method == 'sha512':
            self.hash_tool = hashlib.sha3_512()
        elif hash_method == 'blake2b':
            self.hash_tool = hashlib.blake2b()
        elif hash_method == 'blake2s':
            self.hash_tool = hashlib.blake2s()
        else:
            print('unknown hash method')
            sys.exit()
        self.read_buff_size = read_buff_size
        self.quiet = quiet
        self.total_size = 0
        self.num_files = 0
        self.first_n = int(first_n)

    def hash(self, path):
        hash_value = ''
        if os.path.isdir(path):
            hash_value = self.hash_dic(path)
        elif os.path.isfile(path):
            hash_value = self.hash_file(path)
        else:
            print('Invalid path')
        return hash_value

    def hash_dic(self, root):
        if 'System Volume Information' in root:
            return
        if not os.access(root, os.R_OK):
            print(root, 'permission denied')
            return
        items = os.listdir(root)
        items.sort()
        for item in items:
            path = os.path.join(root, item)
            if os.path.isdir(path):
                self.hash_dic(path)
            else:
                self.hash_file(path)
        return self.hash_tool.hexdigest()

    def hash_file(self, path):
        if self.num_files == self.first_n:
            return
        if not os.access(path, os.R_OK):
            print(path, 'permission denied')
            return
        if not self.quiet:
            print(path)
        file = open(path, 'rb')
        while 1:
            buff_data = file.read(self.read_buff_size)
            if not buff_data:
                break
            self.hash_tool.update(buff_data)
        file.close()
        # record file size and number
        self.total_size = self.total_size + os.path.getsize(path)
        self.num_files = self.num_files + 1

        return self.hash_tool.hexdigest()

    def num_bytes_to_real_size(self, num_bytes):
        if num_bytes < 1024:
            return str(num_bytes) + ' B'
        elif num_bytes in range(pow(1024, 1), pow(1024, 2)):
            return str(round((num_bytes / pow(1024, 1)), 3)) + ' KB'
        elif num_bytes in range(pow(1024, 2), pow(1024, 3)):
            return str(round((num_bytes / pow(1024, 2)), 3)) + ' MB'
        elif num_bytes in range(pow(1024, 3), pow(1024, 4)):
            return str(round((num_bytes / pow(1024, 3)), 3)) + ' GB'


def print_help_and_exit():
    print('Usage:', 'hasher [path][-m [hash method]][-h][-q]')
    print('  ', '-h', '\t', 'Show help')
    print('  ', '-q', '\t', 'Quiet mode, no output.')
    print('  ', '-m [hash method]', '\t',
          'Must be in [md5, sha1, sha256, sha512, blake2b, blake2s]')
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No path given.')
        print_help_and_exit()
    root_path = sys.argv[1]
    if root_path == '-h' and len(sys.argv) == 2:
        print_help_and_exit()
    if not os.path.exists(root_path):
        print(root_path, 'does not exist.')
        sys.exit()
    # parameters
    quiet = False
    method = 'md5'
    allowed_method_list = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b', 'blake2s']
    first_n = -1
    try:
        opts, args = getopt.getopt(sys.argv[2:], '-q-h-m:-n:')
        for opt, value in opts:
            if opt == '-q':
                quiet = True
            if opt == '-h':
                print_help_and_exit()
            if opt == '-m':
                method = value
                if method not in allowed_method_list:
                    print('Unknown method:', value)
                    sys.exit()
            if opt == '-n':
                first_n = value
    except getopt.GetoptError as e:
        print('getopt error: ', e)
        print_help_and_exit()
    # start
    print('hasher 1.0.0    by R.E Function')
    start_time = time.time()
    hasher = Hasher(quiet=quiet, read_buff_size=pow(2, 18), hash_method=method, first_n=first_n)
    hash_value = hasher.hash(root_path)
    print('-------------------------------------------------------')
    print('hash value:', hash_value)
    print('files:', hasher.num_files)
    print('size:', hasher.num_bytes_to_real_size(hasher.total_size))
    print('time:', str(round((time.time() - start_time), 3)) + 's')
    print('-------------------------------------------------------')
