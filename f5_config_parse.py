# -*- encoding: utf-8 -*-
"""
@File    : config-to-execl-f5.py
@Time    : 2024/4/12 21:25
@Author  : Gao
"""
import re
import openpyxl
from os import getcwd
from openpyxl.styles import Alignment


def read_config_file(filepath):
    """读取配置文件内容"""
    with open(filepath, 'r') as file:
        return file.read()

def extract_data(pattern, text):
    """根据提供的正则表达式从文本中提取数据"""
    compiled_pattern = re.compile(pattern, re.MULTILINE)
    return re.findall(compiled_pattern, text)

def initialize_worksheet(wb):
    """初始化工作表，并设置标题和列头"""
    ws = wb.active
    ws.title = 'F5 LTM Configuration'
    headers = ['Pool Name', 'Pool Members', 'Virtual Server Name', 'Virtual Server IP', 'Virtual Server Port','Description']
    for column, header in enumerate(headers, start=1):
        ws.cell(row=1, column=column, value=header)
    return ws

def init_sheet2(wb):
    """初始化工作表，并设置标题和列头"""
    ws = wb.active
    ws = wb.create_sheet()
    ws.title = 'F5 LTM Configuration SNAT'
    headers = ['SNAT Pool Name', 'SNAT Address']
    for column, header in enumerate(headers, start=1):
        ws.cell(row=1, column=column, value=header)
    return ws

def remove_common_prefix(name):
    """移除名称中的公共前缀 '/Common/'"""
    return name.replace('/Common/', '')

def main(filename):
    """主函数，执行配置文件的读取、数据提取和Excel文件的生成"""
    pwd_dir=getcwd().replace('\\','/')
    file_path =  pwd_dir + '/' + str(filename)
    config = read_config_file(file_path)
    workbook = openpyxl.Workbook()
    sheet1 = initialize_worksheet(workbook)
    sheet2 = init_sheet2(workbook)
    
    # 定义用于数据提取的正则表达式
    pool_pattern = r'ltm pool (.+) {\n([\s\S]*?)\n}'
    vs_pattern = r'virtual (.+) {\n([\s\S]*?)\n}'
    snatpool_pattern = r'ltm snatpool (.+) {\n([\s\S]*?)\n}'
    descr_pattern = re.compile(r'description (\S+)')
    member_pattern = re.compile(r'(?:/Common/)([A-Fa-f0-9(:|.)]+[:.]\d+)', re.MULTILINE)
    destination_pattern = re.compile(r'destination (?:/Common/)([A-Fa-f0-9(:|.)]+[:.](\d+))', re.MULTILINE)
    pool_ref_pattern = re.compile(r'pool (.+)', re.MULTILINE)


    # 处理pool配置
    pools = extract_data(pool_pattern, config)
    row = 2
    for pool_name, members in pools:
        pool_name = remove_common_prefix(pool_name.strip())
        descr_str = descr_pattern.search(members).group(1)
        members = member_pattern.findall(members)
        member_str = "\n".join(m for m in members)
        sheet1.cell(row=row, column=1, value=pool_name)
        sheet1.cell(row=row, column=2, value=member_str)
        sheet1.cell(row=row, column=6, value=descr_str).alignment = Alignment(wrap_text=True)
        row += 1

    # 处理vs配置
    virtual_servers = extract_data(vs_pattern, config)
    for vs_name, details in virtual_servers:
        vs_name = remove_common_prefix(vs_name.strip())
        dest_match = destination_pattern.search(details)
        pool_match = pool_ref_pattern.search(details)
        if dest_match and pool_match:
            vs_ip = remove_common_prefix(dest_match.group(1))
            vs_port = dest_match.group(2)
            pool_name = remove_common_prefix(pool_match.group(1).strip())
            for i in range(2, sheet1.max_row + 1):
                if sheet1.cell(row=i, column=1).value == pool_name:
                    sheet1.cell(row=i, column=3, value=vs_name)
                    sheet1.cell(row=i, column=4, value=vs_ip)
                    sheet1.cell(row=i, column=5, value=vs_port)
                    break
                
    # 处理snat pool配置            
    snatpools = extract_data(snatpool_pattern, config)
    row = 2
    for snat_name, members in snatpools:
        snat_name = remove_common_prefix(snat_name.strip())
        members = member_pattern.findall(members)
        member_str = "\n".join(m for m in members)
        sheet2.cell(row=row, column=1, value=snat_name)
        sheet2.cell(row=row, column=2, value=member_str).alignment = Alignment(wrap_text=True)
        row += 1

    # 调整列宽
    for col_letter, width in zip(['A', 'B', 'C', 'D', 'E','F'], [20,40,30,20,25,30]):
        sheet1.column_dimensions[col_letter].width = width

    # 保存工作簿
    workbook.save('f5_ltm_config.xlsx')
    print("数据分析完成结果保存在f5_ltm_config.xlsx")

if __name__ == '__main__':
    main('sou_bigip.conf.txt') #自行修改文件名