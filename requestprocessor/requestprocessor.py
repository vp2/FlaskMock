import imp
import json
from pprint import pformat

from jsonschema import exceptions
from jsonschema.validators import validator_for


class RequestProcessor:
    thread_pool = None

    def __init__(self, thread_pool=None):
        self.thread_pool = thread_pool

    def __load_class(self, path, filenames, importname):
        base_path = "." + path if path[0] == "/" else path

        for filename in filenames:
            try:
                required_class = imp.load_source(importname, base_path + "/" + filename)
                if required_class is not None:
                    print ("Class loaded: " + str(required_class))
                    return required_class
            except (ImportError, IOError) as ex:
                pass
        return None

    def __load_schema(self, base_path, method):
        schema = None
        for filename in ["schema_" + method.lower() + ".json", "schema.json"]:
            schema_name = base_path + "/" + filename
            try:
                with open(schema_name) as schema_file:
                    schema = json.load(schema_file)
                    schema_file.close()
                    print("Schema loaded: " + schema_name)
                    break
            except IOError:
                pass
        return schema

    def validate_schema(self, request_data, schema):
        data = json.loads(request_data)
        validator = validator_for(schema)(schema=schema)
        try:
            validator.check_schema(schema)
        except exceptions.SchemaError:
            return "Invalid schema definition."

        error_lines = []
        for error in validator.iter_errors(data):
            error_lines.append("Error: " + str(pformat(vars(error))))
        return None if len(error_lines) == 0 else "\n\n".join(error_lines)

    def process_request(self, req):
        path = str(req.url_rule)
        method = req.method
        data = req.data
        base_path = "." + path if path[0] == "/" else path

        schema = self.__load_schema(base_path, method)
        custom_validator = self.__load_class(base_path, ["validator_" + method.lower() + ".py", "validator.py"],
                                             "validator")
        custom_processor = self.__load_class(base_path, ["processor_" + method.lower() + ".py", "processor.py"],
                                             "processor")

        if schema is not None:
            info = self.validate_schema(data, schema)
            if info is not None:
                return {"result": "SCHEMA_ERROR", "info": info}

        if custom_validator is not None:
            info = custom_validator.Validator().validate(req)
            if info is not None:
                return {"result": "CUSTOM_VALIDATOR_ERROR", "info": info}

        if custom_processor is not None:
            return custom_processor.Processor(self.thread_pool).process(req)

        return {"result": "OK", "info": ""}
