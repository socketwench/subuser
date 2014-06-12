#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
#import ...
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.dockerImages,subuserlib.dockerPs

class InstalledImage(subuserlib.classes.userOwnedObject.UserOwnedObject):
  __imageID = None
  __lastUpdateTime = None
  __programSource = None

  def __init__(self,user,imageID,lastUpdateTime,sourceName,sourceRepo):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self.__imageID = imageID
    self.__lastUpdateTime = lastUpdateTime
    self.__programSource = self.getUser().repositories.getRepositoryNamed(sourceRepo).getProgramSourceNamed(sourceName)

  def getImageID(self):
    return self.__imageID

  def getLastUpdateTime(self):
    return self.__lastUpdateTime

  def getProgramSource(self):
    return self.__programSource

  def isDockerImageThere(self):
    return not subuserlib.dockerImages.inspectImage(self.getImageId()) == None

  def areRunningContainersUsingThisImage(self):
    return subuserlib.dockerPs.isImageRunning(self.getImageId())

  def removeDockerImage(self):
    subuserlib.dockerImages.removeImage(self.getImageID())