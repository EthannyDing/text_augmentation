import os
import re
import random
import numpy as np
# import pandas as pd
# import spacy
from text_augmentation.utils.file_io import txt_io, excel_io
# import tensorflow as tf

"""
    1. Easy Data Augmentation Techniques
        * random swapping
        * random insertion
        * random deletion
        * random replacement
        
    2. Back Translation
    3. Embedding Techniques
"""


class EasyAugmentation:

    def __init__(self, vocab_path=None):
        self.vocab_path = vocab_path
        self.vocab = []

    def load_vocab(self):
        """Load existing vocabulary file"""
        if os.path.isfile(self.vocab_path):
            self.vocab = txt_io(self.vocab_path, action='r')
        else:
            print("No vocab file is found.")

    def save_vacab(self, filepath):
        """save vocabulary"""
        txt_io(filepath, action="w", write_lines=self.vocab)

    def create_vocab_from_file(self, text_filepath):
        """Create vocabulary from given file of sentences"""
        with open(text_filepath, "r") as f:
            lines = f.read().splitlines()

        total_vocab = " ".join(lines).split()
        self.vocab = list(set(total_vocab))
        print("{} vocabularies created.".format(len(self.vocab)))

    def swapping(self, text, n_iteration=1, position="random"):
        """Swapping (randomly or specific positional) words in the text.
            :arg n_iteration: the number of swaps to be performed.
            :arg position: randomly swapping or specified swaps"""
        assert position == "random" or type(position) == tuple, "position should be either 'random' or a tuple."
        words = text.split()
        length = len(words)

        if length < 2:
            return text

        if position == "random":
            for _ in range(n_iteration):
                index_1, index_2 = np.random.choice(range(length), 2, replace=False)
                words[index_1], words[index_2] = words[index_2], words[index_1]
        else:
            index_1, index_2 = position
            words[index_1], words[index_2] = words[index_2], words[index_1]

        new_text = " ".join(words)

        return new_text

    def deletion(self, text, n_words=2, position="random"):
        """Deleting (randomly or specific positional) words in the text.
            :arg n_words: the number of word to be deleted.
            :arg position: randomly deleting or specified deletion by index
            :return same text of word number is less than 2, or less than or or equal to n_word."""
        assert position == "random" or type(position) == tuple, "position should be either 'random' or a tuple."
        words = text.split()
        length = len(words)

        if length < 2 or n_words >= length:
            return text

        if position == "random":
            indices = np.random.choice(range(length), n_words, replace=False)
        else:
            indices = position

        words = np.delete(words, indices)
        new_text = " ".join(words)

        return new_text

    def insertion(self, text, n_words=2, position="random"):
        """Inserting words into text
            :arg n_words: the number of word to be inserted.
            :arg position: randomly inserting or specified inserting by index"""
        assert position == "random" or type(position) == tuple, "position should be either 'random' or a tuple."
        words = text.split()
        length = len(words)

        if position == "random":
            indices = np.random.choice(range(length + 1), n_words, replace=False)
        else:
            indices = position

        for i in indices:
            insert_word = random.choice(self.vocab)
            words = words[:i] + [insert_word] + words[i:]

        new_text = " ".join(words)

        return new_text

    def replacement(self, text, n_words=2, position="random"):
        """Inserting words into text
            :arg n_words: the number of word to be inserted.
            :arg position: randomly inserting or specified inserting by index"""
        assert position == "random" or type(position) == tuple, "position should be either 'random' or a tuple."
        words = text.split()
        length = len(words)

        if n_words >= length:
            return text

        if position == "random":
            indices = np.random.choice(range(length), n_words, replace=False)
        else:
            indices = position

        for i in indices:
            insert_word = random.choice(self.vocab)
            words[i] = insert_word

        new_text = " ".join(words)

        return new_text


class EasyAugmentationFrench(EasyAugmentation):

    def __init__(self, vocab_path=None):
        super().__init__(vocab_path)
        self.articles = ["le", "la", "les", "l'",
                         "un", "une", "des", "du",
                         "de la", "de l'"]

    def add_article(self, text, article="random"):
        """Add a article to text, randomly or specified if text is without article.
           otherwise, replace current article with another."""
        words = text.split()
        all_articles = self.articles

        if article == "random":
            first_word = words[0].lower()
            first_two_words = " ".join(words[:2]).lower()
            if first_word in self.articles:
                all_articles.remove(first_word)
                words = words[1:]  # remove first article
                new_article = random.choice(all_articles)

            elif first_two_words in self.articles:
                all_articles.remove(first_two_words)
                words = words[1:]  # remove first two articles
                new_article = random.choice(all_articles)

            else:
                new_article = random.choice(all_articles)

        else:
            new_article = article

        words = [new_article] + words
        new_text = " ".join(words)

        return new_text


class EasyAugmentationPipeline(EasyAugmentationFrench):

    def __init__(self):
        super().__init__()
        # self.src_lang = src_lang
        # self.tgt_lang = tgt_lang
        self.input_data = []
        self.new_data = []
        self.methods = ["swapping", "deletion", "replacement", "insertion"]
        self.fra_methods = ["add_article"]
        # self.original_file = None

    def read_files(self, input_file):
        """read input files"""
        if (type(input_file) is list) and len(input_file) == 2:
            src_lines = txt_io(input_file[0], action='r')
            tgt_lines = txt_io(input_file[1], action='r')
            self.input_data = list(zip(src_lines, tgt_lines))

        elif (type(input_file) is str) and (os.path.splitext(input_file)[1] == ".xlsx"):
            df = excel_io(input_file, action='r')
            cols = df.columns
            self.input_data = list(zip(df[cols[0]], df[cols[1]]))
        else:
            raise Exception("input file not supported.")

        print("\n{} parallel data read".format(len(self.input_data)))

    def save_new_data(self, output_file):
        # df = pd.DataFrame(self.new_data, columns=["source", "target"])
        if (type(output_file) is list) and len(output_file) == 2:
            txt_io(output_file[0], action='w', write_lines=[p[0] for p in self.new_data])
            txt_io(output_file[1], action='w', write_lines=[p[1] for p in self.new_data])
        elif (type(output_file) is str) and (os.path.splitext(output_file)[1] == ".xlsx"):
            excel_io(output_file, action='w', write_df=self.new_data)
        else:
            raise Exception("output file not supported.")

    def create_bad_instance_from_good(self,
                                      original_files,
                                      vocab_path,
                                      alter_source=True,
                                      num_instances=100):
        """Create bad instances (randomly) from original TM/TB file.
            :arg original_files: input original TM/TB file
            :arg vocab_path: vocab filepath of specified src or tgt language.
            :arg lang: text of which language will be used to create bad instances.
            :arg randomly: randomly create bad instances or not.
            :arg num_instances: number of instance to create."""
        self.read_files(original_files)
        self.vocab_path = vocab_path  # load specified
        self.load_vocab()
        num_created = 0
        length = len(self.input_data)

        while num_created < num_instances:
        # for j, i in enumerate(np.random.randint(0, len(self.input_data), num_instances)):
            ind = random.choice(range(length))
            src, tgt = self.input_data[ind]
            method = random.choice(self.methods)
            fra_method = None
            param = random.choice(range(1, 3))
            if alter_source:
                print("\nOriginal : {}".format(src))
                new_text = self.__getattribute__(method)(src, param)
                new_pair = (new_text, tgt)

            else:
                print("\nOriginal: {}".format(tgt))
                if random.choice([False] * 9 + [True]):  # 10% of time, add articles
                    fra_method = random.choice(self.fra_methods)
                    new_text = self.__getattribute__(fra_method)(tgt)
                else:
                    new_text = self.__getattribute__(method)(tgt, param)

                new_pair = (src, new_text)

            method_used = fra_method if fra_method else method
            print("{}: {}".format(method_used, new_text))

            if (src, tgt) != new_pair:
                self.new_data.append(new_pair)
                num_created += 1


def test_create_vocab():

    vocab_file = "/linguistics/ethan/DL_Prototype/text_augmentation/text_augmentation/vocab/final_vocab.fra"
    text_filepath = "/linguistics/ethan/DL_Prototype/datasets/TB_TQA/good_merged.fra"
    ea = EasyAugmentation()
    ea.create_vocab_from_file(text_filepath)
    ea.save_vacab(vocab_file)

def test_run_each_method():

    vocab_file = "/linguistics/ethan/DL_Prototype/text_augmentation/vocab/vocab.txt"
    ea = EasyAugmentation(vocab_file)
    ea.load_vocab()
    text = 'Financial assets are crucial to our success.'

    print("\nOriginal : {}".format(text))
    print("Swapping : {}".format(ea.swapping(text, n_iteration=1, position="random")))
    print("Deleting : {}".format(ea.deletion(text, n_words=2, position="random")))
    print("Inserting: {}".format(ea.insertion(text, n_words=2, position="random")))
    print("Replacing: {}".format(ea.replacement(text, n_words=2, position="random")))
    print("\n")

def test_frenchTextAug():
    vocab_file = "/linguistics/ethan/DL_Prototype/text_augmentation/vocab/vocab.txt"
    eaf = EasyAugmentationFrench(vocab_file)

    text = "les siège social"
    print("\nOriginal : {}".format(text))
    print("Add Article: {}".format(eaf.add_article(text, article="random")))

def test_pipeline():
    rootpath = "/linguistics/ethan/DL_Prototype/datasets/TB_TQA/"
    input_files = [os.path.join(rootpath, "train/20210510.good.eng"),
                   os.path.join(rootpath, "train/20210510.good.fra")]
    output_file = [os.path.join(rootpath, "synthetic/20210510.bad.eng"),
                   os.path.join(rootpath, "synthetic/20210510.bad.fra")]
    vocab_path = "/linguistics/ethan/DL_Prototype/text_augmentation/text_augmentation/vocab/final_vocab.fra"
    pipe = EasyAugmentationPipeline()
    pipe.create_bad_instance_from_good(input_files, vocab_path, alter_source=False, num_instances=14572)
    pipe.save_new_data(output_file)

if __name__ == "__main__":

    # test_create_vocab()
    # test_run_each_method()
    # test_frenchTextAug()
    test_pipeline()
