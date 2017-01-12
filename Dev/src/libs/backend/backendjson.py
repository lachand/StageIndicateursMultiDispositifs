import json

from Dev.src.libs.backend import Backend, BackendItem


class BackendJSON(Backend):
    def load_items(self):
        filename = self.options.get('filename', None)
        with open(filename, 'r') as fd:
            data = json.loads(fd.read())
        self.keywords = data['keywords']
        assert (filename is not None)
        for item in data['items']:
            yield BackendItem(item)
