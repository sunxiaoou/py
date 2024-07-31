0. prerequisite

1) Python 脚本基于 python 3.8+
2) 在控制机上关闭签名校验, 以控制机v8.x为例, 其它版本的操作可能不同，请参阅相关文档
$ cd /usr/info2soft/cntlcenter/wwwroot/default/application/config   # 修改 main.php 文件
$ diff -u main.php.orig main.php
   // 接口请求参数签名，postman手工测试时，可关闭该选项跳过复杂的签名计算
  -$config['enable_sign_verify'] = true; // 签名校验
  +$config['enable_sign_verify'] = false; // 关闭签名校验
3) 拷贝控制机根证书 /usr/info2soft/cntlcenter/etc/certs/ca.crt 到当前脚本运行目录
4) 如使用 AccessKey 代替传统的用户名和口令, 需在控制台的 "账户信息/密钥管理" 中事先生成
5) 生成数据库节点时如用到 "凭据(credential)" 对象，需在控制台的 "系统管理/凭据管理" 中事先生成


1. 目录结构
├── ca.crt                  # I2UP 根证书
├── access.key              # 存放 AccessKey 的文件 (可选)
├── excel
│   ├── samples.xlsx        # 生成 MySQL/Kafka 节点和 MySQL-MySQL/Kafka 规则时的工作表示例，只包含创建上述对象所需的常用参数
│   └── template.xlsx       # 生成 MySQL/Kafka 节点和 MySQL-MySQL/Kafka 规则时的默认参数表，和工作表合并后产生实际的参数表
├── excel_tool.py           # 根据Excel工作表通过 I2UP API 批量生成节点和规则的实用工具
├── i2up.py                 # I2UP 实用工具
├── output                  # excel_tool.py 根据Excel工作表批量生成节点和规则的json文件的输出目录
└── readme.txt


2. i2up.py
该工具主要功能如下：

+---------------+---------------------+--------------------+---------------+--------------+
|               | 打印对象列表          | 显示给定对象          | 激活/生成对象   | 删除对象      ｜
+---------------+---------------------+--------------------+---------------+--------------+
| 机器节点(未激活) | list-inactive-nodes | show-inactive-node | activate-node |              ｜
+---------------+---------------------+--------------------+---------------+--------------+
| 机器节点        | list-nodes          | show-node          |               |             ｜
+---------------+---------------------+--------------------+----------------+-------------+
| 数据库节点      | list-dbs            | show-db            | create-db     | delete-db    ｜
+---------------+---------------------+--------------------+---------------+--------------+
| 同步规则        | list-rules          | show-rule          | create-rule   | delete-rule ｜
+---------------+---------------------+--------------------+---------------+--------------+

示例
$ i2up.py -h                                                # 显示帮助信息
$ i2up.py --ip centos1 --pwd Info1234 --version             # 显示控制机版本, centos1 是控制机机器名, 通过用户/口令认证
$ i2up.py --ip centos1 --ak access.key --version            # 显示控制机版本, centos1 是控制机机器名，通过access.key认证

$ i2up.py --ip centos1 --pwd Info1234 --list-inactive-nodes                 # 显示未激活机器节点列表
$ i2up.py --ip centos1 --pwd Info1234 --activate-node --node hadoop3 --pwd2 helper_pwd --src
                                                                            # 激活机器节点 hadoop3 作为源端节点

$ i2up.py --ip centos1 --pwd Info1234 --show-db --db msq_u_auto             # 显示数据库节点 msq_u_auto
$ i2up.py --ip centos1 --pwd Info1234 --create-rule --json json/msq_u_c1_auto.json
                                                                            # 根据json文件生成同步规则 msq_u_c1_auto
$ i2up.py --ip centos1 --pwd Info1234 --delete-rule --rule msq_u_c1_auto    # 删除同步规则 msq_u_c1_auto


3. excel_tool.py
该工具主要功能如下：

1) 显示帮助信息
$ excel_tool.py -h

2) 根据Excel工作表中提供的数据库节点/同步规则信息，结合模版文件中同名表单，批量生成用于创建相关对象的json文件，示例：
$ excel_tool.py --excel2json --excel excel/samples.xlsx --template excel/template.xlsx

3) 根据Excel工作表中提供的数据库节点/同步规则信息，通过 I2UP API 批量删除控制机中的相关对象，示例：
$ excel_tool.py --deleteObjects --ip centos1 --pwd Info1234 --excel excel/samples.xlsx

4) 根据Excel工作表中提供的数据库节点/同步规则信息，结合模版文件中同名表单，通过 I2UP API 在控制机中批量创建相关对象，示例
$ excel_tool.py --createObjects --ip centos1 --pwd Info1234 --excel excel/samples.xlsx --template excel/template.xlsx

