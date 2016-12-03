import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
import itertools
import json
import re
from collections import defaultdict as DefaultDict
import sys
import utils


def index_lookup(elements):
    result = DefaultDict(list)
    for index, keyy in enumerate(elements):
        result[keyy].append(index)
    return result


def get_distribution(filename):
    cached_stop_words = stopwords.words("english")
    text_matrix = []
    text_set_stop = []
    corpus = ""
    for line in open(filename):
        line = unicode(line, 'utf8')
        # text_matrix_inner = word_tokenize(line, language='english')
        text_matrix_inner = line.split()
        stop_removed = ' '.join([word for word in line.split() if word not in cached_stop_words])
        corpus += stop_removed
        stop_removed = word_tokenize(stop_removed, language='english')
        text_set_stop.append(stop_removed)
        text_matrix.append(text_matrix_inner)

    return text_matrix, text_set_stop


def match_index(freq_dist, text_matrix):
    key_count = 1
    index_dict = {}
    print "Extracting indices.."

    for key in freq_dist.keys():
        sys.stderr.write(".")
        if key_count % 150 == 0:
            sys.stderr.write("\n")
        _iterator = 0
        count = 0
        while _iterator < len(text_matrix):
            ind_dict = index_lookup(text_matrix[_iterator])

            if key in ind_dict:
                indices = ind_dict[key]
                inner_dict = {int(_iterator): indices}
                # print key," -- ", inner_dict
                if count > 0:
                    index_dict[key].update(inner_dict)
                else:
                    index_dict[key] = inner_dict
                    count += 1
            _iterator += 1
        key_count += 1

    return index_dict


if __name__ == "__main__":
    # input_file = "data/newstest2011.en"
    json_filepath = 'sentences_subwords.json'
    # whole_text, local_corpus = get_distribution(input_file)
    # print text_matrix
    local_corpus = utils.build_text_matrix('t', json_filepath)

    word_freq = nltk.FreqDist(itertools.chain(*local_corpus))
    print word_freq
    # unigrams = ngrams(tokenized_corpus, 1)

    print "Pruning words which occur only once.."
    count = 0
    freq_dict = {}
    for item in word_freq.items():
        # only keeping words which appear more than once
        if int(item[1]) > 1:
            # keeping words that have at least 1 letter of alphabet
            if re.search('[a-zA-Z]', item[0]):
                # building dictionary
                freq_dict[item[0]] = int(item[1])
                count += 1

    print count, " relevant words found!"

    # json_ready = json.dumps(freq_dict, sort_keys=True, ensure_ascii=False)
    freq_file = open('data/freq_dist_test1.json', 'w')
    # json.dump(json_ready, freq_file, encoding='utf8')
    json.dump(freq_dict, freq_file, sort_keys=True, encoding='utf8')
    print "Frequency Distribution saved in file."

    indices_dict = match_index(freq_dict, local_corpus)
    # json_ready = json.dumps(indices_dict, sort_keys=True, ensure_ascii=False)
    index_file = open('data/index_file1.json', 'w')
    json.dump(indices_dict, index_file, sort_keys=True, encoding='utf8')
    print "\nWord-Index pairs saved in file."
