# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import SearchFiles
import os
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST":
        search = request.form['search']
    return render_template("bio_form.html")

@app.before_first_request
@app.route('/showbio', methods=['POST','GET'])
def showbio():
    search = request.args.get('search')
    SearchFiles.command = search
    SearchFiles.main()
    result = '<p>找到{}个结果。</p>\n'.format(SearchFiles.numDocs)
    for i in SearchFiles.results:
        result += "<p><font size=5><a href = \"{}\">{}</a></font></p>\n<p><font size=4>{}</font></p>\n<p><font size=3 color=green>{}</font></p>\n".format(i[2], i[3],i[1],i[2])
    try:
        os.remove("templates/result.html")
    except:
        i = 1
    file = open("templates/result.html","w")
    file.write(result)
    file.close()
    if request.method == "POST":
        search = request.form['search']
    return render_template("show_bio.html", search=search)

# @app.route('/index', methods=['GET'])
# def hello():
#     try:
#         username = request.args.get('username')
#         return render_template("index.html", name=username)
#     except:
#         return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
