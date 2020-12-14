# coding=utf-8
# 将每个txt文件划分成512长度的子序列
# 句中停用词是否去掉可视模型效果决定

import os


def split_to_subsequence(input_folder, output_folder, s_words_list, label, max_length):
    files = os.listdir(input_folder)
    file_lines = list()
    for index1, file in enumerate(files):
        file_path = os.path.join(input_folder, file)
        ori_f = open(file_path, 'r', encoding='utf-8')
        index_file = file.split('.')[0]
        ori_lines = ori_f.readlines()
        num_sub = 0
        new_line = ''
        new_lines = list()
        for index2, ori_line in enumerate(ori_lines):
            ori_line = ''.join(ori_line.split())
            # for word in s_words_list:
            #     ori_line = ori_line.replace(word, '')
            new_line = new_line + ori_line
            num_words = len(new_line)
            if num_words > round(0.6 * max_length):
                if num_words < max_length - 1:
                    new_line_push = new_line + '\t' + index_file + '_' + str(num_sub) + '\t' + str(label) + '\n'
                    new_lines.append(new_line_push)
                    new_line = ''
                else:
                    new_line_push = new_line[0:max_length - 2] + '\t' + index_file + '_' + str(num_sub) + '\t' + str(
                        label) + '\n'
                    new_lines.append(new_line_push)
                    new_line = new_line[max_length - 2:]
                num_sub += 1
            if index2 == len(ori_lines) - 1 and len(new_line) != 0:
                while len(new_line) > max_length - 1:
                    new_line_push = new_line[0:max_length - 2] + '\t' + index_file + '_' + str(num_sub) + '\t' + str(
                        label) + '\n'
                    new_lines.append(new_line_push)
                    new_line = new_line[max_length - 2:]
                    num_sub += 1
                new_line_push = new_line + '\t' + index_file + '_' + str(num_sub) + '\t' + str(label) + '\n'
                new_lines.append(new_line_push)
        file_lines.extend(new_lines)
    sample_type = input_folder.split('_')[0]
    output_txt = os.path.join(output_folder, sample_type + '_' + output_folder + '.txt')
    with open(output_txt, 'w+', encoding='utf-8') as f:
        f.writelines(file_lines)


def get_stop_words(path):
    words_list = []
    with open(path, 'r', encoding='gbk') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            words_list.append(line)
    return words_list


if __name__ == "__main__":
    stop_words_list = get_stop_words('hit_stopwords.txt')
    input_f = 'neg_test'
    max_length = 512
    output_f = 'test' + '_' + str(max_length)
    sample_label = 1 if input_f.split('_')[0] == 'pos' else 0
    if not os.path.isdir(output_f):
        os.makedirs(output_f)
    split_to_subsequence(input_f, output_f, stop_words_list, sample_label, max_length)
