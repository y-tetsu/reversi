#!/usr/bin/env python
import glob
import os
import shutil


def install():
    src_dir = os.path.dirname(__file__)
    dst_dir = os.path.join(os.getcwd(), "reversi_examples")

    print("Install reversi examples to {} ...".format(dst_dir))

    shutil.rmtree(dst_dir, ignore_errors=True)
    os.makedirs(os.path.join(dst_dir, "extra"))
    os.makedirs(os.path.join(dst_dir, "extra/perl/bottomright"))
    os.makedirs(os.path.join(dst_dir, "extra/python/topleft"))
    os.makedirs(os.path.join(dst_dir, "extra/vbscript/randomcorner"))
    os.makedirs(os.path.join(dst_dir, "extra/sample_input"))

    patterns = ["[0-5]*.py", "*.bat", "*.json", "*.ico", "extra/*.json", "extra/perl/bottomright/*.pl", "extra/python/topleft/*.py", "extra/vbscript/randomcorner/*.vbs", "extra/sample_input/*.txt"]  # noqa: E501

    for pattern in patterns:
        srcs = glob.glob(os.path.join(src_dir, pattern))

        for src in srcs:
            relpath = os.path.relpath(src, src_dir)
            dst = os.path.join(dst_dir, relpath)

            print("    {}".format(relpath))
            shutil.copyfile(src, dst)


if __name__ == "__main__":
    install()
