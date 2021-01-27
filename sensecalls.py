import json

class SenseCalls:
    def __init__(self):
        self.id = 1

    def inc_id(self):
        return self.id+1

    #to create a session for fieldlist
    def create_session(self, params, qhandle):
        request = {
            "method": "CreateSessionObject",
            "handle": qhandle,
            "params": params,
            "outKey": -1,
            "id": 3
        }
        return json.dumps(request)

    def get_layout(self, qhandle):
        request = {
            "method": "GetLayout",
            "handle": qhandle,
            "params": [],
            "outKey": -1,
            "id": 4
        }
        return json.dumps(request)

    #returns the JSON file like appname, lastreloadtime etc.
    def get_doc_list(self):
        request = {
            "handle": -1,
            "method": "GetDocList",
            "params": {},
            "outKey": -1,
            "id": 2}
        return json.dumps(request)
    
    #to open an app
    def open_doc(self, appname):
        request = {
            "handle": -1,
            "method": "OpenDoc",
            "params": [appname],
            "outKey": -1,
            "id": 1}
        return json.dumps(request)

    #to evaluate the expression
    def evaluate_expr(self, expression, qhandle):
        print('qlik call :',expression)
        request = {
            "handle": qhandle,
            "method": "EvaluateEx",
            "params": {
            "qExpression": expression
            },
            "outKey": -1,
            "id": 4}
        return json.dumps(request)
    
    # request to crerat a session for a particular field
    def create_fieldvalues_session(self, params, qhandle):
        request = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "CreateSessionObject",
            "handle": qhandle,
            "params": params
        }
        return json.dumps(request)

    # to initiate a field request
    def Select_list_object_values(self, qHandle):
        request = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "SelectListObjectValues",
            "handle": str(qHandle),
            "params": [
                "/qListObjectDef",
                [
                    0
                ],
                True
            ]
        }
        # jaja = json.loads(request)
        return json.dumps(request)

    # to get the the max of qHeight number of values 
    def get_list_object_data(self):
        request =  {
        "jsonrpc": "2.0",
        "id": self.inc_id(),
        "method": "GetListObjectData",
        "handle": 2,
        "params": [
            "/qListObjectDef",
            [
            {
                "qTop": 0,
                "qLeft": 0,
                "qWidth": 1,
                "qHeight": 20
            }
            ]
        ]
        }
        return json.dumps(request)

    # to get the chart object
    def get_object(self,qhandle,chart_objid):
        request = {
        "handle": qhandle,
        "method": "GetObject",
        "params": {
            "qId": chart_objid
        },
        "outKey": -1,
        "id": 6
        }
        return json.dumps(request)
    
    # to get the url of the exporting chart
    def export_data(self,qhandle,chartname):
        request = {
        "handle": qhandle,
        "method": "ExportData",
        "params": {
            "qFileType": "OOXML",
            "qPath": "",
            "qFileName": chartname,
            "qExportState": 0
        },
        "outKey": -1,
        "id": 7
        }
        return json.dumps(request)
        