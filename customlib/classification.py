# -*- coding: utf-8 -*-
import os
import numpy as np
from sklearn import tree

class classification:
    """ファイルからのデータ読み込み
        決定木での学習
        木構造を解析し質問、回答を返す
    """

    def load(self):
        
        #相対パス取得
        base = os.path.dirname(os.path.abspath(__file__))

        #ファイルパス取得
        data_file = os.path.normpath(os.path.join(base, './data/data.tsv'))
        label_file = os.path.normpath(os.path.join(base, './data/label_nm.txt'))
        feature_file = os.path.normpath(os.path.join(base, './data/feature_nm.txt'))
        
        #データ読み込み
        self.data = np.loadtxt(data_file, delimiter='\t')
        self.label = open(label_file, 'r', encoding='utf-8').readlines()
        for i in range(len(self.label)):
            self.label[i] = self.label[i].rstrip("\n")
        self.feature = open(feature_file, 'r', encoding='utf-8').readlines()
        for i in range(len(self.feature)):
            self.feature[i] = self.feature[i].rstrip("\n")

        #学習
        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(self.data, self.label)

    def save(self, answer, feature_nm_list, data_list):
        
        feature_list = self.__get_feature_list(feature_nm_list)

        test_data = []
        for i in range(len(self.feature)):
            if i in feature_list:
                test_data.append(data_list[feature_list.index(i)])
            else:
                test_data.append("3")


        #相対パス取得
        base = os.path.dirname(os.path.abspath(__file__))
        #ファイルパス取得
        data_file = os.path.normpath(os.path.join(base, './data/data.tsv'))
        label_file = os.path.normpath(os.path.join(base, './data/label_nm.txt'))
        data_writer = open(data_file, 'a', encoding='utf-8')
        label_writer = open(label_file, 'a', encoding='utf-8')

        data_tsv = ""
        for data in test_data:

            if data_tsv != "":
                data_tsv = data_tsv + "\t"
            
            data_tsv = data_tsv + data

        data_writer.write(data_tsv + "\n")
        label_writer.write(answer + "\n")   

    def answer(self, feature_nm_list, data_list):
        
        feature_list = self.__get_feature_list(feature_nm_list)
        queation, answer = self.__recursion(0, 0, feature_list, data_list)

        return answer

    def queation(self, feature_nm_list, data_list):
                
        feature_list = self.__get_feature_list(feature_nm_list)
        queation, answer = self.__recursion(0, 0, feature_list, data_list)

        return queation

    def __get_feature_list(self, feature_nm_list):
        #特徴名からindex番号のリストを取得
        feature_list = []
        for feature_nm in feature_nm_list:
            if feature_nm in self.feature:
                feature_list.append(self.feature.index(feature_nm))
        return feature_list

    def __recursion(self, node_index, class_cnt, feature_list, data_list):         
        #tree構造のレンジ外なら(ERROR)
        if self.clf.tree_.node_count <= node_index:
            raise "tree構造のレンジ外"

        feature_index = self.clf.tree_.feature[node_index]
  
        #特徴が-2の場合終端ノードなので、labelを返す
        if str(feature_index) == "-2":
            value_list = self.clf.tree_.value[node_index][0].tolist()
            label_index = value_list.index(max(value_list))

            return "", self.clf.classes_[label_index]

        #現在の階層より、取得済みの回答が少ない場合、問題を返す
        if class_cnt > len(feature_list) - 1:
            return self.feature[feature_index], ""

        #treeの特徴と回答の特徴が一致しない場合(ERROR)
        if feature_list[class_cnt] != feature_index:
            raise "treeの特徴と回答の特徴が一致しない"

        feature_threshold = self.clf.tree_.threshold[node_index]

        #境界値以下の場合は左のノード、それ以外は右のノード
        if int(data_list[class_cnt]) <= feature_threshold:
            next_index = self.clf.tree_.children_left[node_index]
        else :
            next_index = self.clf.tree_.children_right[node_index]

        return self.__recursion(next_index, class_cnt + 1, feature_list, data_list)


if __name__ == '__main__':
    clf = classification()
    clf.load()
    print(clf.queation([], []))
    #print(clf.queation(["問1"], [2]))
    
