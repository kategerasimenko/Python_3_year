# site - kategerasimenko.pythonanywhere.com

from flask import Flask
from flask import render_template, request
from from_vk import vk_wordforms
from count_verbs import count_all
from subst_words import change_words

app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/counts',methods=['GET','POST'])
def counts():
    if request.method == 'POST':
        text = request.form['text']
        len_v,part,tr,asp,lem = count_all(text)
        return render_template('counts.html',len_v=len_v,part=part,tr=tr,
                               asp=asp,lem=lem,show=True)

    return render_template('counts.html',len_v=None,part=None,tr={},
                           asp={},lem=[],show=False)


@app.route('/vk_wordforms',methods=['GET','POST'])
def vk():
    if request.method == 'POST':
        group = request.form['group']
        most_freq,found = vk_wordforms(group)
        return render_template('vk.html',data=most_freq,found=found)
    return render_template('vk.html',data=[])

@app.route('/change_words',methods=['GET','POST'])
def change():
    if request.method == 'POST':
        text = request.form['text']
        answer = change_words(text)
        return render_template('change.html',answer=answer,text=text)
    return render_template('change.html',answer='',text='')

if __name__ == '__main__':
    app.run(debug=True)