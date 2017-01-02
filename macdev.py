#!/usr/bin/env python

import os
import re
import urllib2
import subprocess

MACDEV_PATH = os.path.dirname(os.path.realpath(__file__))
DOTFILES_DIR = "dotfiles"

def remake_dir(path):
    full_path = os.path.expanduser(path)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)

def mk_dirs():
    # create a few standard directories
    basic_dirs = ["~/bin", "~/code"]
    for bdir in basic_dirs:
        remake_dir(bdir)

def copy_dotfiles():
    dotfile_dir = os.path.join(MACDEV_PATH, DOTFILES_DIR)
    dotfiles = os.listdir(dotfile_dir)
    for dotfile in dotfiles:
        ln_src = os.path.join(dotfile_dir, dotfile)
        ln_dest = os.path.expanduser("~/." + dotfile)
        if os.path.isfile(ln_dest):
            os.remove(ln_dest)
        os.symlink(ln_src, ln_dest)

def install_pathogen():
    pathogen_dest = os.path.expanduser("~/.vim/autoload/pathogen.vim")
    if not os.path.isfile(pathogen_dest):
        pathogen_url = "https://tpo.pe/pathogen.vim"
        pathogen = urllib2.urlopen(pathogen_url)
        with open(pathogen_dest, "w") as pathogen_file:
            pathogen_file.write(pathogen.read())

def vim_plugins():
    vim_dirs = ["~/.vim/autoload", "~/.vim/bundle"]
    for vdir in vim_dirs:
        remake_dir(vdir)
    install_pathogen()

    plugin_urls = [
            "git://github.com/tpope/vim-sensible.git",
            "git://github.com/tpope/vim-surround.git",
            "git://github.com/tpope/vim-commentary.git",
            "git://github.com/ctrlpvim/ctrlp.vim.git"
            ]

    dest_extractor = r'/([^/]+).git'
    for plugin_url in plugin_urls:
        dest_name = re.search(dest_extractor, plugin_url).group(1)
        dest = os.path.expanduser("~/.vim/bundle/" + dest_name)
        if not os.path.isdir(dest):
            git_cmd = ["git", "clone", plugin_url, dest]
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(git_cmd, stdout=devnull, stderr=subprocess.STDOUT)
    

if __name__ == "__main__":
    print("we on it")
    mk_dirs()
    copy_dotfiles()
    vim_plugins()

