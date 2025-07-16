import json
import os
import argparse
from random import choice

from db_exporter import DatabaseExporter

def get_user_input(config: dict) -> dict:
    """获取用户输入的配置信息"""
    db_config = config.get("database", {})
    host = None
    port = None
    user = None
    password = None
    database = None
    choice = input(f"请选择模式。1-默认模式，2-自定义配置模式: ")
    if choice == 2:
        host = input(f"请输入数据库主机 [{db_config.get('host', 'localhost')}]: ")
        port = input(f"请输入数据库端口 [{db_config.get('port', 3306)}]: ")
        user = input(f"请输入数据库用户名 [{db_config.get('user', 'root')}]: ")
        password = input(f"请输入数据库密码 [{db_config.get('password', '')}]: ")
        database = input(f"请输入数据库名 [{db_config.get('database', '')}]: ")
    # 使用用户输入或默认值
    db_config["host"] = host if host else db_config.get("host", "localhost")
    db_config["port"] = int(port) if port else db_config.get("port", 3306)
    db_config["user"] = user if user else db_config.get("user", "root")
    db_config["password"] = password if password else db_config.get("password", "")
    db_config["database"] = database if database else db_config.get("database", "")
    
    config["database"] = db_config
    return config

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MySQL数据导出工具")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--use-default", action="store_true", help="使用默认配置，不询问用户输入")
    args = parser.parse_args()
    
    # 创建导出器实例
    exporter = DatabaseExporter(args.config)
    
    # 如果用户没有指定使用默认配置，则获取用户输入
    if not args.use_default:
        print("\n请输入数据库配置信息（直接回车使用默认值）：")
        exporter.config = get_user_input(exporter.config)
    # 查询机构的自定义SQL
    '''
    
    '''
    institution_query = """
    SELECT
        *
        WHERE
            p.STATUS = 'A' 
            AND p.org_code = '{org_code}';
	"""
    try:
        # 执行SQL，查库获取到SQL
        institutions = exporter.execute_query(institution_query)
        print(f"成功获取到 {len(institutions)} 个机构")
    except Exception as e:
        print(f"获取机构列表失败: {e}")
        return
    # 示例：多个机构数据导出
    # institutions = ["school1", "school2", "school3"]


    for institution in institutions:
        org_code = institution["org_code"]
        org_name = institution["org_name"]
        print(f"\n正在导出 {org_name}({org_code}) 的数据...")

        # 为不同机构定制SQL
        # student_sql = f"SELECT id, name, age, gender FROM {institution}_students"
        # teacher_sql = f"SELECT id, name, subject FROM {institution}_teachers"
        # semester_sql =f"SELECT id, name, subject FROM {institution}_semesters"

        student_sql = f"""
        SELECT
        *
        WHERE
            p.STATUS = 'A' 
            AND p.org_code = '{org_code}';
        """
        teacher_sql = f"""
                SELECT
                *
                WHERE
                    p.STATUS = 'A' 
                    AND p.org_code = '{org_code}';
                """
        semester_sql = f"""
                SELECT
                *
                WHERE
                    p.STATUS = 'A' 
                    AND p.org_code = '{org_code}';
                """

        # 定义列映射关系
        student_mapping = {
            "学生姓名": "学生姓名",
            "性别": "性别",
            "学号": "学号",
            "学段": "学段"
        }
        teacher_mapping = {
            "用户名称": "用户名称",
            "用户编号": "用户编号",
            "身份证号": "身份证号",
            "部门": "部门",
            "创建时间": "创建时间"
        }
        semester_mapping = {
            "学年": "学年",
            "学期": "学期",
            "开始时间": "开始时间",
            "结束时间": "结束时间"
        }
        
        # 导出数据
        exporter.export_with_config(
            sqls=[student_sql, teacher_sql,semester_sql],
            mappings=[student_mapping, teacher_mapping,semester_mapping],
            file_name=f"G:\\test\\{org_name}数据统计汇总.xlsx",
            sheet_names=["学生信息", "教师信息","校历信息"]
        )
    
    print("\n数据导出完成！")

if __name__ == "__main__":
    main()    