import os
import subprocess
import tempfile

from flask import Flask
from flask import request
from flask.helpers import make_response
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class UnoconvConverter(object):

    def convert(self, file, input_format, output_format):
        temp_path = tempfile.NamedTemporaryFile(suffix=".%s" % (input_format, ))
        temp_path.write(file)
        temp_path.flush()

        unoconv_bin = 'unoconv'
        command = [unoconv_bin, '--stdout', '-e', 'UseLosslessCompression=false', '-e', 'ReduceImageResolution=false', '--format', output_format, temp_path.name]
        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data, stderrdata = p.communicate()

        if stderrdata:
            raise Exception(str(stderrdata))

        temp_path.close()

        return data


class UnoconvResource(Resource):

    def post(self, output_format):
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1][1:]
        converter = UnoconvConverter()

        raw_bytes = converter.convert(file.read(), extension, output_format)
        response = make_response(raw_bytes)
        response.headers['Content-Type'] = "application/octet-stream"
        response.headers['Content-Disposition'] = "inline; filename=converted.%s" % (output_format, )
        return response

api.add_resource(UnoconvResource, '/unoconv/<string:output_format>/')

