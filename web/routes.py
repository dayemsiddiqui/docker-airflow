from app import app
from flask import request, jsonify
from services.jobs import fetch_latest_jobs, get_total_jobs_count, search_jobs, get_job_details


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


@app.route('/ping')
def test():
    return jsonify('pong')


@app.route('/jobs/<job_id>')
def job_detail(job_id):
    return get_job_details(job_id)
