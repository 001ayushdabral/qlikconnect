import websocket
import sensecalls
import json
import ssl


class SenseConnect:
    #initialising the constructor
    def __init__(self, domain='localhost', port='4848', userdirectory='', userid='', conntype='cert'):
        self.ws = self.create_connection(domain, port, userdirectory, userid, conntype)
        self.qlikcall = sensecalls.SenseCalls()

    def create_connection(self, domain, port, userdirectory, userid, conntype):
        print('Connection initiated!')
        if domain=='localhost':
            try:
                conn = websocket.create_connection("ws://localhost:4848/app")
                print('Succesfully connected to local qliksense desktop app.')
                return conn
            except :
                print('Error : Failed to connect with Qliksense app.\nMake sure you have opened your local qliksense desktop app.')
                return 'Make sure you have opened your local qliksense desktop app before running this.'
        else:
            qlik_server_url = f"wss://{domain}:{port}/app"
            certs = ({"ca_certs":'root.pem',
                      "certfile": 'client.pem',
                      "keyfile": 'client_key.pem',
                      "cert_reqs": ssl.CERT_REQUIRED,
                      "server_side": False})
            ssl.match_hostname = lambda cert, hostname: True
            return websocket.create_connection(qlik_server_url, 
                                            sslopt=certs,
                                            header={f"'X-Qlik-User':  'UserDirectory={userdirectory}; UserId={userid}'"})


    def close_connection(self):
        self.ws.close()
    
    # return the handle 
    def get_handle(self):
        result = json.loads(self.ws.recv())
        if 'method' in result.keys():
            result = json.loads(self.ws.recv())
        return result['result']['qReturn']['qHandle']
        
    
    # This will give the list of all the apps in workspace
    def get_list_of_apps(self):
        app_list = []
        self.ws.send(self.qlikcall.get_doc_list())
        result = json.loads(self.ws.recv())
        if 'method' in result.keys():
            # result = self.ws.recv()
            result = json.loads(self.ws.recv())
        for doclist in result['result']['qDocList']:
            app_list.append(doclist['qTitle'])           
        return app_list
    
    # This will give the last updated/reloaded date&time of an app
    def get_last_updated_status(self, appname):
        reload_status = []
        request = self.qlikcall.get_doc_list()
        self.ws.send(request)
        result = json.loads(self.ws.recv())
        if 'method' in result.keys():
            result = json.loads(self.ws.recv())
        for doclist in result['result']['qDocList']:
            if 'qLastReloadTime' in doclist.keys() and doclist['qTitle'].lower() in appname.lower():
                reload_status.append(doclist['qTitle'])
                reload_status.append(doclist['qLastReloadTime'])
                break
        # print(reload_status,len(reload_status))
        if len(reload_status)>0:
            return reload_status
        else:
            return print('App not found!\n[Localhost] : Make sure spelling of app is correct.\n[Enterprise] : Make sure App ID is correct.')
    
    # evaluate the expression and return the output of set analysis(expression)
    def evaluate_expression(self,appname,expression,e_o_dim):
        self.ws.send(self.qlikcall.open_doc(appname))
        #self.ws.recv()
        self.ws.send(self.qlikcall.evaluate_expr(expression, self.get_handle()))
        result = json.loads(self.ws.recv())
        resp = result['result']['qValue']['qText']
        if e_o_dim==0:
            # self.ws.close()
            pass
        return resp

    #return all the fields name and related data in a list
    def get_all_fields(self, appname):
        self.ws.send(self.qlikcall.open_doc(appname))
        self.ws.send(self.qlikcall.create_session(self.get_params('field'), self.get_handle()))
        request = self.qlikcall.get_layout(self.get_handle())
        self.ws.send(request)
        res = json.loads(self.ws.recv())
        #self.ws.close()
        return res['result']['qLayout']['qFieldList']['qItems']

    # it will return the parameter to create the session
    def get_params(self, requirement, fieldname=False):
        if requirement=='fieldvalues':
            params = [
                {
                    "qInfo": {
                    "qId": "ListObject01",
                    "qType": "ListObject"
                    },
                    "qListObjectDef": {
                    "qStateName": "$",
                    "qLibraryId": "",
                    "qDef": {
                        "qFieldDefs": [
                        fieldname
                        ],
                        "qFieldLabels": [
                            fieldname
                        ],
                        "qSortCriterias": [
                            {
                                "qSortByLoadOrder": 1
                            }
                        ]
                    },
                        "qInitialDataFetch": [
                            {
                                "qTop": 0,
                                "qHeight": 1,
                                "qLeft": 0,
                                "qWidth": 1
                            }
                        ]
                    }
                }
            ]
        elif requirement=='master_measures':
            params = [
                {
                    "qInfo": {
                        "qType": "MeasureList"
                    },
                    "qMeasureListDef": {
                        "qType": "measure",
                        "qData": {
                            "title": "/qMetaDef/title",
                            "description": "/qMetaDef/description",
                            "expression": "/qMeasure/qDef"
                        }
                    }
                }
            ]
        elif requirement=='exportdata':
            params = [
                {
                    "qInfo": {
                        "qType": "SheetList"
                    },
                    "qAppObjectListDef": {
                        "qType": "sheet",
                        "qData": {
                            "title": "/qMetaDef/title",
                            "description": "/qMetaDef/description",
                            "thumbnail": "/thumbnail",
                            "cells": "/cells",
                            "rank": "/rank",
                            "columns": "/columns",
                            "rows": "/rows"
                        }
                    }
                }
            ]
        else:
            params = [
                {
                    "qInfo": {
                        "qType": "FieldList"
                    },
                    "qFieldListDef": {
                        "qShowSystem": False,
                        "qShowHidden": False,
                        "qShowDerivedFields": True,
                        "qShowSemantic": True,
                        "qShowSrcTables": True,
                        "qShowImplicit": True
                    }
                }
            ]
        return params

    # returs the json of all the values in a field
    def get_all_field_values(self, appname, fieldname):
        filedvalues = []
        # request = self.qlikcall.open_doc(appname)
        self.ws.send(self.qlikcall.open_doc(appname))
        self.ws.send(self.qlikcall.create_session(self.get_params('fieldvalues', fieldname), self.get_handle()))
        self.ws.send(self.qlikcall.Select_list_object_values(self.get_handle()))
        # print('pehla result : ',self.ws.recv())
        self.ws.recv()
        # print('okieeeeeeeeeeeeeeeeeeeeeeeeee, ',fieldname)
        request = self.qlikcall.get_list_object_data()
        self.ws.send(request)
        # res = self.ws.recv()
        result = json.loads(self.ws.recv())
        print(result)
        for qMatrix in result['result']['qDataPages'][0]['qMatrix']:
            filedvalues.append(qMatrix[0]['qText'])
        return filedvalues

    # returns the master_measure expressions
    def get_master_measures(self, appname, only_mastermeasure_name=False):
        mastermeasure_info = []
        self.ws.send(self.qlikcall.open_doc(appname))
        self.ws.send(self.qlikcall.create_session(self.get_params('master_measures'), self.get_handle()))
        self.ws.send(self.qlikcall.get_layout(self.get_handle()))
        res = json.loads(self.ws.recv())
        if only_mastermeasure_name:
            for qItem in res['result']['qLayout']['qMeasureList']['qItems']:
                mastermeasure_info.append(qItem['qData']['title'])
        else:
            for qItem in res['result']['qLayout']['qMeasureList']['qItems']:
                mastermeasure_info.append((qItem['qData']['title'],qItem['qData']['description'],qItem['qData']['expression']))
        return mastermeasure_info

    def export_to_excel(self, appname):
        export_info = []
        self.ws.send(self.qlikcall.open_doc(appname))
        self.ws.send(self.qlikcall.create_session(self.get_params('exportdata'), self.get_handle()))
        qhandle_obj = self.get_handle()
        self.ws.send(self.qlikcall.get_layout(qhandle_obj))
        result = json.loads(self.ws.recv())
        # qhandle = result['result']['qReturn']['qHandle']  
        for sheet in result['result']['qLayout']['qAppObjectList']['qItems']:
            for chart in sheet['qData']['cells']:
                self.ws.send(self.qlikcall.get_object(1,chart['name']))
                result = json.loads(self.ws.recv())
                if result['result']['qReturn']['qGenericType'] not in ['VizlibFilter','tcmenu','filterpane','kpi']:
                    chart_type = result['result']['qReturn']['qGenericType']
                    qhandle_export = result['result']['qReturn']['qHandle']
                    self.ws.send(self.qlikcall.get_layout(qhandle_export))
                    result = json.loads(self.ws.recv())
                    chart_name = result['result']['qLayout']['title']
                    print('chart name :',chart_name)
                    print('qhandle :',qhandle_export)
                    self.ws.send(self.qlikcall.export_data(qhandle_export,chart_name))
                    result = json.loads(self.ws.recv())
                    chart_url="http://localhost:4848" + result["result"]["qUrl"]
                    export_info.append((chart_name, chart_url, chart_type))
        return export_info

