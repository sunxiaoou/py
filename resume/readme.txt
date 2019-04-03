
0. Prerequisite for Mac

$ brew install mongodb      # install Mongodb
...
To have launchd start mongodb now and restart at login:
  brew services start mongodb
Or, if you don't want/need a background service you can just run:
  mongod --config /usr/local/etc/mongod.conf

$ pip3 install pymongo


$ cd ~/suzy/shoulie/backup
$ mongoimport --drop --db shoulie --collection resumes --file jl.json
$ mongoimport --db shoulie --collection resumes --file j51.json
$ mongoimport --db shoulie --collection resumes --file jxw.json
$ mongoimport --db shoulie --collection resumes --file zljl.json

$ cd ~/suzy/shoulie/resumes
$ tar xf ../backup/jlok.tgz; mv jlok jl
$ tar xf ../backup/j51ok.tgz; mv j51ok j51
$ tar xf ../backup/jxwok.tgz; mv jxwok jxw
$ tar xf ../backup/zljlok.json; mv zljlok zljl


1. Runtime

$ mongod --config /usr/local/etc/mongod.conf

$ cd ~/suzy/shoulie/src     # from another terminal
$ webSvr.py                 # httpd listen to localhost:7412
