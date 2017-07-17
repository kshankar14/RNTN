#!/bin/env python3

import os
from collections import defaultdict

from nltk.parse import CoreNLPParser
from nltk.tree import ParentedTree

import util

UNK = 'UNK'

WORD_MAP_FILENAME = 'models/word_map.pickle'


def parse(text):
    parser = CoreNLPParser("http://localhost:9000")
    result = parser.raw_parse(text.lower())
    trees = [tree for tree in result]
    for tree in trees:
        tree.chomsky_normal_form()
        tree.collapse_unary(collapseRoot=True, collapsePOS=True)
    trees = [ParentedTree.convert(tree) for tree in trees]
    return trees


def isleaf(tree):
    return isinstance(tree, ParentedTree) and tree.height() == 2


def traverse(tree, f=print, args=None, leaves=False):
    if leaves:
        if isleaf(tree):
            f(tree, args)
            return
    else:
        f(tree, args)
        if isleaf(tree):
            return
    for child in tree:
        traverse(child, f, args)


def build_word_map():
    print("Building word map...")
    with open("trees/train.txt", "r") as f:
        trees = [ParentedTree.fromstring(line.lower()) for line in f]

    print("Counting words...")
    words = defaultdict(int)
    for tree in trees:
        for token in tree.leaves():
            words[token] += 1

    word_map = dict(zip(words.keys(), range(len(words))))
    word_map[UNK] = len(words)  # Add unknown as word
    util.save_to_file(word_map, WORD_MAP_FILENAME)
    return word_map


def load_word_map():
    if not os.path.isfile(WORD_MAP_FILENAME):
        return build_word_map()
    print("Loading word map...")
    return util.load_from_file(WORD_MAP_FILENAME)


def load_trees(dataset='train'):
    filename = "trees/{}.txt".format(dataset)
    with open(filename, 'r') as f:
        print("Reading '{}'...".format(filename))
        trees = [ParentedTree.fromstring(line.lower()) for line in f]
    return trees


if __name__ == '__main__':
    word_map = load_word_map()
