#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
#import ...
#internal imports
import subuserlib.classes.installedImage,subuserlib.classes.fileBacked, subuserlib.classes.userOwnedObject

class InstalledImages(subuserlib.classes.userOwnedObject.UserOwnedObject,subuserlib.classes.fileBackedObject.FileBackedObject):
  __installedImagesDict = {}
  __installedImages = None

  def reloadInstalledImagesRegistry(self):
    """ Reload the installed images list from disk, discarding the current in-memory version. """
    installedImagesDict = {}
    installedImagesPath = self.getUser().config.getInstalledImagesDotJsonPath()
    if os.path.exists(installedImagesPath):
      with open(installedImagesPath, 'r') as file_f:
        programRegistry = json.load(file_f, object_pairs_hook=collections.OrderedDict)
    self.__installedImages = None
    self.__installedImagesDict = installedImagesDict

  def save(self):
    """ Save attributes of the installed images to disk. """
    installedImagesPath = self.getUser().config.getInstalledImagesDotJsonPath()
    with open(installedImagesPath, 'w') as file_f:
      json.dump(self.__installedImagesDict, file_f, indent=1, separators=(',', ': '))

  def __init__(self,user):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self.reloadInstalledImagesRegistry()

  def getInstalledImages(self):
    if not self.__installedImages == None:
      return self.__installedImages

    for imageID,imageAttributes in self.__installedImagesDict.iteritems():
      self.__installedImages.append(subuserlib.classes.installedImage.InstalledImage(imageID=imageID,lastUpdateTime=imageAttributes["last-update-time"],sourceName=imageAttributes["source-name"],sourceRepo=imageAttributes["source-repo"]))
    return self.__installedImages

  def registerImage(self,image):
    # set the images attributes in the __installedImagesDict
    sourceProgram = image.getSourceProgram()
    self.__installedImagesDict[image.getImageID()]={"source-name":sourceProgram.getName(),"source-repo"=sourceProgram.getRepository().getName(),"last-update-time"=image.getLastUpdateTime()}

    # update or add an entry to the __installedImages list
    self.__installedImages = [image if image_.getImageID() == image.getImageID() else image_ for image_ in self.__installedImages]

  def unregisterImage(self,image):
    del self.__installedImagesDict[image.getImageID()]
    self.__installedImages = [ image_ for image_ in self.__installedImages if not image_.getImageID() == image.getImageID()]

  def unregisterNonExistantImages(self):
    for image in self.getInstalledImages():
      if not image.isDockerImageThere():
        self.unregisterImage(image)