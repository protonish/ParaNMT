import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def open_json(fname):
    with open(fname) as json_file:
        data = json.load(json_file)
    return data

def dump_json(filename, data):
    #json_ready = json.dumps(data, sort_keys=True, ensure_ascii=False)
    output_file = open(filename, 'w')
    json.dump(data, output_file, sort_keys=True, encoding='utf8')
         
def subwords_to_words(subword_list):
    word_dict = {}
    tmp_word = []
    tmp_positions = []
    key = 0
    for idx, subword in enumerate(subword_list):
        if subword.find("@@") == len(subword) - 2:
            tmp_word.append(subword[:-2])
            tmp_positions.append(idx)
        else:
            tmp_word.append(subword)
            tmp_positions.append(idx)
            word_dict[key] = [tmp_word, tmp_positions]
            key = key + 1
            tmp_word = []
            tmp_positions = []
    return word_dict

def sentence_only(word_dict):
    sent = []
    for key in word_dict.keys():
        sent += word_dict[key][0]
    return sent


def build_text_matrix(side, json_filepath):
    source_target_dict = open_json(json_filepath)
    text_matrix = []
    if side.lower() in ['t', 'target']:
        for line in source_target_dict.keys():
            index_dict = subwords_to_words(source_target_dict[line]['t'])
            text_matrix.append(sentence_only(index_dict))
    elif side.lower() in ['s', 'source']:
        for line in source_target_dict.keys():
            index_dict = subwords_to_words(source_target_dict[line]['s'])
            text_matrix.append(sentence_only(index_dict))

    return text_matrix

if __name__ == "__main__":
    print 'tsted ok'
    # filepath = 'sentences_subwords.json'
    # json_dict = open_json(filepath)
    #
    # # target_words_and_subword_indices = subwords_to_words(json_dict['1938']['t'])
    # # print target_words_and_subword_indices[7][0]
    # # print ' '.join(target_words_and_subword_indices[7][0])
    # # print sentence_only(target_words_and_subword_indices)
    #
    # build_text_matrix('s',json_dict)