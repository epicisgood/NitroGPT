#! /bin/bash
pip install openai==0.28
pip install py-cord
pip install colorama
git clone https://github.com/epicisgood/nitrogpt
cd nitrogpt
git fetch
git pull
python main.py
