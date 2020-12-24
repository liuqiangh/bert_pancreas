# coding=utf-8
# 文本数据表中没有并发症标签
# 结合并发症表即research.lqh_t_cancer_complicatiion_sure表给文本数据表
# research.lqh_t_cancer_note_pre_copy.csv表打标签
# research.lqh_t_cancer_note_pre_copy表已经对“病程记录-入院后72小时谈话记录”、
# “病程记录-转入记录”、“病程记录-首次病程记录”做了处理，具体看md文件
# 目前思路是
# 1、将同一个人的文本数据整合成一个txt，txt以visit_record_id命名
# 2、结合lqh_t_cancer_complicatiion_sure给上述txt打标签
import os
import csv
import shutil
import random


def add_label_and_split(label_file, note_file):
    """根据并发症表将文本进行正负样本划分"""
    # label_lines = list(csv.reader(open(label_file, 'r', encoding='gbk')))
    # label_list = []
    # for index, line in enumerate(label_lines):
    #     if index == 0:
    #         continue
    #     label_list.append(line[0])
    # name_files = os.listdir(note_file)

    pos_folder = note_file + '/note_pos'
    neg_folder = note_file + '/note_neg'
    # if not os.path.isdir(pos_folder):
    #     os.makedirs(pos_folder)
    # if not os.path.isdir(neg_folder):
    #     os.makedirs(neg_folder)
    # for file_name in name_files:
    #     file_path = os.path.join(note_file, file_name)
    #     if file_name.split('.')[0] in label_list:
    #         shutil.move(file_path, pos_folder)
    #     else:
    #         shutil.move(file_path, neg_folder)

    # 划分数据集
    split_data(pos_folder, 'pos')
    split_data(neg_folder, 'neg')


# two types : train and test
# def split_data(folder, sample_type, radio=0.7):
#     name_files = os.listdir(folder)
#     file_num = len(name_files)
#     index_list = random.sample(range(0, file_num), round(radio * file_num))
#
#     # 上级目录
#     parent_dir = folder.split('/')[0]
#     train_folder = parent_dir + '/note_split_2/' + sample_type + '_train/'
#     test_folder = parent_dir + '/note_split_2/' + sample_type + '_test/'
#     if not os.path.isdir(train_folder):
#         os.makedirs(train_folder)
#     if not os.path.isdir(test_folder):
#         os.makedirs(test_folder)
#     for index, file_name in enumerate(name_files):
#         file_path = os.path.join(folder, file_name)
#         if index in index_list:
#             shutil.copy(file_path, train_folder)
#         else:
#             shutil.copy(file_path, test_folder)


# three types : train test validation
def split_data(folder, sample_type, radio_train=0.6, radio_val=0.2):
    name_files = os.listdir(folder)
    file_num = len(name_files)
    index_list_train_and_val = random.sample(range(0, file_num), round((radio_train + radio_val) * file_num))
    index_list_val = random.sample(index_list_train_and_val, round(file_num*radio_val))

    # 上级目录
    parent_dir = folder.split('/')[0]
    train_folder = parent_dir + '/note_split_3/' + sample_type + '_train/'
    val_folder = parent_dir + '/note_split_3/' + sample_type + '_val/'
    test_folder = parent_dir + '/note_split_3/' + sample_type + '_test/'
    if not os.path.isdir(train_folder):
        os.makedirs(train_folder)
    if not os.path.isdir(val_folder):
        os.makedirs(val_folder)
    if not os.path.isdir(test_folder):
        os.makedirs(test_folder)
    for index, file_name in enumerate(name_files):
        file_path = os.path.join(folder, file_name)
        if index in index_list_train_and_val:
            if index in index_list_val:
                shutil.copy(file_path, val_folder)
            else:
                shutil.copy(file_path, train_folder)
        else:
            shutil.copy(file_path, test_folder)


def integrate_pre_note(note_file, output_file):
    """将同一次visit的文本数据整合成一个txt,第一行为表头"""
    note_lines = list(csv.reader(open(note_file, 'r', encoding='gbk')))
    if not os.path.isdir(output_file):
        os.makedirs(output_file)

    temp_id = note_lines[1][0]
    text = ''
    file_name = os.path.join(output_file, temp_id + '.txt')
    for index, line in enumerate(note_lines):
        if index == 0:
            continue
        visit_id = line[0]
        if visit_id != temp_id:
            with open(file_name, 'w+', encoding='utf-8') as f:
                f.write(text)
            text = ''
            temp_id = visit_id
            file_name = os.path.join(output_file, temp_id + '.txt')

        text = text + line[4]
        if index == len(note_lines) - 1:
            with open(file_name, 'w+', encoding='utf-8') as f:
                f.write(text)


if __name__ == "__main__":
    complication_csv = 'research.lqh_t_cancer_complication_sure.csv'
    note_csv = 'research.lqh_t_cancer_note_pre_copy.csv'
    sub_folder = 'note'
    # integrate_pre_note(note_csv, sub_folder)
    add_label_and_split(complication_csv, sub_folder)
