#!/usr/bin/env python

import os
import re
import urllib.request
import subprocess

MACDEV_PATH = os.path.dirname(os.path.realpath(__file__))
MACDEV_DOTFILES_DIR = "dotfiles"
MACDEV_SUBLIME_PREFS_DIR = "sublime"
SUBLIME_PREFS_DIR = "~/Library/Application Support/Sublime Text 3/Packages/User/"
CODE_DIR = os.path.expanduser("~/code")
BIN_DIR = os.path.expanduser("~/bin")

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
    if not os.path.isfile("/opt/homebrew/bin/brew"):
        print("installing brew")
        brew_url = "https://raw.githubusercontent.com/Homebrew/install/master/install"
        brew_script = urllib.request.urlopen(brew_url)
        brew_cmd = ["/usr/bin/ruby", "-e", brew_script.read()]
        subprocess.call(brew_cmd)

def install_brew_pkgs():
    brew_pkgs = [ "nvm", "rbenv", "pyenv", "direnv" ]
    for pkg in brew_pkgs:
        check_cmd = ["brew", "ls", "--versions", pkg]
        if subprocess.call(check_cmd) == 1:
            brew_cmd = ["brew", "install", pkg]
            subprocess.call(brew_cmd)

def remake_dir(path):
    full_path = os.path.expanduser(path)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)

def mk_dirs():
    print("creating some standard directories")
    # create a few standard directories
    basic_dirs = [BIN_DIR, CODE_DIR, "~/.ssh"]
    for bdir in basic_dirs:
        remake_dir(bdir)

def copy_dotfiles():
    print("copying all dotfiles")
    dotfile_dir = os.path.join(MACDEV_PATH, MACDEV_DOTFILES_DIR)
    dotfiles = os.listdir(dotfile_dir)
    for dotfile in dotfiles:
        ln_src = os.path.join(dotfile_dir, dotfile)
        ln_dest = os.path.expanduser("~/." + dotfile)
        if os.path.isfile(ln_dest):
            os.remove(ln_dest)
        os.symlink(ln_src, ln_dest)

def copy_sublime_prefs():
    print("copying sublime prefs")
    dotfile_dir = os.path.join(MACDEV_PATH, MACDEV_SUBLIME_PREFS_DIR)
    dotfiles = os.listdir(dotfile_dir)
    for dotfile in dotfiles:
        ln_src = os.path.join(dotfile_dir, dotfile)
        ln_dest = os.path.expanduser(SUBLIME_PREFS_DIR + dotfile)
        if os.path.isfile(ln_dest):
            os.remove(ln_dest)
        os.symlink(ln_src, ln_dest)

def install_pathogen():
    pathogen_dest = os.path.expanduser("~/.vim/autoload/pathogen.vim")
    if not os.path.isfile(pathogen_dest):
        pathogen_url = "https://tpo.pe/pathogen.vim"
        pathogen = urllib.request.urlopen(pathogen_url)
        with open(pathogen_dest, "w") as pathogen_file:
            pathogen_file.write(pathogen.read())

def git_clone(git_url, dest_dir):
    dest_extractor = r'/([^/]+).git'
    dest_name = re.search(dest_extractor, git_url).group(1)
    dest = os.path.join(os.path.expanduser(dest_dir), dest_name)
    if not os.path.isdir(dest):
        git_cmd = ["git", "clone", git_url, dest]
        silent_call(git_cmd)
    return dest

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
            "git://github.com/altercation/vim-colors-solarized.git",
            "git://github.com/sheerun/vim-polyglot.git"
            ]

    plugin_dir = "~/.vim/bundle/"
    for plugin_url in plugin_urls:
        git_clone(plugin_url, plugin_dir)

def install_my_tools():
    tools = [
            {"url": "git@github.com:macrael/webnull.git"}
            ]

    for tool in tools:
        path = git_clone(tool["url"], CODE_DIR)

if __name__ == "__main__":
    print("we on it")
    install_xcode_tools()
    install_brew()
    # install_brew_pkgs()
    mk_dirs()
    copy_dotfiles()
    copy_sublime_prefs()
    # vim_plugins()
    install_my_tools()
