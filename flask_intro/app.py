from flask import Flask, request, redirect, render_template
from collections import Counter
from os.path import isfile

app = Flask(__name__)

@app.route('/')
def index():
    if request.args:
        d = request.args
        with open('data.txt','a',encoding='utf-8') as f:
            f.write(d['name']+'\t'+d['choice']+'\n')
            return redirect('/result')
    return render_template('index.html')

@app.route('/result')
def results():
    if isfile('data.txt'):
        with open('data.txt','r',encoding='utf-8') as f:
            lines = f.readlines()
        names = [x.split('\t')[0].strip() for x in lines]
        choices = [x.split('\t')[1].strip() for x in lines]
        names_count = dict(Counter(names))
        choice_count = dict(Counter(choices))
        return render_template('result.html',ch = choice_count, n = names_count)
    return ('No results yet!')

if __name__ == '__main__':
    app.run()
        
            
