#! /usr/bin/python3
import json
import sys
import time
from pprint import pprint
from uuid import uuid4

from requests import request

# TOKEN = "nqf4mtafv03jmksonlm6rwghq18773lq"
URL_DOC = "http://localhost:8000/desktop/api2/xo_doc/"
URL_DOCS = "http://localhost:8000/desktop/api2/xo_docs/"
URL_FILE = "http://localhost:8000/filebrowser/listdir2/"
HOME_PATH = "/user/sun_xo/"
WORKSPACE = "/user/hue/oozie/workspaces/"


def listdir_from_hue(token: str, path: str = None) -> list:
    url = URL_FILE + "?path=" + path if path else URL_FILE
    payload = {}
    files = {}
    headers = {
        'x-csrftoken': token
    }
    response = request("GET", url, headers=headers, data=payload, files=files)
    dic = json.loads(response.text)
    return dic["data"] if dic["status"] == 0 else []


def get_empty_doc():
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


def prepare_document(name: str, node_type: str, command: str, files: list) -> dict:
    document = get_empty_doc()
    workflow = document["workflow"]
    workflow["name"] = name
    workflow["uuid"] = str(uuid4())
    workflow["properties"]["deployment_dir"] = WORKSPACE + str(time.time())
    if node_type == 'shell':
        add_shell_node(command, [{"value": x} for x in files], document)
    elif node_type == 'sqoop':
        add_sqoop_node(command, [{"value": x} for x in files], document)
    else:
        assert False, node_type + " is not supported"
    return document


def create_document_in_hue(token: str, document: dict) -> int:
    payload = json.dumps(document)
    headers = {
        'Content-Type': 'application/json',
        'x-csrftoken': token
    }
    response = request("POST", URL_DOCS, headers=headers, data=payload)
    dic = json.loads(response.text)
    return dic["id"] if dic["status"] == 0 else -1


def get_document_from_hue(token: str, wf_id: int) -> dict:
    url = URL_DOC + "?workflow=" + str(wf_id)
    payload = {}
    files = {}
    headers = {
        'x-csrftoken': token
    }
    response = request("GET", url, headers=headers, data=payload, files=files)
    dic = json.loads(response.text)
    return dic["data"] if dic["status"] == 0 else {}


def main():
    if len(sys.argv) < 3:
        print('Usage: {} token doc_name'.format(sys.argv[0]))
        sys.exit(1)

    # pprint(listdir_from_hue(sys.argv[1]))
    # pprint(listdir_from_hue(sys.argv[1], HOME_PATH + "/oozie/apps"))

    # command = HOME_PATH + "oozie/apps/hue/hello_hue.sh"
    # doc = prepare_document(sys.argv[2], "shell", command, [command])

    command = "import " \
              "--connect jdbc:mysql://localhost:3306/manga " \
              "--username manga " \
              "--password manga " \
              "--table fruit " \
              "--target-dir /user/sun_xo/sqoop/fruit " \
              "-m 1 " \
              "--delete-target-dir"
    file = "/user/sun_xo/oozie/apps/sqoop_import/lib/mysql-connector-java-8.0.28.jar"
    doc = prepare_document(sys.argv[2], "sqoop", command, [file])

    # pprint(doc)
    workflow_id = create_document_in_hue(sys.argv[1], doc)
    print(workflow_id)
    pprint(get_document_from_hue(sys.argv[1], workflow_id))


if __name__ == "__main__":
    main()
