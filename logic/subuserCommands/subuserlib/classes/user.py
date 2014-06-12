#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
#import ...
#internal imports
import subuserlib.classes.registry, subuserlib.classes.config, subuserlib.classes.repositories

class User(object):
  homeDir = None
  __config = None
  __registry = None
  __repositories = None
  
  def __init__(self,homeDir):
    self.homeDir = homeDir

  def getConfig(self):
    if self.__config == None:
      self.__config = subuserlib.classes.config.Config(self)
    return self.__config

  def getRegistry(self):
    if self.__registry == None:
      self.__registry = subuserlib.classes.registry.Registry(self)
    return self.__registry

  def getRepositories(self):
    if self.__repositories == None:
      self.__repositories = subuserlib.classes.repositories.Repositories(self)
    retunr self.__repositories