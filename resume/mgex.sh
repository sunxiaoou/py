#! /bin/sh

ex1()
{
mongo <<-!end
    use shoulie
    db.getCollection('resumes').find({'姓名': '安敬辉'}, {'_id': 0, 'file': 1})
!end
}

ex2()
{
mongo <<-!end
    use shoulie
    db.resumes.find({'工作年限': -1, '学历': -1, 'file' : {'\$regex': /^jl/}},
            {'_id': 0, 'file': 1}).limit(10)
!end
#    db.resumes.find({'工作年限': -1, '学历': -1}, {'_id': 0, 'file': 1}).limit(10)
}

ex2
