#! /usr/bin/python3

import zipfile, os

# os.chdir('../materials')    # move to the folder with example.zip
exampleZip = zipfile.ZipFile('../materials/example.zip')
print(exampleZip.namelist())
spamInfo = exampleZip.getinfo('spam.txt')
print(spamInfo.file_size)
print(spamInfo.compress_size)
print('Compressed file is %sx smaller!' % (round(spamInfo.file_size / spamInfo .compress_size, 2)))

# exampleZip.extractall()
exampleZip.extractall('foo')
exampleZip.extract('spam.txt', 'foo/bar')
exampleZip.close()

newZip = zipfile.ZipFile('new.zip', 'w')
newZip.write('foo/spam.txt', compress_type=zipfile.ZIP_DEFLATED)
newZip.close()
