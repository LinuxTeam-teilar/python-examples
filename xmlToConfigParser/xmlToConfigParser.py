#!/usr/bin/env python

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
        #xml = urllib2.urlopen(xml_source)
        #in case that wifi is down
        xml = open("/home/tsiapaliwkas/sources/github/python-examples/kde_projects.xml")

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
        self.releases = [
            "kde",
            "extragear",
            "playground",
            "kdesupport",
            "kdereview",
            "calligra"
        ]

        #now lets create the directories for our releases
        for i in self.releases:
            #take the path
            releasePath = self.configPath + i

            if not path.exists(releasePath):
                mkdir(releasePath)

        #now create the dirs for our projects and modules
        #I took the names project and module from the xml
        self._projectConfigFiles()
        self._moduleConfigFiles()


    #It will create any necessary directory file for each element in
    #the xml, which is name 'project'
    def _projectConfigFiles(self):
        for project in self.soup.find_all("project"):
            try:
                projectPath = project.path.string.split('/')

                for release in self.releases:
                    #include only the projects for which we want their data,
                    #those are the ones which live under the elements of self.releases
                    if projectPath[0] == release:
                        #the kde release is an exception
                        if projectPath[0] == 'kde':
                            configFilePath = self.configPath + projectPath[0] + '/' + projectPath[1] + '.cfg'
                            open(configFilePath, 'w')
                            self._writeIntoConfig(configFilePath, projectPath[2])
                        else:
                            if len(projectPath) == 4:
                                #extragear/network/
                                directory = self.configPath + projectPath[0] + '/' + projectPath[1] + '/'

                                #create the dir
                                if not path.exists(directory):
                                    mkdir(directory)

                                #extragear/network/telepathy.cfg
                                configFilePath = directory + projectPath[2] + '.cfg'
                                open(configFilePath, 'w')
                                self._writeIntoConfig(configFilePath, projectPath[3])
                            elif len(projectPath) == 3:
                                #playground/base/
                                dirPath = self.configPath + projectPath[0] + '/' + projectPath[1] + '/'
                                if not path.exists(dirPath):
                                    mkdir(dirPath)
                                configFilePath = dirPath + '/' + projectPath[2] + '.cfg'
                                open(configFilePath, 'w')
                                self._writeIntoConfig(configFilePath, projectPath[2])

            except AttributeError:
                #forget the error and go to the next item
                pass


    def _moduleConfigFiles(self):
        for module in self.soup.find_all("module"):
            try:
                modulePath = module.path.string.split('/')
                for release in self.releases:
                    if modulePath == release:
                        moduleDir = self.configPath + modulePath[0] + '/'
                        if not path.exists(moduleDir):
                            mkdir(moduleDir)

                        configFilePath = moduleDir + modulePath[1] + '.cfg'
                        open(configFilePath, 'w')
                        self._writeIntoConfig(configFilePath, modulePath[1])
            except AttributeError:
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