import json
import os
import re
import miner_text_generator


def get_reference(pdf_path, regex="\n\nReferences\n\n", page_regex="\n\n[0-9]*\n\n"):
    # 获取摘要文本
    # Args:
    #   pdf_path: 要解析的pdf的路径
    #   regex: 参考文献标志的正则表达式
    #   page_regex: 页码的正则表达式
    # Returns:
    #   reference_str: 摘要字符串
    journal = miner_text_generator.extract_text(pdf_path)
    for i in range(len(journal)):
        reg_result = re.search(regex, journal[len(journal) - i - 1])
        if reg_result:
            reference_str = journal[len(journal) - i - 1][(reg_result.end()):].replace("\n", " ")
            for j in range(len(journal) - i - 1, len(journal)):
                reference_str = "{}{}".format(reference_str, re.sub(page_regex, "", journal[j]).replace("\n", " "))
            break
    return reference_str


def get_all_reference_in_path(folder_path, record_dict):
    # 获取路径下所有pdf的参考文献
    # Args:
    #   folder_path: 文件夹路径
    #   record_dict: 包含摘要等信息的列表
    # Returns:
    #   record_dict：字典，paper名称 -> paper信息（包括摘要、参考文献等）
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        if file_name.endswith(".pdf"):
            try:
                record_dict[file_name[:-4]]["reference"] = get_reference(folder_path + file_name)
                print(file_name)
            except:
                continue
    return record_dict


def get_all_reference_in_parent_path(parent_path):
    # 获取路径下所有子文件夹中pdf的参考文献
    # Args:
    #   parent_path: 文件夹路径
    # Returns:
    #   输出结果至json文件
    file_names = os.listdir(parent_path)
    for file_name in file_names:
        if os.path.isdir(os.path.join(parent_path,file_name)):
            print("==={}===".format(file_name))
            with open("{}{}.json".format(parent_path, file_name)) as f:
                record_list = json.load(f)
            record_dict = {}
            for record in record_list:
                record_dict[record["header"]] = record
            record_dict_add_reference = get_all_reference_in_path("{}{}/".format(parent_path, file_name), record_dict)
            with open("{}{}_with_reference.json".format(parent_path, file_name), "w") as f:
                json.dump(record_dict_add_reference, f)


if __name__ == '__main__':
    get_all_reference_in_parent_path("JMLR/")
