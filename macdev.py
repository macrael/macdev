#!/usr/bin/env python

import os

MACDEV_PATH = os.path.dirname(os.path.realpath(__file__))
DOTFILES_DIR = "dotfiles"

def copy_dotfiles():
    dotfile_dir = os.path.join(MACDEV_PATH, DOTFILES_DIR)
    dotfiles = os.listdir(dotfile_dir)
    for dotfile in dotfiles:
        ln_src = os.path.join(dotfile_dir, dotfile)
        ln_dest = os.path.expanduser("~/." + dotfile)
        if os.path.isfile(ln_dest):
            os.remove(ln_dest)
        os.symlink(ln_src, ln_dest)
    

if __name__ == "__main__":
    print("we on it")
    copy_dotfiles()
