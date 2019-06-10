import collections
import json
from datetime import datetime
from decimal import Decimal




class JsonEncoder(json.JSONEncoder):
    def default(self, o):

        if isinstance(o,Decimal):
            return float([o][0])
        if isinstance(o, collections.Iterable):
            return list(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')

        return json.JSONEncoder.default(self, o)


