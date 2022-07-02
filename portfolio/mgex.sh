#! /bin/sh

count() {
mongosh <<-!end
    use $1
    db.$2.countDocuments()
!end
}

ex1() {
mongo <<-!end
    use $db
    db.$collection.find({type: 'a'}, {_id: 0, name: 1, price: 1}).limit(10)
!end
}

ex2() {
mongo <<-!end
    use shoulie
    db.getCollection('resumes').
        find({
            '姓名': {'\$regex': /^安/},
            '期望从事职业': {'\$regex': /高级软件/}
    }, {'_id': 0, 'file': 1}).skip(30)
!end
}

ex3() {
mongo <<-!end
    use tutorial
    db.getCollection('resumes').
        find({
            '工作经历': {'\$regex': /保密控制系统/},
            '项目经历': {'\$regex': /物联网/}
    }, {'_id': 0, 'file': 1})
!end
}

count_type() {
mongo <<-!end
  use $db
  db.getCollection('funds_info').aggregate([{\$group: {_id: {'type': '\$type', 'typ2': '\$typ2'}, num: {\$sum : 1}}}])
!end
}

find_date() {
mongo <<-!end
  use $db
  db.getCollection('sh000985').find({
     "\$expr":{
      "\$and":[
        {"\$gte":[{"\$toDate":"\$_id"},ISODate("2021-11-24T00:00:00.000Z")]},
        {"\$lte":[{"\$toDate":"\$_id"},ISODate("2021-11-30T00:00:00.000Z")]}
      ]
    }
  }, {'_id': 1, 'close': 1})
!end
}

drop_collections() {
mongo <<-!end
  use $db
  regex = /^f/;
  db.getCollectionNames().filter(function(name){
    return name.match(regex)
  }).forEach(function(name){
    db.getCollection(name).drop()
  })
!end
}

show_last_documents() {
mongosh <<-!end
  use $1
  db.getCollection('$2').aggregate([
    {\$sort: {'_id': -1}},
    {\$addFields: {'Date': {\$toDate: '\$_id'}}},
    {\$limit: 2}
  ]);
!end
}


## main ##

db='portfolio'
# count 'portfolio' 'funds_info'
# count_type
# find_date
# drop_collections
show_last_documents 'portfolio' 'sh000985'  # 'valuation'