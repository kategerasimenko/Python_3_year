from pymystem3 import Mystem
from flask import Flask
from flask import url_for, render_template, request, redirect
from collections import Counter

m = Mystem()
app = Flask(__name__)


def find_verbs(text):
    anas = m.analyze(text)
    verbs = [x for x in anas if 'analysis' in x and \
             x['analysis'][0]['gr'].split('=')[0].split(',')[0] == 'V']
    return verbs, len(verbs)/len(text.split())


def get_aspect(verb):
    chars = verb['analysis'][0]['gr'].split('=')[1]
    chars = chars.strip('()').split('|')
    if len(chars) > 1:
        chars = [x for y in chars for x in y.split(',')]
    else:
        chars = chars[0].split(',')
    if 'cов' in chars and 'несов' in chars:
        aspect = ['сов','несов']
    elif 'сов' in chars:
        aspect = ['сов']
    elif 'несов' in chars:
        aspect = ['несов']
    else:
        aspect = ['no aspect value']
    return aspect


def get_trans_aspect(verb):
    aspect = []
    after_pos = verb['analysis'][0]['gr'].split('=')[0].split(',')[1:]
    if len(after_pos) == 1:
        trans = after_pos[0]
    elif len(after_pos) > 1:
        aspect = [after_pos[-2]]
        trans = after_pos[-1]
    else:
        trans = 'no transitivity value'
    return trans, aspect


def get_info(verbs):
    tr = []
    asp = []
    for verb in verbs:
        aspect = get_aspect(verb)
        trans,aspect2 = get_trans_aspect(verb)
        if aspect2:
            aspect = aspect2
        asp += aspect
        tr.append(trans)
    return Counter(tr),Counter(asp)


def lemmas(verbs):
    all_lemmas = [x['analysis'][0]['lex'] for x in verbs]
    return Counter(all_lemmas).most_common()


def count_all(text):
    v,part = find_verbs(text)
    tr,asp = get_info(v)
    tr_count = Counter(tr)
    asp_count = Counter(asp)
    lem = lemmas(v)
    return len(v),part,tr,asp,lem


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('counts',**request.form),code=307)
    return render_template('index.html')


@app.route('/counts',methods=['GET','POST'])
def counts():
    if request.method == 'POST':
        text = request.form['text']
        len_v,part,tr,asp,lem = count_all(text)
        return render_template('counts.html',
                               len_v=len_v,
                               part=part,
                               tr=tr,
                               asp=asp,
                               lem=lem)
    return 'Enter the text at first'

if __name__ == '__main__':
    app.run(debug=True)
