import openpyxl
import openpyxl.utils
import pandas as pd
import pymysql
import logging
import json
import os
from typing import List, Dict, Any, Optional

class DatabaseExporter:
    """数据库导出工具类，用于从MySQL导出数据到Excel"""
    
    def __init__(self, config_path: str = "config.json"):
        """初始化导出工具，加载配置文件"""
        self.connection = None
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()

    # Dict[str, Any]: 加载的配置字典，包含数据库连接、Excel导出和日志配置信息
    # 此处的Dict相当于Java中的Map<String,Object>
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件，如果文件不存在则返回默认配置"""
        try:
            if os.path.exists(self.config_path):
                # with open(...) 是 Python 语言特有的语法糖，简化了文件操作和资源管理。利用了Python的上下文管理器机制
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_config()
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "database": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "test",
                "database": "testdb"
            },
            "excel": {
                "default_file_name": "output.xlsx",
                "sheet_names": ["sheet1"]
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            }
        }
        
    def _setup_logging(self) -> None:
        """设置日志配置"""
        log_config = self.config.get("logging", {})
        level = getattr(logging, log_config.get("level", "INFO").upper())
        log_format = log_config.get("format", "%(asctime)s - %(levelname)s - %(message)s")
        
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.StreamHandler()
            ]
        )
        
    def execute_sql(self, sql: str) -> pd.DataFrame:
        """执行SQL查询并返回DataFrame"""
        try:
            self.connect()
            # 将查询到的结果存储到由PD提供的二位数组存放对象中
            '''
            类似以下的这种形式
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
            '''
            df = pd.read_sql(sql, self.connection)
            logging.info(f"当前执行到的SQL------>>>{sql}")
            self.connection.close()
            logging.info(f"SQL执行成功，返回 {len(df)} 条记录")
            return df
        except Exception as e:
            logging.error(f"SQL执行失败: {str(e)}")
            return pd.DataFrame()

    def connect(self):
        """建立数据库连接"""
        # 从config元组中读取db_config信息，有点类似java中的Map的get()
        db_config = self.config["database"]
        logging.info(f"成功连接到数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
        self.connection = pymysql.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            charset='utf8mb4'
        )

    def execute_query(self, sql):
        """执行查询并返回结果"""
        if not self.connection:
            self.connect()
            # 自动管理游标生命周期，因为cursor也实现了python的上下文管理器
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            # 获取列名，# 如 ['name', 'age']
            # 用zip将列名和行值配对：zip(['name', 'age'], ('Alice', 25)) → ('name','Alice'), ('age',25)
            '''
            Python的列表推导式，强制结构：
            [处理逻辑 for 元素 in 可迭代对象] 结构
            实际执行过程，
            先执行：cursor.fetchall() 获取所有行 → 得到 row 序列
            对每个 row：执行前面的 dict(zip(...)) 转换
            自动收集结果：所有转换后的字典组成新列表返回
            设计哲学：
            让代码更贴近自然语言表达（类似英语的 "return processed_row for each row"）
            笔者留言：确实神奇
            '''
            return [dict(zip([col[0] for col in cursor.description], row))
                    # 返回类似 [('Alice', 25), ('Bob', 30)] 的元组列表，row就是其中一条数据记录
                    for row in cursor.fetchall()]

    def map_columns(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        根据映射关系重命名DataFrame列
        df.rename(columns=mapping) 内部会：
            检查 DataFrame 的所有列名
            将存在于 mapping 字典键中的列名替换为对应的值
            忽略不存在的列名（不会报错）
            返回一个新的 DataFrame（原始数据不变）
        """
        return df.rename(columns=mapping)
        
    def export_to_excel(
        self, 
        dataframes: List[pd.DataFrame], 
        file_name: Optional[str] = None, 
        sheet_names: Optional[List[str]] = None
    ) -> None:
        """将多个DataFrame导出到Excel的不同sheet"""
        try:
            if not file_name:
                file_name = self.config["excel"]["default_file_name"]
                
            if not sheet_names:
                sheet_names = self.config["excel"]["sheet_names"]
                
            # 确保sheet名称数量与DataFrame数量匹配
            if len(sheet_names) < len(dataframes):
                sheet_names = sheet_names + [f"sheet{i+1}" for i in range(len(dataframes) - len(sheet_names))]
                
            with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                # zip() 是 Python 内置函数，用于将多个可迭代对象（如列表）的元素按顺序配对，生成一个迭代器。
                for df, sheet_name in zip(dataframes, sheet_names):
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    #对有内容的df做自适应列宽逻辑处理
                    if len(df) > 0:
                        # 获取工作表对象
                        worksheet = writer.sheets[sheet_name]
                        # 自适应列宽逻辑，enumerate(..., 1) 适配 Excel 的列编号规则（从 1 开始）
                        for col_idx, column in enumerate(df.columns, 1):
                            # 计算列最大宽度（数据与列名比较）
                            max_len = max(
                                # astype(str) 确保数值/日期等非字符串类型也能计算长度
                                df[column].astype(str).str.len().max(),  # 数据最大长度
                                len(str(column))  # 列名长度
                            ) + 2  # 增加边距

                            # 设置列宽（最大限制30）
                            adjusted_width = min(max_len * 1.5, 30)
                            col_letter = openpyxl.utils.get_column_letter(col_idx)
                            worksheet.column_dimensions[col_letter].width = adjusted_width

                logging.info(f"已导出 {len(df)} 条记录到 {file_name} 的 {sheet_name} 工作表")
        except Exception as e:
            logging.error(f"导出Excel失败: {str(e)}")
            
    def export_with_config(
        self, 
        sqls: List[str], 
        mappings: List[Dict[str, str]],
        file_name: Optional[str] = None,
        sheet_names: Optional[List[str]] = None
    ) -> None:
        """根据配置导出数据"""
        if len(sqls) != len(mappings):
            logging.error("SQL语句数量与映射关系数量不匹配")
            return
            
        dataframes = []
        for sql, mapping in zip(sqls, mappings):
            df = self.execute_sql(sql)
            #空数据也直接写入
            # if not df.empty:
            #     mapped_df = self.map_columns(df, mapping)
            #     dataframes.append(mapped_df)
            mapped_df = self.map_columns(df, mapping)
            dataframes.append(mapped_df)
                
        if dataframes:
            self.export_to_excel(dataframes, file_name, sheet_names)
        else:
            logging.warning("没有数据可导出")    