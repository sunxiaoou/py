#! /bin/sh

count()
{
mongo <<-!end
    use shoulie
    db.resumes.find({}).count()
!end
}

ex1()
{
mongo <<-!end
    use shoulie
    db.resumes.find({'工作年限': -1, '学历': -1, 'file' : {'\$regex': /^jl/}},
            {'_id': 0, 'file': 1}).limit(10)
!end
#    db.resumes.find({'工作年限': -1, '学历': -1}, {'_id': 0, 'file': 1}).limit(10)
}

ex2()
{
mongo <<-!end
    use shoulie
    db.getCollection('resumes').
        find({
            '姓名': {'\$regex': /^安/},
            '期望从事职业': {'\$regex': /高级软件/}
    }, {'_id': 0, 'file': 1}).skip(30)
!end
}

ex3()
{
mongo <<-!end
    use tutorial
    db.getCollection('resumes').
        find({
            '工作经历': {'\$regex': /保密控制系统/},
            '项目经历': {'\$regex': /物联网/}
    }, {'_id': 0, 'file': 1})
!end
}


count
# ex3
