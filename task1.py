from flask import Flask, jsonify, request
from tinydb import TinyDB, Query, where
import json
import re

app = Flask(__name__)


db = TinyDB('db.json')
@app.route('/get_form', methods=['POST', 'GET'])
def check_db():
    
    if request.method == 'POST':

        data = dict(request.form)
        d = {}
        m = 0
        FIELD_TYPE = 'text'
        if data:
            for k in data:
                if db.search(Query()[k].exists()):
                    m += 1
                    el = db.search(where(k) == str(data[k][0]))
                    for i in el:
                        form_num = i.eid
                        if str(form_num) in d:
                            d[str(form_num)] += 1
                        else:
                            d[str(form_num)] = 1

                else:
                    print('No field %s in db' % (k))
                    break
            if len(data) == m:
                cur_max = 0
                winner = 'None'
                if d:
                    for k in d:
                        if d[k] > cur_max:
                            winner = 'Form ' + k
                            cur_max = d[k]
                res = {'Form': winner, 'Matches': cur_max}
                return json.dumps(res)

            n = {}
            for k in data:
                FIELD_TYPE = find_field(str(data[k][0]))
                n[k] = FIELD_TYPE
            return json.dumps(n)


        else:
            return 'Empty request'
    return 'Not a POST request'


def find_field(f_value):

    phone = re.compile('\d+-\(\d+\)\d{3}-\d{4}')
    email = re.compile('([a-z0-9][-a-z0-9_\+\.]*[a-z0-9])@([a-z0-9][-a-z0-9\.]*[a-z0-9]\.(arpa|root|aero|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)|([0-9]{1,3}\.{3}[0-9]{1,3}))')
    date = re.compile('\d{2}\/\d{2}\/\d{4}')
    text = re.compile('.+')

    d = {'date': date, 'phone': phone, 'email': email, 'text': text}

    for k in d:
        if d[k].match(f_value):
            return k
    return 'unknown_type'