import requests

class Api:
    @staticmethod
    def _make_request(method, url, req=None, headers=None):
        try:
            # Seleccionar el método HTTP dinámicamente
            res = requests.request(method, url, json=req, headers=headers)
            data = res.json()
            data['success'] = res.status_code == 200
        except requests.exceptions.RequestException as e:
            data = {'success': False, 'error': str(e)}
        return data

    @staticmethod
    def get(url, headers=None):
        return Api._make_request("GET", url, headers=headers)

    @staticmethod
    def post(url, req=None, headers=None):
        return Api._make_request("POST", url, req=req, headers=headers)

    @staticmethod
    def put(url, req=None, headers=None):
        return Api._make_request("PUT", url, req=req, headers=headers)

    @staticmethod
    def patch(url, req=None, headers=None):
        return Api._make_request("PATCH", url, req=req, headers=headers)

    @staticmethod
    def delete(url, headers=None):
        return Api._make_request("DELETE", url, headers=headers)
