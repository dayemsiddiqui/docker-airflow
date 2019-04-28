from flask import Flask, jsonify
from flask import request
from services.jobs import fetch_latest_jobs, get_total_jobs_count
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return fetch_latest_jobs(page, per_page)

@app.route('/jobs/count')
def get_jobs_counts():
    return get_total_jobs_count()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')