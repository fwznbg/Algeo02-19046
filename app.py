from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/concept")
def concept():
	return render_template("concept.html")
	
@app.route("/howto")
def howto():
	return render_template("howto.html")
	
@app.route("/input_file")
def input_file():
	return render_template("file.html")
	
@app.route("/about")
def about():
	return render_template("about.html")
	
@app.route("/motivational_video")
def motivational_video():
	return render_template("video.html")
	
@app.route("/result")
def result():
	return render_template("result.html")

if (__name__ == "__main__"):
	app.run(debug=True,host="0.0.0.0",port=80)
