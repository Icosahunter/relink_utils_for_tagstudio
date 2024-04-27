import relink_utils as ru
import glob
from pathlib import Path

p1 = Path('test/fruits/apple/cosmic.txt')
p2 = Path('test/fruits/apple/cosmic.json')
p3 = Path('test/fruits/apple/cosmic')
p4 = Path('test/fruits/apple/cosmic.jpg')
p5 = Path('test/fruits/banana/cavandish.txt')
p6 = Path('test/fruits2/apple/cosmic.txt')
p7 = Path('test/fruits2/apple/cosmic.conf')
p8 = Path('test/fruits2/apple/cosmic.JPEG')
p9 = Path('test/fruits2/apple/cosmic.png')
p10 = Path('test/fruits2/apple/cosine.txt')

print('--- Comparison Functions ---')

def path_dist_test(file1, file2):
    print(f'Path distance between \'{file1}\' and \'{file2}\' = {ru.path_distance(file1, file2)}')

def str_comp_test(file1, file2):
    print(f'String similarity between \'{file1.stem}\' and \'{file2.stem}\' = {ru.str_compare(file1.stem, file2.stem)}')

def ext_comp_test(file1, file2):
    print(f'File type similarity between \'{file1.name}\' and \'{file2.name}\' = {ru.ext_compare(file1, file2)}')

path_dist_test(p1, p5)
path_dist_test(p1, p2)

str_comp_test(p1, p10)
str_comp_test(p1, p5)

ext_comp_test(p1, p3)
ext_comp_test(p1, p2)
ext_comp_test(p1, p4)
ext_comp_test(p1, p7)
ext_comp_test(p4, p8)
ext_comp_test(p4, p9)

print('--- Comparison Index ---')

def index_test(file1, file2):
    print(f'File diff index \'{file1.name}\' and \'{file2.name}\' = {ru.file_diff_index(file1, file2)}')

index_test(p1, p2)
index_test(p1, p5)
index_test(p1, p10)
index_test(p4, p8)
index_test(p4, p9)

print('--- Relink Finds ---')

def relink_test(file, directory, no_hash=False):
    files = [x for x in Path(directory).glob('**/*') if x.is_file() and x.absolute() != file.absolute()]
    hs = None if no_hash else ru.hash_file(file) 
    rl = ru.relink(file, files, hs)
    ht = ' (no hash)' if no_hash else ''
    print(f'Relink{ht} find for \'{file}\' in \'{directory}\' = {rl}')

relink_test(p1, 'test/')
relink_test(p1, 'test/', True)
relink_test(p1, 'test/fruits2/')
relink_test(p2, 'test/')
relink_test(p5, 'test/')
relink_test(p4, 'test/')
relink_test(p4, 'test/', True)