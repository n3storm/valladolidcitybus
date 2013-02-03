from flask import Flask, render_template, request
from libs.valladolidcitybus import CityBus, Stop
from libs.caching import cached

"""
Run with gunicorn  sudo gunicorn -b 0.0.0.0:5000 -w 4 --debug --log-level debug web:app
"""

app = Flask(__name__)
auvasa = CityBus()

@app.route('/')
@cached()
def lines():
    """Get lines"""
    return render_template('lines.html', lines=auvasa.lines())
    

    
@cached()  
@app.route('/<line>')
def line(line):
    """Get line"""
    return render_template('line.html', line=auvasa.lines(line_id=line))

@app.route('/check/<line>/<stop>')
def check(line, stop):
    """Get line"""
    ourstop = Stop()
    check = ourstop.check(stop_id=stop, line_id=line)
    return render_template('check.html', check = check)

@cached()
@app.route('/about/')
def about():
    """Get lines"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
