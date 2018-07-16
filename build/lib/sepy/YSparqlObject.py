#!/usr/bin/python3

import logging
import yaml

        
def ysparql_to_string(filepath,char_filter="#"):
    """
    Takes a path to file, returns a string containing the file without lines 
    starting with a specific character. Default is '#'
    """
    # Opening file and reading all lines.
    with open(filepath,"r") as myfile:
        lines = myfile.readlines()
    # Removing the lines beginning with the filter character.
    filtered = list(filter(lambda line: line[0]!=char_filter,lines))
    return "".join(filtered)

class YSparqlObject:
    def __init__(self,YSparqlFile,external_prefixes=""):
        self.logger = logging.getLogger("sepaLogger")
        logging.basicConfig(format='%(levelname)s:%(message)s')
        self._external_prefixes = external_prefixes
        self._content = ysparql_to_string(YSparqlFile)
        
    def getData(self,fB_values={}):
        """
        fB_values parameter can force values from the defaults in the yaml_file
        The couple SPARQL string, forced binding dictionary is given in return.
        """
        yaml_raw = yaml.load(self._content)
        yaml_obj = yaml.dump(yaml_raw)
        yaml_root = yaml_obj[:yaml_obj.index(":")]
        sparql = self._external_prefixes + yaml_raw[yaml_root]["sparql"]
        fB = yaml_raw[yaml_root]["forcedBindings"]
        # forcing bindings available in fB_values
        checkBindings(fB_values,fB)
        for binding in fB_values.keys():
            if binding in fB:
                fB[binding]["value"] = fB_values[binding]
        return sparql,fB

    @staticmethod
    def checkBindings(current,expected):
        pritnt("checkBindings")
        set_current = set(current.keys())
        set_expected = set(expected.keys())
        
        set_difference = set_expected - set_current
        if len(set_difference) != 0:
            for key in set_difference:
                if ((expected[key]["value"] != "UNDEF") and (expected[key]["value"] != "")):
                    raise KeyError(key+" is a required forcedbinding")
        return True
