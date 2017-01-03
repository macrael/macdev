#!/usr/bin/env python

import os
import re
import urllib2
import subprocess

MACDEV_PATH = os.path.dirname(os.path.realpath(__file__))
DOTFILES_DIR = "dotfiles"

def silent_call(cmd):
    with open(os.devnull, 'w') as devnull:
        retcode = subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)
        return retcode

def install_xcode_tools():
    xcode_cmd = ["xcode-select", "--install"]
    retcode = silent_call(xcode_cmd)    
    if retcode == 0:
        print("rerun after you've installed the xcode tools")
        exit(0)
    else:
        print("xcode tools like git are installed")

def install_brew():
    if not os.path.isfile("/usr/local/bin/brew"):
        print("installing brew")
        brew_url = "https://raw.githubusercontent.com/Homebrew/install/master/install"
        brew_script = urllib2.urlopen(brew_url)
        brew_cmd = ["/usr/bin/ruby", "-e", brew_script.read()]
        subprocess.call(brew_cmd)

def remake_dir(path):
    full_path = os.path.expanduser(path)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)

def mk_dirs():
    print("creating some standard directories")
    # create a few standard directories
    basic_dirs = ["~/bin", "~/code"]
    for bdir in basic_dirs:
        remake_dir(bdir)

def copy_dotfiles():
    print("copying all dotfiles")
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
    print("configuring vim")
    vim_dirs = ["~/.vim/autoload", "~/.vim/bundle"]
    for vdir in vim_dirs:
        remake_dir(vdir)
    install_pathogen()

    plugin_urls = [
            "git://github.com/tpope/vim-sensible.git",
            "git://github.com/tpope/vim-surround.git",
            "git://github.com/tpope/vim-commentary.git",
            "git://github.com/ctrlpvim/ctrlp.vim.git",
            "git://github.com/altercation/vim-colors-solarized.git"
            ]

    dest_extractor = r'/([^/]+).git'
    for plugin_url in plugin_urls:
        dest_name = re.search(dest_extractor, plugin_url).group(1)
        dest = os.path.expanduser("~/.vim/bundle/" + dest_name)
        if not os.path.isdir(dest):
            git_cmd = ["git", "clone", plugin_url, dest]
            silent_call(git_cmd)
    

if __name__ == "__main__":
    print("we on it")
    install_xcode_tools()
    install_brew()
    mk_dirs()
    copy_dotfiles()
    vim_plugins()

