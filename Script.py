from pyPiper import Node, Pipeline
from tqdm import tqdm
import json

class Generate(Node):
    def setup(self, size):
        self.size = size
        self.pos = 0

    def run(self, data):
        if self.pos < self.size:
            self.emit(self.pos)
            self.pos = self.pos + 1
        else:
            self.close()

class Square(Node):
    def run(self, data):
        # print(data)
        self.emit(data ** 2)


class Printer(Node):
    def run(self, data):
        print(data)
        with open('output.json', 'a') as f:
            f.write(str(data) + "\n")

# class TqdmUpdate(tqdm):
class TqdmUpdate():
    def update(self, done, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.n = done
        # print(str(self.n) + '/' + str(self.total))
        # super().refresh()


if __name__ == '__main__':
    pipeline = Pipeline(Generate("gen", size=10) | Square("square") | Printer("print"), n_threads=8, quiet = True)
    pbar = TqdmUpdate()
    pipeline.run(update_callback=pbar.update)
    