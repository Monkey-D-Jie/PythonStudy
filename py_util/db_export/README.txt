程序生成：来自豆包AI
MySQL数据导出Excel工具使用说明

一、环境准备
1. 安装Python 3.7及以上版本
2. 安装依赖库：
   pip install pandas pymysql openpyxl

二、配置文件
1. 配置文件为JSON格式，默认名为config.json
2. 配置项说明：
   - database: 数据库连接配置
     - host: 数据库主机
     - port: 数据库端口
     - user: 数据库用户名
     - password: 数据库密码
     - database: 数据库名
   - excel: Excel导出配置
     - default_file_name: 默认导出文件名
     - sheet_names: 默认工作表名列表
   - logging: 日志配置
     - level: 日志级别
     - format: 日志格式

三、使用方法
1. 直接运行：python main.py
2. 程序会提示输入数据库配置信息（直接回车使用默认值）
3. 程序会按配置导出多个机构的数据到不同Excel文件

四、转换为exe
1. 安装PyInstaller: pip install pyinstaller
2. 执行打包命令: pyinstaller --onefile main.py
3. 生成的exe文件位于dist目录下
4. 运行exe文件即可使用工具

五、注意事项
1. 确保数据库连接信息正确
2. SQL语句需要根据实际表结构调整
3. 列映射关系需要与SQL查询结果列名匹配
4. 日志会输出到控制台，方便排查问题    