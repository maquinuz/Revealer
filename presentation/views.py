from flask import render_template, abort
from jinja2 import TemplateNotFound

from . import app

multiplexer = {}
multiplex_count = 0


@app.route('/<presentation_name>/<user_type>', methods=['GET'])
@app.route('/<presentation_name>/', defaults={'user_type': 'client'},
           methods=['GET'])
def landing(presentation_name, user_type):
    global multiplex_count, multiplexer
    try:
        if presentation_name in multiplexer:
            multiplex_id = multiplexer[presentation_name]
        else:
            multiplex_id = multiplex_count
            multiplexer[presentation_name] = multiplex_id
            multiplex_count += 1
        return render_template("%s.html" % presentation_name,
                               user_type=user_type,
                               mult_id=multiplex_id)
    except TemplateNotFound:
        abort(404)
