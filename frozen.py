#!/usr/bin/env python3

import requests
import json
import datetime
import argparse
import sys

def incomplete(job_url):
    data = json.loads(requests.get(job_url + "/api/json").text)
    builds = data["builds"]
    for build in builds:
        build_url = build["url"]
        build_data = json.loads(requests.get(build_url + "/api/json").text)
        build_result = build_data["result"]
        if not build_result:
            yield build_data

def frozen(job_url, time_delta):
    for incomplete_job in incomplete(job_url):
        scheduled_at = incomplete_job["timestamp"]
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(scheduled_at/1000)
        if delta > time_delta:
            yield incomplete_job

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--job", metavar="URL", dest="url", required=True, action="store")
    args = arg_parser.parse_args(sys.argv[1:])

    treat_as_frozen_delta = datetime.timedelta(days=1)
    for frozen_jon in frozen(args.url, treat_as_frozen_delta):
        print (frozen_jon["url"])
