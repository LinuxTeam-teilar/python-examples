import urllib2
from os import path, mkdir, getcwd
from bs4 import BeautifulSoup

class xmlToConfigParser(object):
    #this is the xml which kde-projects provided


    def __init__(self, xml_source):
        #open the xml
        xml = urllib2.urlopen(xml_source)

        #create our soup!
        self.soup = BeautifulSoup(xml.read())


    """
    This method will create the directories for each
    component(I took the name from the xml) aka kde,
    playground, extragear and also it will create a config
    directory in the path

    :param destinationPath: the directory in which we will create our configs
    :type destinationPath: string
    """

    """
    This method will do the actual work.
    """
    def do(self):
        #first create the directories
        self._createDirectories(getcwd())

    """
    This method will create the directories that we want.
    We want one directory for each component
    """
    def _createDirectories(self, destinationPath):
        tmpPath = path.abspath(destinationPath)

        if not path.exists(tmpPath) and not path.isdir(tmpPath):
            print "errorrrrrrrrrrrrr!"
            return;
        else:
            configPath = tmpPath + '/config'
            if not path.exists(configPath):
                mkdir(configPath)

            #now lets create the directories for our components
            for component in self.soup.find_all("component"):
                #take the path
                componentPath = configPath + '/' + component["identifier"]

                if not path.exists(componentPath):
                    mkdir(componentPath)

XML_SOURCE = 'https://projects.kde.org/kde_projects.xml'
worker = xmlToConfigParser(XML_SOURCE)
worker.do()