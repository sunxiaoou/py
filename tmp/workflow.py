#! /usr/bin/python3
import json
import re
import sys
from pprint import pprint

from requests import request


def list_jobs_workflows(host: str, user: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/jobs/workflows"
    payload = {'interface': '"workflows"',
               'filters': '[{"text":"user:' + user + ' "},'
                          '{"time":{"time_value":7,"time_unit":"days"}},'
                          '{"states":[]},'
                          '{"pagination":{"page":1,"offset":1,"limit":100}}]'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def submit_wf(host: str, wf_id: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/oozie/editor/workflow/submit/" + wf_id
    payload = {'form-TOTAL_FORMS': '1',
               'form-INITIAL_FORMS': '1',
               'form-MIN_NUM_FORMS': '0',
               'form-MAX_NUM_FORMS': '1000',
               'form-0-name': 'oozie.use.system.libpath',
               'form-0-value': 'True',
               'format': 'json'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def check_job(host: str, app_id: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/job/workflows"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'pagination': '{"page":1,"offset":1,"limit":50}'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def get_log(host: str, app_id: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/job/logs?is_embeddable=true"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'type': '"workflow"',
               'name': '"default"'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def get_profile_properties(host: str, app_id: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/job/profile"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'app_type': '"workflow"',
               'app_property': '"properties"',
               'app_filters': '[{"text":""},{"states":[]},{"types":[]}]'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def get_profile_xml(host: str, app_id: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/job/profile"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'app_type': '"workflow"',
               'app_property': '"xml"',
               'app_filters': '[{"text":""},{"states":[]},{"types":[]}]'}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def main():
    if len(sys.argv) < 3:
        print('Usage: {} host wf_id|job_id'.format(sys.argv[0]))
        sys.exit(1)

    with open('hue_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]

    if sys.argv[2].isnumeric():
        dic = submit_wf(sys.argv[1], sys.argv[2], cookie)
    elif '-' in sys.argv[2]:
        # dic = check_job(sys.argv[1], sys.argv[2], cookie)
        # dic = get_log(sys.argv[1], sys.argv[2], cookie)
        # dic = get_profile_properties(sys.argv[1], sys.argv[2], cookie)
        dic = get_profile_xml(sys.argv[1], sys.argv[2], cookie)
    else:
        dic = list_jobs_workflows(sys.argv[1], sys.argv[2], cookie)
    pprint(dic)


if __name__ == "__main__":
    main()
