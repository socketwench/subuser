ProgramSource
--
__name : string
__repo : Repository
--
getName() : string
getRepository() : Repository
getInstalledImages() : InstalledImage[]
getImage() : InstalledImage or None
buildImage() : InstalledImage
getSubusersBasedOnThisSource() : Subuser[]
getProgramSourceDir() : string
getPermissions() : Permissions
#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import subprocess,os
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.classes.describable,subuserlib.subprocessExtras

class InstalledImage(subuserlib.classes.userOwnedObject.UserOwnedObject,subuserlib.classes.describable.Describable):
  __name = None
  __repo = None

  def __init__(self,user,repo,name):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self.__name = name
    self.__repo = repo

  def getName(self):
    return self.__name

  def getRepository(self):
    return self.__repo

  def getInstalledImages(self):
    """ Get all InstalledImage s built from this ProgramSource, including out of date images. """
    return [image for image in self.getUser().getRegistry().installedImages.getInstalledImages() if image.getProgramSource() == self]

  def getImage(self):
    """ Get the most up to date InstalledImage built from this ProgramSource or None, if there are no InstalledImage s built from this ProgramSource. """
    latestUpdateTime = ""
    imageWithLatestUpdateTime = None
    for image in self.getInstalledImages():
      if image.getLastUpdateTime() > latestUpdateTime:
        latestUpdateTime = image.getLastUpdateTime()
        imageWithLatestUpdateTime = image
    return imageWithLatestUpdateTime

  def getAvailablePrograms(self):
    if not self.__availablePrograms == None:
      return self.__availablePrograms

    if not os.path.exists(self.getRepoPath()):
      self.updateSources()
    programNames = os.listdir(self.getRepoPath())
    availablePrograms = []
    for programName in programNames:
      availablePrograms.append(subuserlib.classes.programSource.ProgramSource(self.getUser(),self,programName))
    self.__availablePrograms = availablePrograms
    return self.__availablePrograms