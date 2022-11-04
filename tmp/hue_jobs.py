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


def list_jobs_jobs(host: str, user: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/jobbrowser/api/jobs/jobs"
    payload = {'interface': '"jobs"',
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


def get_job_wf(host: str, app_id: str, cookie: str) -> dict:
    result = {}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }

    url = "http://" + host + ":8000/jobbrowser/api/job/workflows"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'pagination': '{"page":1,"offset":1,"limit":50}'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['app'] = dic.pop('app')

    url = "http://" + host + ":8000/jobbrowser/api/job/logs?is_embeddable=true"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'type': '"workflow"',
               'name': '"default"'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['logs'] = dic.pop('logs')

    url = "http://" + host + ":8000/jobbrowser/api/job/profile"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'app_type': '"workflow"',
               'app_property': '"properties"',
               'app_filters': '[{"text":""},{"states":[]},{"types":[]}]'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['properties'] = dic.pop('properties')

    url = "http://" + host + ":8000/jobbrowser/api/job/profile"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"workflows"',
               'app_type': '"workflow"',
               'app_property': '"xml"',
               'app_filters': '[{"text":""},{"states":[]},{"types":[]}]'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['xml'] = dic.pop('xml')

    return result


def get_job_job(host: str, app_id: str, cookie: str) -> dict:
    result = {}
    headers = {
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }

    url = "http://" + host + ":8000/jobbrowser/api/job/logs?is_embeddable=true"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"jobs"',
               'type': '"YarnV2"',
               'name': '"stdout"'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['stdout'] = dic.pop('logs')

    url = "http://" + host + ":8000/jobbrowser/api/job/logs?is_embeddable=true"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"jobs"',
               'type': '"YarnV2"',
               'name': '"stderr"'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['stderr'] = dic.pop('logs')

    url = "http://" + host + ":8000/jobbrowser/api/job/logs?is_embeddable=true"
    payload = {'app_id': '"{}"'.format(app_id),
               'interface': '"jobs"',
               'type': '"YarnV2"',
               'name': '"syslog"'}
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    if dic['status'] == 0:
        result['syslog'] = dic.pop('logs')

    return result


def main():
    if len(sys.argv) < 4:
        print('Usage: {} submit host wf_id          # submit a workflow'.format(sys.argv[0]))
        print('       {} get_workflow host app_id   # get workflow log'.format(sys.argv[0]))
        print('       {} get_job host app_id        # get job log'.format(sys.argv[0]))
        print('       {} list_workflows host user   # list workflow logs'.format(sys.argv[0]))
        print('       {} list_jobs host user        # list job logs'.format(sys.argv[0]))
        sys.exit(1)

    with open('hue_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]

    if sys.argv[1] == 'submit':
        assert sys.argv[3].isnumeric()
        dic = submit_wf(sys.argv[2], sys.argv[3], cookie)
    elif sys.argv[1] == 'get_workflow':
        assert '-' in sys.argv[3]
        dic = get_job_wf(sys.argv[2], sys.argv[3], cookie)
    elif sys.argv[1] == 'get_job':
        assert sys.argv[3].startswith('application_')
        dic = get_job_job(sys.argv[2], sys.argv[3], cookie)
    elif sys.argv[1] == 'list_workflows':
        dic = list_jobs_workflows(sys.argv[2], sys.argv[3], cookie)
    elif sys.argv[1] == 'list_jobs':
        dic = list_jobs_jobs(sys.argv[2], sys.argv[3], cookie)
    else:
        assert False

    pprint(dic)


if __name__ == "__main__":
    main()
