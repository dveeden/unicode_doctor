#!/usr/bin/python3
from flask import Flask, jsonify, render_template, request, send_from_directory
from unicode_doctor import DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor

app = Flask(__name__)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

@app.route('/api/v1/make_guess/')
def make_guess():
    good = request.args.get('good', type=str)
    bad = request.args.get('bad', type=str)
    results = {}
    nr = 0
    for res in DecodeEncodeUnicodeDoctor.make_guess(str_bad=bad,str_good=good):
        results[nr] = {'issue': res.issue, 'acceptable': res.acceptable}
        nr += 1
    for res in ForcedAsciiUnicodeDoctor.make_guess(str_bad=bad,str_good=good):
        results[nr] = {'issue': res.issue, 'acceptable': res.acceptable}
        nr += 1

    return jsonify(results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
