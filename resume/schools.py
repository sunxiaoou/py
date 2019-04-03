#! /usr/local/bin/python3


class Schools:
    @staticmethod
    def is_985(school):
        school985 = [
            '清华大学', '北京大学', '中国科学技术大学', '复旦大学', '中国人民大学', '上海交通大学',
            '南京大学', '同济大学', '浙江大学', '南开大学', '北京航空航天大学', '北京师范大学',
            '武汉大学', '西安交通大学', '天津大学', '华中科技大学', '北京理工大学', '东南大学',
            '中山大学', '华东师范大学', '哈尔滨工业大学', '厦门大学', '西北工业大学', '中南大学',
            '大连理工大学', '四川大学', '电子科技大学', '华南理工大学', '吉林大学', '湖南大学',
            '重庆大学', '山东大学', '中国农业大学', '中国海洋大学', '中央民族大学', '东北大学',
            '兰州大学', '西北农林科技大学', '国防科技大学']
        return school in school985

    @staticmethod
    def is_211(school):
        school211 = [
            '清华大学', '北京大学', '中国科学技术大学', '复旦大学', '中国人民大学', '上海交通大学',
            '南京大学', '同济大学', '浙江大学', '上海财经大学', '南开大学', '北京航空航天大学',
            '中央财经大学', '北京师范大学', '武汉大学', '对外经济贸易大学', '西安交通大学',
            '天津大学', '华中科技大学', '北京理工大学', '东南大学', '北京外国语大学', '中山大学',
            '中国政法大学', '华东师范大学', '哈尔滨工业大学', '北京邮电大学', '厦门大学',
            '上海外国语大学', '西北工业大学', '西南财经大学', '中南大学', '大连理工大学',
            '中国传媒大学', '四川大学', '电子科技大学', '中南财经政法大学', '华南理工大学',
            '吉林大学', '南京航空航天大学', '湖南大学', '重庆大学', '北京科技大学', '北京交通大学',
            '山东大学', '华东理工大学', '西安电子科技大学', '天津医科大学', '南京理工大学',
            '中国农业大学', '华中师范大学', '中国海洋大学', '哈尔滨工程大学', '中央民族大学',
            '华北电力大学', '北京中医药大学', '暨南大学', '苏州大学', '武汉理工大学', '东北大学',
            '兰州大学', '中国药科大学', '东华大学', '河海大学', '北京林业大学', '河北工业大学',
            '北京工业大学', '江南大学', '北京化工大学', '西南交通大学', '上海大学', '南京师范大学',
            '中国地质大学', '中国地质大学', '西北大学', '东北师范大学', '长安大学', '中国矿业大学',
            '华中农业大学', '合肥工业大学', '广西大学', '中国石油大学', '陕西师范大学',
            '南京农业大学', '湖南师范大学', '福州大学', '大连海事大学', '西北农林科技大学',
            '西南大学', '中国矿业大学', '云南大学', '太原理工大学', '华南师范大学', '北京体育大学',
            '中国石油大学', '安徽大学', '东北林业大学', '东北农业大学', '辽宁大学', '南昌大学',
            '延边大学', '内蒙古大学', '四川农业大学', '海南大学', '贵州大学', '郑州大学',
            '新疆大学', '宁夏大学', '石河子大学', '青海大学', '国防科技大学', '中央音乐学院']
        return school in school211

    @staticmethod
    def get_rank(school):
        if Schools.is_985(school):
            return 3
        elif Schools.is_211(school):
            return 2
        else:
            return 1
