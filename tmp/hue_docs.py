#! /usr/bin/python3
import json
import re
import sys
import time
from pprint import pprint
from uuid import uuid4

from requests import request


def listdir_from_hue(host: str, cookie: str, path: str = None) -> list:
    url = "http://" + host + ":8000/filebrowser/listdir2/"
    if path:
        url += "?path=" + path
    headers = {
        'cookie': cookie
    }
    response = request("GET", url, headers=headers)
    dic = json.loads(response.text)
    return dic["data"] if dic["status"] == 0 else []


def list_documents(host: str, cookie: str) -> list:
    url = "http://" + host + ":8000/desktop/api2/xo_docs/"
    headers = {'Cookie': cookie}
    response = request("GET", url, headers=headers)
    assert response.status_code == 200
    dic = json.loads(response.text)
    return dic['documents'] if dic["status"] == 0 else []


def create_empty_document(name: str) -> dict:
    document = {
        "workflow": {
            "id": None,
            "uuid": "b6c038cc-1c07-9e24-f9b5-6e5371534bcc",
            "name": "empty2",
            "isDirty": True,
            "properties": {
                "parameters": [
                    {
                        "name": "oozie.use.system.libpath",
                        "value": True
                    }
                ],
                "deployment_dir": "/user/hue/oozie/workspaces/hue-oozie-1665451673.597297",
                "properties": [],
                "show_arrows": True,
                "schema_version": "uri:oozie:workflow:0.5",
                "job_xml": "",
                "sla_enabled": False,
                "sla": [
                    {
                        "key": "enabled",
                        "value": False
                    },
                    {
                        "key": "nominal-time",
                        "value": "${nominal_time}"
                    },
                    {
                        "key": "should-start",
                        "value": ""
                    },
                    {
                        "key": "should-end",
                        "value": "${30 * MINUTES}"
                    },
                    {
                        "key": "max-duration",
                        "value": ""
                    },
                    {
                        "key": "alert-events",
                        "value": ""
                    },
                    {
                        "key": "alert-contact",
                        "value": ""
                    },
                    {
                        "key": "notification-msg",
                        "value": ""
                    },
                    {
                        "key": "upstream-apps",
                        "value": ""
                    }
                ],
                "wf1_id": None,
                "description": ""
            },
            "nodes": [
                {
                    "id": "3f107997-04cc-8733-60a9-a4bb62cebffc",
                    "name": "Start",
                    "type": "start-widget",
                    "properties": {},
                    "children": [
                        {
                            "to": "33430f0f-ebfa-c3ec-f237-3e77efa03d0a"
                        }
                    ],
                    "associatedDocumentLoading": True,
                    "associatedDocumentUuid": None,
                    "actionParameters": [],
                    "actionParametersFetched": False
                },
                {
                    "id": "33430f0f-ebfa-c3ec-f237-3e77efa03d0a",
                    "name": "End",
                    "type": "end-widget",
                    "properties": {
                        "enableMail": False,
                        "to": "",
                        "cc": "",
                        "subject": "",
                        "body": "",
                        "content_type": "text/plain",
                        "attachment": ""
                    },
                    "children": [],
                    "associatedDocumentLoading": True,
                    "associatedDocumentUuid": None,
                    "actionParameters": [],
                    "actionParametersFetched": False
                },
                {
                    "id": "17c9c895-5a16-7443-bb81-f34b30b21548",
                    "name": "Kill",
                    "type": "kill-widget",
                    "properties": {
                        "message": "Action failed, error message[${wf:errorMessage(wf:lastErrorNode())}]",
                        "enableMail": False,
                        "to": "",
                        "cc": "",
                        "subject": "",
                        "body": ""
                    },
                    "children": [],
                    "associatedDocumentLoading": True,
                    "associatedDocumentUuid": None,
                    "actionParameters": [],
                    "actionParametersFetched": False
                }
            ],
            "versions": [
                "uri:oozie:workflow:0.4",
                "uri:oozie:workflow:0.4.5",
                "uri:oozie:workflow:0.5"
            ],
            "movedNode": None,
            "nodeIds": [
                "3f107997-04cc-8733-60a9-a4bb62cebffc",
                "33430f0f-ebfa-c3ec-f237-3e77efa03d0a",
                "17c9c895-5a16-7443-bb81-f34b30b21548"
            ],
            "nodeNamesMapping": {
                "3f107997-04cc-8733-60a9-a4bb62cebffc": "Start",
                "33430f0f-ebfa-c3ec-f237-3e77efa03d0a": "End",
                "17c9c895-5a16-7443-bb81-f34b30b21548": "Kill"
            },
            "linkMapping": {
                "3f107997-04cc-8733-60a9-a4bb62cebffc": [
                    "33430f0f-ebfa-c3ec-f237-3e77efa03d0a"
                ],
                "33430f0f-ebfa-c3ec-f237-3e77efa03d0a": [],
                "17c9c895-5a16-7443-bb81-f34b30b21548": []
            },
            "hasKillNode": True
        },
        "layout": [
            {
                "id": "1c082fb1-4df6-b50d-3269-3151272a52be",
                "size": 12,
                "rows": [
                    {
                        "id": "aa6414f7-3a28-6e5f-8f53-ae593fc493d8",
                        "widgets": [
                            {
                                "size": 12,
                                "gridsterHeight": 0,
                                "name": "Start",
                                "id": "3f107997-04cc-8733-60a9-a4bb62cebffc",
                                "widgetType": "start-widget",
                                "properties": {},
                                "offset": 0,
                                "isLoading": False,
                                "isEditing": False,
                                "klass": "card card-widget span12",
                                "oozieMovable": False,
                                "oozieExpanded": False,
                                "ooziePropertiesExpanded": False,
                                "status": "",
                                "progress": 0,
                                "actionURL": "",
                                "logsURL": "",
                                "externalId": "",
                                "externalJobId": "",
                                "externalIdUrl": ""
                            }
                        ],
                        "columns": [],
                        "enableOozieDrop": False,
                        "enableOozieDropOnBefore": True,
                        "enableOozieDropOnSide": True
                    },
                    {
                        "id": "b3fdbd04-0c07-2b18-f271-35f293260131",
                        "widgets": [
                            {
                                "size": 12,
                                "gridsterHeight": 0,
                                "name": "End",
                                "id": "33430f0f-ebfa-c3ec-f237-3e77efa03d0a",
                                "widgetType": "end-widget",
                                "properties": {},
                                "offset": 0,
                                "isLoading": False,
                                "isEditing": False,
                                "klass": "card card-widget span12",
                                "oozieMovable": False,
                                "oozieExpanded": False,
                                "ooziePropertiesExpanded": False,
                                "status": "",
                                "progress": 0,
                                "actionURL": "",
                                "logsURL": "",
                                "externalId": "",
                                "externalJobId": "",
                                "externalIdUrl": ""
                            }
                        ],
                        "columns": [],
                        "enableOozieDrop": False,
                        "enableOozieDropOnBefore": True,
                        "enableOozieDropOnSide": True
                    },
                    {
                        "id": "eeb51c81-de31-7c07-773e-1f7e9b2227ff",
                        "widgets": [
                            {
                                "size": 12,
                                "gridsterHeight": 0,
                                "name": "Kill",
                                "id": "17c9c895-5a16-7443-bb81-f34b30b21548",
                                "widgetType": "kill-widget",
                                "properties": {},
                                "offset": 0,
                                "isLoading": False,
                                "isEditing": False,
                                "klass": "card card-widget span12",
                                "oozieMovable": True,
                                "oozieExpanded": False,
                                "ooziePropertiesExpanded": False,
                                "status": "",
                                "progress": 0,
                                "actionURL": "",
                                "logsURL": "",
                                "externalId": "",
                                "externalJobId": "",
                                "externalIdUrl": ""
                            }
                        ],
                        "columns": [],
                        "enableOozieDrop": False,
                        "enableOozieDropOnBefore": True,
                        "enableOozieDropOnSide": True
                    }
                ],
                "drops": [
                    "temp"
                ],
                "klass": "card card-home card-column span12",
                "oozieStartRow": {
                    "id": "aa6414f7-3a28-6e5f-8f53-ae593fc493d8",
                    "widgets": [
                        {
                            "size": 12,
                            "gridsterHeight": 0,
                            "name": "Start",
                            "id": "3f107997-04cc-8733-60a9-a4bb62cebffc",
                            "widgetType": "start-widget",
                            "properties": {},
                            "offset": 0,
                            "isLoading": False,
                            "isEditing": False,
                            "klass": "card card-widget span12",
                            "oozieMovable": False,
                            "oozieExpanded": False,
                            "ooziePropertiesExpanded": False,
                            "status": "",
                            "progress": 0,
                            "actionURL": "",
                            "logsURL": "",
                            "externalId": "",
                            "externalJobId": "",
                            "externalIdUrl": ""
                        }
                    ],
                    "columns": [],
                    "enableOozieDrop": False,
                    "enableOozieDropOnBefore": True,
                    "enableOozieDropOnSide": True
                },
                "oozieEndRow": {
                    "id": "b3fdbd04-0c07-2b18-f271-35f293260131",
                    "widgets": [
                        {
                            "size": 12,
                            "gridsterHeight": 0,
                            "name": "End",
                            "id": "33430f0f-ebfa-c3ec-f237-3e77efa03d0a",
                            "widgetType": "end-widget",
                            "properties": {},
                            "offset": 0,
                            "isLoading": False,
                            "isEditing": False,
                            "klass": "card card-widget span12",
                            "oozieMovable": False,
                            "oozieExpanded": False,
                            "ooziePropertiesExpanded": False,
                            "status": "",
                            "progress": 0,
                            "actionURL": "",
                            "logsURL": "",
                            "externalId": "",
                            "externalJobId": "",
                            "externalIdUrl": ""
                        }
                    ],
                    "columns": [],
                    "enableOozieDrop": False,
                    "enableOozieDropOnBefore": True,
                    "enableOozieDropOnSide": True
                },
                "oozieKillRow": {
                    "id": "eeb51c81-de31-7c07-773e-1f7e9b2227ff",
                    "widgets": [
                        {
                            "size": 12,
                            "gridsterHeight": 0,
                            "name": "Kill",
                            "id": "17c9c895-5a16-7443-bb81-f34b30b21548",
                            "widgetType": "kill-widget",
                            "properties": {},
                            "offset": 0,
                            "isLoading": False,
                            "isEditing": False,
                            "klass": "card card-widget span12",
                            "oozieMovable": True,
                            "oozieExpanded": False,
                            "ooziePropertiesExpanded": False,
                            "status": "",
                            "progress": 0,
                            "actionURL": "",
                            "logsURL": "",
                            "externalId": "",
                            "externalJobId": "",
                            "externalIdUrl": ""
                        }
                    ],
                    "columns": [],
                    "enableOozieDrop": False,
                    "enableOozieDropOnBefore": True,
                    "enableOozieDropOnSide": True
                },
                "oozieRows": [],
                "enableOozieDropOnBefore": True,
                "enableOozieDropOnAfter": True
            }
        ]
    }

    workflow = document["workflow"]
    workflow["name"] = name
    workflow["uuid"] = str(uuid4())
    workflow["properties"]["deployment_dir"] = "/user/hue/oozie/workspaces/" + str(time.time())

    return document


def add_shell_node(command: str, files: list, document: dict):
    workflow = document["workflow"]
    start_node, end_node, kill_node = workflow["nodes"]
    node_id = str(uuid4())
    node_name = "shell-" + node_id[: 4]
    node = {
        "id": node_id,
        "name": node_name,
        "type": "shell-widget",
        "properties": {
            "shell_command": command,
            "arguments": [],
            "env_var": [],
            "capture_output": True,
            "files": files,
            "archives": [],
            "job_properties": [],
            "prepares": [],
            "job_xml": "",
            "retry_max": [],
            "retry_interval": [],
            "sla": [
                {
                    "key": "enabled",
                    "value": False
                },
                {
                    "key": "nominal-time",
                    "value": "${nominal_time}"
                },
                {
                    "key": "should-start",
                    "value": ""
                },
                {
                    "key": "should-end",
                    "value": "${30 * MINUTES}"
                },
                {
                    "key": "max-duration",
                    "value": ""
                },
                {
                    "key": "alert-events",
                    "value": ""
                },
                {
                    "key": "alert-contact",
                    "value": ""
                },
                {
                    "key": "notification-msg",
                    "value": ""
                },
                {
                    "key": "upstream-apps",
                    "value": ""
                }
            ],
            "credentials": []
        },
        "children": [
            {
                "to": end_node["id"]
            },
            {
                "error": kill_node["id"]
            }
        ],
        "associatedDocumentLoading": True,
        "associatedDocumentUuid": None,
        "actionParameters": [],
        "actionParametersFetched": False
    }

    workflow["nodes"].append(node)
    start_node["children"][0]["to"] = node["id"]
    workflow["nodeIds"].append(node_id)
    workflow["nodeNamesMapping"][node_id] = node_name
    workflow["linkMapping"][start_node["id"]] = [node_id]
    workflow["linkMapping"][node_id] = [end_node["id"]]

    layout = document["layout"]
    row = {
        "id": "f71d9c0b-47c6-fc60-420c-1812b607e28a",
        "widgets": [
            {
                "size": 12,
                "gridsterHeight": 0,
                "name": "Shell",
                "id": node_id,
                "widgetType": "shell-widget",
                "properties": {},
                "offset": 0,
                "isLoading": False,
                "isEditing": False,
                "klass": "card card-widget span12",
                "oozieMovable": True,
                "oozieExpanded": False,
                "ooziePropertiesExpanded": False,
                "status": "",
                "progress": 0,
                "actionURL": "",
                "logsURL": "",
                "externalId": "",
                "externalJobId": "",
                "externalIdUrl": ""
            }
        ],
        "columns": [],
        "enableOozieDrop": False,
        "enableOozieDropOnBefore": True,
        "enableOozieDropOnSide": True
    }
    layout[0]["oozieRows"].append(row)
    layout[0]["rows"].append(row)


def add_sqoop_node(command: str, files: list, document: dict):
    workflow = document["workflow"]
    start_node, end_node, kill_node = workflow["nodes"]
    node_id = str(uuid4())
    node_name = "sqoop-" + node_id[: 4]
    node = {
        "id": node_id,
        "name": node_name,
        "type": "sqoop-widget",
        "properties": {
            "command": command,
            "arguments": [],
            # "env_var": [],
            # "capture_output": True,
            "files": files,
            "archives": [],
            "job_properties": [],
            "prepares": [],
            "job_xml": "",
            "retry_max": [],
            "retry_interval": [],
            "sla": [
                {
                    "key": "enabled",
                    "value": False
                },
                {
                    "key": "nominal-time",
                    "value": "${nominal_time}"
                },
                {
                    "key": "should-start",
                    "value": ""
                },
                {
                    "key": "should-end",
                    "value": "${30 * MINUTES}"
                },
                {
                    "key": "max-duration",
                    "value": ""
                },
                {
                    "key": "alert-events",
                    "value": ""
                },
                {
                    "key": "alert-contact",
                    "value": ""
                },
                {
                    "key": "notification-msg",
                    "value": ""
                },
                {
                    "key": "upstream-apps",
                    "value": ""
                }
            ],
            "credentials": []
        },
        "children": [
            {
                "to": end_node["id"]
            },
            {
                "error": kill_node["id"]
            }
        ],
        "associatedDocumentLoading": True,
        "associatedDocumentUuid": None,
        "actionParameters": [],
        "actionParametersFetched": False
    }

    workflow["nodes"].append(node)
    start_node["children"][0]["to"] = node["id"]
    workflow["nodeIds"].append(node_id)
    workflow["nodeNamesMapping"][node_id] = node_name
    workflow["linkMapping"][start_node["id"]] = [node_id]
    workflow["linkMapping"][node_id] = [end_node["id"]]

    layout = document["layout"]
    row = {
        "id": "f71d9c0b-47c6-fc60-420c-1812b607e28a",
        "widgets": [
            {
                "size": 12,
                "gridsterHeight": 0,
                "name": "Sqoop 1",
                "id": node_id,
                "widgetType": "sqoop-widget",
                "properties": {},
                "offset": 0,
                "isLoading": False,
                "isEditing": False,
                "klass": "card card-widget span12",
                "oozieMovable": True,
                "oozieExpanded": False,
                "ooziePropertiesExpanded": False,
                "status": "",
                "progress": 0,
                "actionURL": "",
                "logsURL": "",
                "externalId": "",
                "externalJobId": "",
                "externalIdUrl": ""
            }
        ],
        "columns": [],
        "enableOozieDrop": False,
        "enableOozieDropOnBefore": True,
        "enableOozieDropOnSide": True
    }
    layout[0]["oozieRows"].append(row)
    layout[0]["rows"].append(row)


def add_document(host: str, user: str, name: str, node_type: str, cookie: str) -> int:
    doc = create_empty_document(name)
    home_path = "/user/{}/".format(user)
    if node_type == 'shell':
        command = home_path + "oozie/apps/hue/hello_hue.sh"
        files = [command]
        add_shell_node(command, [{"value": x} for x in files], doc)
    elif node_type == 'sqoop':
        command = "import " \
                  "--connect jdbc:mysql://localhost:3306/manga " \
                  "--username manga " \
                  "--password manga " \
                  "--table fruit " \
                  "--target-dir " + home_path + "sqoop/fruit " \
                  "-m 1 " \
                  "--delete-target-dir"
        files = [home_path + "oozie/apps/sqoop_import/lib/mysql-connector-java-8.0.28.jar"]
        add_sqoop_node(command, [{"value": x} for x in files], doc)
    else:
        assert False, "node_type({}) is not supported".format(node_type)

    url = "http://" + host + ":8000/desktop/api2/xo_docs/"
    payload = json.dumps(doc)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    dic = json.loads(response.text)
    return dic["id"] if dic["status"] == 0 else -1


def get_document(host: str, cookie: str, wf_id: int) -> dict:
    url = "http://" + host + ":8000/desktop/api2/xo_doc/" + "?workflow=" + str(wf_id)
    headers = {'cookie': cookie}
    response = request("GET", url, headers=headers)
    assert response.status_code == 200
    dic = json.loads(response.text)
    return dic["data"] if dic["status"] == 0 else {}


def modify_document(host: str, cookie: str, wf_id: int) -> dict:
    doc = get_document(host, cookie, wf_id)
    doc['workflow']['id'] = wf_id
    doc['workflow']['properties']['description'] = 'from new world'
    url = "http://" + host + ":8000/desktop/api2/xo_doc/"
    payload = json.dumps(doc)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("PUT", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def main():
    if len(sys.argv) < 5:
        print('Usage: {} host user doc_name node_type'.format(sys.argv[0]))
        sys.exit(1)

    with open('hue_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]

    # pprint(listdir_from_hue(sys.argv[1], cookie))
    # pprint(listdir_from_hue(sys.argv[1], cookie, home_path + "/oozie/apps"))

    # workflow_id = add_document(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], cookie)
    # print(workflow_id)
    # pprint(get_document(sys.argv[1], cookie, workflow_id))

    # pprint(list_documents(sys.argv[1], cookie))
    # pprint(get_document(sys.argv[1], cookie, 213))
    pprint(modify_document(sys.argv[1], cookie, 213))


if __name__ == "__main__":
    main()
