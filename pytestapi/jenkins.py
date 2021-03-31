import jenkins

from pytestapi.util.xml import dict_to_xml_str, xml_str_to_dict

EMPTY_JSON = {
    "project": {
        "children": [
            {"keepDependencies": {"text": "false"}},
            {"properties": {}},
            {"scm": {"attrib": {"class": "jenkins.scm.NullSCM"}}},
            {"canRoam": {"text": "true"}},
            {"disabled": {"text": "false"}},
            {"blockBuildWhenUpstreamBuilding": {"text": "false"}},
            {"triggers": {"attrib": {"class": "vector"}}},
            {"concurrentBuild": {"text": "false"}},
            {"builders": {}},
            {"publishers": {}},
            {"buildWrappers": {}}
        ]
    }
}


class Jenkins(jenkins.Jenkins):
    def __init__(self, url, username, password):
        super(Jenkins, self).__init__(url=url, username=username, password=password)

    def create_job_by_xml(self, name, config_xml=jenkins.EMPTY_CONFIG_XML):
        super(Jenkins, self).create_job(name, config_xml)

    def create_job_by_dict(self, name, kwargs=None):
        if kwargs is None:
            kwargs = EMPTY_JSON
        super(Jenkins, self).create_job(name, dict_to_xml_str(kwargs))

    def get_job_config_dict(self, name):
        return xml_str_to_dict(super(Jenkins, self).get_job_config(name))


