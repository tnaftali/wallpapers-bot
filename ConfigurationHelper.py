import ConfigParser


class ConfigurationHelper:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")

    def config_section_map(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
