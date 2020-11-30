# -*- encoding: utf-8 -*-
# 更新 story_class

import os
import random

file_path = 'fictions'
story_class = {}

for maindir, subdir, file_name_list in os.walk(file_path):
    # print(file_name_list)
    if len(file_name_list) == 0:
        continue
    fold_name = os.path.basename(maindir)
    if fold_name not in story_class.keys():
        story_class[fold_name] = {}
    for i, each in enumerate(file_name_list):
        story_class[fold_name][str(i)] = [each, int(100*random.random())]



with open('story_class.txt', 'w', encoding='utf-8') as f:
    f.write(str(story_class))
