from pyPiper import Node, Pipeline

import os

from utils import file_utils
from utils.logger import get_logger
from utils.tqdmUpdate import TqdmUpdate


class FileOutputNode(Node):
    def __init__(self, name, out_dir, **kwargs):
        self.out_dir = os.path.join(out_dir, name)
        file_utils.ensure_dir(self.out_dir)
        super().__init__(name, **kwargs)

    def derive_new_file_path(self, old_file, new_ext=None):
        old_fname = os.path.basename(old_file)

        if new_ext is not None:
            ext = new_ext
            if not ext.startswith("."):
                ext = "." + ext

            new_fname = file_utils.strip_ext(old_fname) + ext
        else:
            new_fname = old_fname

        return os.path.join(self.out_dir, new_fname)

    def log(self, level, msg):
        get_logger().log(level=level, msg="%s: %s" % (self.name, msg))



class FindFiles(Node):
    def setup(self, dir, ext="", prefix=""):
        self.files = file_utils.find_files(dir, prefix=prefix, ext=ext)
        self.size = len(self.files)

    def run(self, data):
        if len(self.files) > 0:
            self.emit(self.files.pop())
        else:
            self.close()


class ProgressPipeline(Pipeline):
    def run(self, update_callback=None, *args, **kwargs):
        if update_callback is None:
            with TqdmUpdate(*args, **kwargs) as pbar:
                super().run(update_callback=pbar.update)
        else:
            super().run(update_callback=update_callback)