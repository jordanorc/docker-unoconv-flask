import os
import subprocess

from flask import Flask
from flask import request
from flask.helpers import make_response
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class UnoconvConverter(object):

    def convert(self, file, input_format, output_format):
        unoconv_bin = 'unoconv'
        command = [unoconv_bin, '--stdin', '--stdout', '-e', 'UseLosslessCompression=false', '-e', 'ReduceImageResolution=false', '--format', output_format]

        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(file)
        data, stderrdata = p.communicate()

        if stderrdata:
            raise Exception(stderrdata)

        return data


class UnoconvResource(Resource):

    def post(self, output_format):
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        converter = UnoconvConverter()

        raw_bytes = converter.convert(file.read(), extension, output_format)
        response = make_response(raw_bytes)
        response.headers['Content-Type'] = "application/octet-stream"
        response.headers['Content-Disposition'] = "inline; filename=converted.%s" % (output_format, )
        return response

api.add_resource(UnoconvResource, '/unoconv/<string:output_format>/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
