import json
import os


def merge_keywords_in_parent_path(parent_path):
    # 合并父文件夹中的所有关键词
    # Args:
    #   parent_path: 文件夹路径
    # Returns:
    #   输出结果至json文件
    keywords = []
    file_names = os.listdir(parent_path)
    for file_name in file_names:
        if os.path.isdir(os.path.join(parent_path, file_name)):
            with open("{}{}_with_reference_and_keywords.json".format(parent_path, file_name)) as f:
                record_dict = json.load(f)
            for key in record_dict:
                if "keywords" in record_dict[key].keys() and record_dict[key]["keywords"] != None:
                    for keyword in record_dict[key]["keywords"]:
                        if keyword != "":
                            keywords.append(keyword)
    keywords = list(set(keywords))
    print(keywords)
    with open("{}keywords.json".format(parent_path), "w") as f:
        json.dump(keywords, f)


if __name__ == '__main__':
    merge_keywords_in_parent_path("COLT/")
