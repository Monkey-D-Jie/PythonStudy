# db_utils.py
import traceback

import pymysql
# from DBUtils.PooledDB import PooledDB 安装不上
# from pymysql import Pool 安装不上

from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
# 需要安装：pip install DBUtils
class DBHandler:
    _pool = None  # 类变量，共享连接池
    _engine = None  # SQLAlchemy 引擎
    _Session = None  # 会话工厂

    def __init__(self):
        '''
        对于新项目，建议使用 SQLAlchemy 方案，因为它：
        有更好的维护支持
        提供更完善的连接池功能
        支持多种数据库后端
        有更完善的错误处理机制
        '''
        if not DBHandler._engine:
            db_config = self._get_db_config()
            # 添加配置验证
            if not db_config or not all(key in db_config for key in ['host', 'user', 'password', 'db']):
                raise ValueError("数据库配置不完整")
            port = db_config.get('port', 3306)  # 默认端口
            connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{port}/{db_config['db']}"
            DBHandler._engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                # True 调试时显示SQL语句
                echo= False
            )
            print("✅ 数据库连接成功")
            DBHandler._Session = sessionmaker(bind=DBHandler._engine)

    def _get_db_config(self):
        return {
            "host": "127.0.0.1",
            "user": "root",
            "password": "jfkjyfb",
            "db": "scrapy_demo_db"
        }

    def get_db_session(self):
        """获取数据库会话"""
        '''
        优势
        连接池统一管理：SQLAlchemy 的 QueuePool 比 DBUtils 更健壮
        自动连接复用：会话会自动从连接池获取/归还连接
        更好的错误处理：SQLAlchemy 提供更详细的数据库错误信息
        未来扩展性：可以轻松切换ORM方式或支持其他数据库
        '''
        try:
            return DBHandler._Session()
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            traceback.print_exc()
            return None

    def get_db_connection(self):
        """ 获取数据库连接 """
        '''
        此处的 ** 双星号操作符
        这是 Python 的 字典解包 语法
        将字典中的键值对解包为函数的命名参数
        等价于：
        return pymysql.connect(
        host=self.db_config["host"],
        user=self.db_config["user"],
        password=self.db_config["password"],
        db=self.db_config["db"]
        )
        
        '''
        """ 获取数据库连接对象 """
        try:
            """ 从连接池获取连接 """
            return DBHandler._pool.connection()
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return None

    def insert_data(self, item, table_name, field_map):
        """
        插入数据到指定的表中（SQLAlchemy核心方式）
        """
        session = self.get_db_session()
        if not session:
            return False

        try:
            # 构建动态SQL
            fields = ", ".join(field_map.values())
            placeholders = ", ".join([f":{k}" for k in field_map.keys()])
            values = {k: item.get(k) for k in field_map.keys()}

            sql = text(f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})")

            session.execute(sql, values)
            session.commit()
            return True

        except Exception as e:
            print(f"插入数据时出错: {e}")
            session.rollback()
            traceback.print_exc()
            return False
        finally:
            session.close()
    def insert_data2(self, item, table_name, field_map):
        """
        插入数据到指定的表中

        :param item: Scrapy 的 item 对象
        :param table_name: 数据库表名
        :param field_map: 字段映射字典，格式为：
                         {"title": "title", "price": "price", ...}
        :return: 是否插入成功
        """
        try:
            connect = self.get_db_connection()
            cursor = connect.cursor()

            # 构建 SQL 插入语句
            fields = ", ".join(field_map.values())
            placeholders = ", ".join(["%s"] * len(field_map))
            values = [item.get(k) for k in field_map.keys()]

            sql = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders});"

            cursor.execute(sql, tuple(values))
            connect.commit()
            return True

        except Exception as e:
            print(f"插入数据时出错: {e}")
            # 打印完整的堆栈跟踪
            traceback.print_exc()
            return False

        finally:
            cursor.close()
            connect.close()


def insert_data_to_table(item, table_name, field_map):
    """
    外部调用接口，封装了 DBHandler 类的调用逻辑

    示例调用方式:
    from db_utils import insert_data_to_table
    success = insert_data_to_table(item, "news")

    :param item: Scrapy item 对象
    :param table_name: 要插入的数据库表名
    :param field_map: 要插入的字段映射信息
    :return: 是否插入成功
    """
    handler = DBHandler()

    # 根据不同的表设置字段映射
    # if table_name == "news":
    #     field_map = {
    #         "title": "title",
    #         "link": "link",
    #         "classify": "classify",
    #         "content": "content"
    #     }
    # elif table_name == "goods":
    #     field_map = {
    #         "title": "title",
    #         "price": "price",
    #         "comment_num": "comment_num",
    #         "link": "link"
    #     }
    # else:
    #     raise ValueError(f"不支持的表名: {table_name}")

    return handler.insert_data(item, table_name, field_map)
