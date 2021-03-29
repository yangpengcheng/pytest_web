import jenkins


class Jenkins(jenkins.Jenkins):
    def __init__(self, url, username, password):
        super(Jenkins, self).__init__(url=url, username=username, password=password)

    def create_job(self, name, config_xml=jenkins.EMPTY_CONFIG_XML):
        super(Jenkins, self).create_job(name, config_xml)

