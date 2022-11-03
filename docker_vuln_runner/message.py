import json


class VulnMessage:
    def __init__(self, token, msg, data=None):
        self.token = token
        self.msg = msg
        self.data = data

    def parse_json(json_data):
        obj = json.loads(json_data)
        if 'data' in obj.keys():
            return VulnMessage(obj['token'], obj['msg'], obj['data'])
        else:
            return VulnMessage(obj['token'], obj['msg'])

    def is_hello(self):
        return self.msg == 'hello'

    def is_run(self):
        return self.msg == 'run'

    def is_down(self):
        return self.msg == 'down'

    def msg(self):
        return json.dumps(self.__dict__)