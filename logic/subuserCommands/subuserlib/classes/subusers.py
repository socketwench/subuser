Subusers
--
__subuserDict
--
getSubusers() : Subuser[]
registerSubuser(subuser : Subuser) : None
unregisterSubuser(subuser : Subuser) None
getSubuserNamed(subuserName : string) : Subuser or None
addSubuser(subuserName : string
      , image = InstalledImage) : None#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import subprocess
#internal imports
import subuserlib.classes.fileBacked, subuserlib.classes.userOwnedObject, subuserlib.classes.repository,subuserlib.loadMultiFallbackJsonConfigFile

class Repositories(subuserlib.classes.userOwnedObject.UserOwnedObject,subuserlib.classes.fileBackedObject.FileBackedObject):
  __repositoriesDict = {}
  __repositories = None
  __defaultRepository = None

  def _getRepositoryListPaths():
    """ Returns a list of paths to repositories.json files in order that they should be looked in. """
    repositoryListPaths = []
    repositoryListPaths.append(os.path.join(self.getUser().homeDir,".subuser","repositories.json"))
    repositoryListPaths.append("/etc/subuser/repositories.json") # TODO how does this work on windows?
    repositoryListPaths.append(os.path.join(_getSubuserDir(),"repositories.json"))
    return repositoryListPaths

  def reloadRepositoryList(self):
    """ Load the repository list from disk, discarding the current in-memory version. """
    repositories = subuserlib.loadMultiFallbackJsonConfigFile.getConfig(getRepositoryListPaths())
    __repositories = None
    self.__repositoriesDict = repositories

  def save(self):
    """ Save attributes of the installed images to disk. """
    higherLevelLists = []
    higherLevelLists.append("/etc/subuser/repositories.json") # TODO how does this work on windows?
    higherLevelLists.append(os.path.join(_getSubuserDir(),"repositories.json"))
    whatsOnDisk = subuserlib.loadMultiFallbackJsonConfigFile.getConfig(higherLevelLists)
    whatNeedsToBeSaved = {}
    for repo,attributes in self.__repositoriesDict.iteritems():
      if not repo in whatsOnDisk or not whatsOnDisk[repo] == attributes:
        whatNeedsToBeSaved[repo]=attributes
    with open(os.path.join(self.getUser().homeDir,".subuser","repositories.json"), 'w') as file_f:
      json.dump(whatNeedsToBeSaved, file_f, indent=1, separators=(',', ': '))

  def __init__(self,user):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self.reloadRepositoryList()

  def getRepositories(self):
    if not self.__repositories == None:
      return self.__repositories

    for repoName,repoAttributes in self.__repositoriesDict.iteritems():
      self.__repositories.append(subuserlib.classes.repository.Repository(self.getUser(),name=repoName,gitOriginURI=repoAttributes["git-remote-uri"]))
    return self.__repositories

  def registerRepository(self,repo):
    """ If there is a repository in the repo list with the same name, replace it, otherwise add a new repo to the repo list. """
    # set the repo's attributes in the __repositoriesDict
    self.__repositoriesDict[repo.getName]={"git-origin-uri":repo.getOriginURI()}

    # update or add an entry to the __installedImages list
    self.__repositories = [repo if repo_.getName() == repo.getName() else repo_ for repo_ in self.__repositories]

  def unregisterRepository(self,repo):
    del self.__repositoriesDict[repo.getName()]
    self.__repositories = [ repo_ for repo_ in self.__repositories if not repo_.getName() == repo.getName()]

  def getRepositoryNamed(repoName):
    """ Returns either the repository of the given name or None if no repo with that name exists. """
    for repo in self.__repositories:
      if repo.getName() == repoName:
        return repo
    return None