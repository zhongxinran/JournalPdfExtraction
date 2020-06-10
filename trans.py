import os
import numpy as np
import json
import pandas as pd

os.chdir("/Users/bytedance/Desktop/JournalPdfExtraction/")
papers_dir = "./COLT/"
if not os.path.exists(papers_dir + "data/"):
    os.mkdir(papers_dir + "data/")

files = os.listdir(papers_dir)
files = [i for i in files if len(i) > 13]
files.sort()

total_dic = {}
for fi in files:
    with open(papers_dir + fi, 'r') as f:
        d = json.load(f)
        total_dic.update(d)

items = list(total_dic.keys())
for ind in items:
    if "reference" not in total_dic[ind].keys():
        out = total_dic.pop(ind)
    elif not total_dic[ind]["keywords"]:
        out = total_dic.pop(ind)

items = list(total_dic.keys())
pres = pd.DataFrame(None, columns=["pre", "after"])

for ind in items:
    pre_text = total_dic[ind]["reference"].strip()
    pre_dic = {"1": pre_text}
    after_text = total_dic[ind]["abstract"]
    if len(after_text) == 0: continue
    after_dic = {"1": after_text}
    head = "".join(ind.strip().split(" "))
    head = head.replace(",", "").replace(".", "").replace("-", "").replace("\"", "").replace("\'", "").replace("/",
                                                                                                               "").replace(
        "\\", "").replace(":", "")
    # key words
    concepts = total_dic[ind]["keywords"]
    concepts = [i for i in concepts if len(i) > 0]
    if len(concepts) == 0: continue
    csv_file = papers_dir + "data/concept_" + head + ".csv"
    df = pd.DataFrame({"concept": concepts}, index=range(len(concepts)))
    df.to_csv(csv_file, header=False, index=False)
    pre_file = "PRE_" + head + ".json"
    after_file = head + ".json"
    # 两个json file
    with open(papers_dir + "data/" + pre_file, 'w+') as f:
        json.dump(pre_dic, f)
    with open(papers_dir + "data/" + after_file, 'w+') as f:
        json.dump(after_dic, f)
    # 先后修关系
    pres = pres.append(pd.DataFrame({"pre": "PRE_" + head, "after": head}, index=[items.index(ind)]))

pres.to_csv(papers_dir + "data/COLT_prerequisite.csv", header=True, index=False)
print(pres.shape)
