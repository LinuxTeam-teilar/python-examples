import urllib2
from os import path, mkdir, getcwd
from bs4 import BeautifulSoup

class xmlToConfigParser(object):

    def __init__(self, xml_source, configDestinationPath):

        #now create the config path
        #this is the path in which we will store our configs
        tmpPath = path.abspath(configDestinationPath)

        if not path.exists(tmpPath) and not path.isdir(tmpPath):
            print "errorrrrrrrrrrrrr!"
            return;
        else:
            self.configPath = tmpPath + '/config/'
            if not path.exists(self.configPath):
                mkdir(self.configPath)

        #open the xml
        xml = urllib2.urlopen(xml_source)
        #in case that wifi is down
        #xml = open("/home/tsiapaliwkas/sources/github/python-examples/kde_projects.xml")

        #create our soup!
        self.soup = BeautifulSoup(xml.read())

    """
    This method will do the actual work.
    """
    def do(self):
        #first create the directories
        self._createComponentDirectories()

    """
    This method will create the directories for each
    release(I took the name from the xml) aka kde,
    playground, extragear
    """
    def _createComponentDirectories(self):
        #this is the releases that we want
        #to keep
        releases = [
            "kde",
            "extragear",
            "playground",
            "kdesupport",
            "kdereview",
            "calligra"
        ]

        #now lets create the directories for our releases
        for i in releases:
            #take the path
            releasePath = self.configPath + i

            if not path.exists(releasePath):
                mkdir(releasePath)

        #now create the dirs for our project
        #I took the name project from the xml
        self._projectConfigFiles()


    #It will create any necessary directory file for each element in
    #the xml, which is name 'project'
    def _projectConfigFiles(self):
        for project in self.soup.find_all("project"):
            try:
                projectPath = project.path.string.split('/')

                #make the dir like $foo/config/kde/kdegraphics/
                modulePath = self.configPath + projectPath[0] + '/' + projectPath[1] + '/'

                #check if the dir exists
                if not path.exists(modulePath):
                    mkdir(modulePath)

               # print 'modulePath'
               # print modulePath
               # print projectPath

                if len(projectPath) == 3:
                    #this is like,
                    #kde/kdegraphics/okular.cfg
                    configFilePath = modulePath + projectPath[2] + '.cfg'
                    open(configFilePath, 'w')
                    self._writeIntoConfig(configFilePath, projectPath[2])
                elif len(projectPath) == 4:
                    print 'projectPath'
                    print project.path.string
                    #this is like,
                    #extragear/network/telepathy/ktp-send-file
                    configFilePath = modulePath + projectPath[2] + '.cfg'
                    open(configFilePath, 'w')
                    self._writeIntoConfig(configFilePath, projectPath[3])

            except AttributeError:
                #forget the error and go to the next item
                pass

    """
    :param configFilePath: the path of the config filePath
    :type moduleName: the name of the module, like okular
    """
    def _writeIntoConfig(self, configFilePath, moduleName):
        pass


#this is the xml which kde-projects provided
XML_SOURCE = 'https://projects.kde.org/kde_projects.xml'

worker = xmlToConfigParser(XML_SOURCE, getcwd())
worker.do()