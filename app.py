from flask import Flask, url_for, request, render_template
app = Flask(__name__)
# -----------------Task-----------------------
import socket
import os

# ------------------BD------------------------
import redis
cache = redis.Redis(host='redis', port=6379)
cache.mset({
	"q": "й",
	"w": "ц",
	"e": "у",
	"r": "к",
	"t": "е",
	"y": "н",
	"u": "г",
	"i": "ш",
	"o": "щ",
	"p": "з",
	"a": "ф",
	"s": "ы",
	"d": "в",
	"f": "а",
	"g": "п",
	"h": "р",
	"j": "о",
	"k": "л",
	"l": "д",
	"z": "я",
	"x": "ч",
	"c": "с",
	"v": "м",
	"b": "и",
	"n": "т",
	"m": "ь",
})


def translate(lang_from:str, lang_to:str, txt:str):
	a = ""
	print(lang_from, lang_to, txt) #TO BE LOGGED
	for c in txt:
		nxt = cache.get(c)
		if (str(nxt) != "None"):
			a += nxt.decode('unicode-escape').encode('latin1').decode('utf-8')
		else:
			a += c
	return a


# ---------------Flask part-------------------
@app.route('/')
def index():
	return render_template("index.html", name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route('/',methods = ['POST'])
def login():
	if request.method == 'POST':
		# # get form data
		initial = request.form['input_lang']
		target = request.form['target_lang']
		text = request.form['text']
		# render template
		output = translate(initial, target, text)
		return render_template("index.html", output=output, name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug = True)