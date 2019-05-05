from flask import Flask, jsonify
from flask import request
from services.jobs import fetch_latest_jobs, get_total_jobs_count, search_jobs
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

@app.route('/jobs')
def search():
    search = request.args.get('search')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return search_jobs(search, page, per_page)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')