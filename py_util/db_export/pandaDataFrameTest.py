#实践参考链接：https://geek-blogs.com/blog/pddataframe-in-python/
#pandas dataframe的一些实践
import pandas as pd
print("======== 一、创建数据 ========")
print("========1.从字典创建========")
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
print(df)
print("========2.从列表的列表创建========")
data = [
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]
columns = ['Name', 'Age', 'City']
df = pd.DataFrame(data, columns=columns)
print(df)
print("======== 二、访问数据 ========")
print("========1.通过列名访问========")
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

df = pd.DataFrame(data)

# 访问 'Name' 列
names = df['Name']
print(names)
print("========2.通过行索引和列索引访问========")
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

df = pd.DataFrame(data)

# 访问第一行第二列的数据
value = df.iloc[0, 1]
print(value)
print("========3.数据分组和聚合========")
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Department': ['HR', 'IT', 'HR', 'IT'],
    'Salary': [5000, 6000, 5500, 6500]
}

df = pd.DataFrame(data)
print(df)
# 按部门分组并计算平均工资
print("按Department分组并计算平均工资")
grouped = df.groupby('Department')['Salary'].mean()
print(grouped)