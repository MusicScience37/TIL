#!/bin/bash

pipenv sync --dev

git config --global --add safe.directory /workspaces/til
pipenv run pre-commit install

git config gpg.program gpg2
git config commit.gpgsign true
git config tag.gpgsign true

git lfs install

echo "source /usr/share/bash-completion/completions/git" >> ~/.bashrc
