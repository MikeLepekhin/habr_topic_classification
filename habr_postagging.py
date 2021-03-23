import os
import pickle
from pathlib import Path
from multiprocessing import Process

from ufal.udpipe import Model, Pipeline
from conllu import parse


class HabrPostagging:
    def __init__(self):
        # https://github.com/jwijffels/udpipe.models.ud.2.0/blob/master/inst/udpipe-ud-2.0-170801/russian-ud-2.0-170801.udpipe
        self.model = Model.load("russian-ud-2.0-170801.udpipe")
        self.pipeline = Pipeline(model, 'generic_tokenizer', '', '', '')
        self.reset_counter()

    def reset_counter(self):
        self.__pos_couter = {}

    def get_counter(self):
        return self.__pos_couter

    def __update_counter(self, pos):
        if pos in self.__pos_couter:
            self.__pos_couter[pos] += 1
        else:
            self.__pos_couter[pos] = 1

    def tag_file(self, input_file, output_file):
        text = pickle.load(open(input_file, 'rb'))['text']
        # Вообще-то питоновская обёртка udpipe сильно багованная, но на всех наших даннных отработала корректно.
        # Других парсеров, умеющих работать с русским, насколько мне известно, нет.
        parsed = self.pipeline.process(text)
        parsed = parse(parsed)
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in parsed:
                for word in sentence:
                    self.__update_counter(word['upos'])
                    f.write('\t'.join([word['form'], word['lemma'], word['upos'], str(word['feats'])]) + '\n')

    def tag_files(self, files, input_dir, output_dir, log=False):
        for filename in files:
            input_file = os.path.join(input_dir, filename)
            if os.path.isfile(input_file):
                if log:
                    print(input_file)
                output_file = os.path.join(output_dir, filename)
                output_file = os.path.splitext(output_file)[0] + '.tsv'
                self.tag_file(input_file, output_file)

    def tag_dir(self, input_dir, output_dir, log=False):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.tag_files(os.listdir(input_dir), input_dir, output_dir, log)


def tag_files(files, input_dir, output_dir):
    hp = HabrPostagging()
    hp.tag_files(files, input_dir, output_dir)


def tag_dir_multiproc(input_dir, output_dir, num_procs):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    files = os.listdir(input_dir)
    procs = []
    for i in range(num_procs):
        proc = Process(target=tag_files, args=(files[i::num_procs], input_dir, output_dir))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()


if __name__ == '__main__':
    tag_dir_multiproc('clean_files', 'pos', 4)
