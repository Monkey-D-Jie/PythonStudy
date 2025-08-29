from setuptools import setup, find_packages
'''
🔍 setup.py 的核心作用
1. 项目打包与安装
允许通过 pip install -e . 以"可编辑模式"安装项目
生成可分发的包（如 .whl 或 .tar.gz）
2. 解决导入路径问题
通过 find_packages() 自动发现项目中的所有 Python 包
使项目内的模块可以互相导入（解决你之前遇到的导入错误）
3. 定义项目元数据
项目名称、版本、依赖等基础信息（示例中只定义了最简配置）
'''
setup(
    name="baidunews_demo",
    packages=find_packages(),
)
