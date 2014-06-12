Permissions
--
__permissionsDict
--
getHasExecutable() : bool
setHasExecubable(hasExecubable : bool) : None
getLastUpdateTime() : string
setLastUpdateTime(lastUpdateTime : string) : None
getExecubable() : string
setExecubable(executable : string) : None
getDependency() : string
setDependency(dependency : string) : None
getUserDirs() : string[]
setUserDirs(userDirs : string []) : None
getSystemDirs() : string[]
setSystemDirs(systemDirs : string[]) : None
getX11() : bool
setX11(x11Allowed : bool) : None
getGraphicsCard() : bool
setGraphicsCard(graphicsCardAllowed : bool) : None
getSoundCard() : bool
setSoundCard(soundCardAllowed : bool) : None
getWebcam() : bool
setWebcam(webcamAllowed : bool) : None
getInheritWorkingDirectory() : bool
setInheritWorkingDirectory(inheritWorkingDirectory : bool) : None
getAllowNetworkAccess() : bool
setAllowNetworkAccess(allowNetworkAccess : bool) : None
getStatefullHome() : bool
setStatefullHome(statefullHome : bool) : None
getAsRoot() : bool
setAsRoot(asRoot : bool) : None
getPrivileged() : bool
setPrivileged(privileged : bool) : None
#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import subprocess,os
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.classes.programSource,subuserlib.subprocessExtras

class InstalledImage(subuserlib.classes.userOwnedObject.UserOwnedObject):
  __name = None
  __gitOriginURI = None
  __availablePrograms = None

  def __init__(self,user,name,gitOriginURI):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self.__name = name
    self.__gitOriginURI = gitOriginURI

  def getName(self):
    return self.__name

  def getGitOriginURI(self):
    return self.__gitOriginURI

  def getRepoPath(self):
    """ Get the path of the repo's sources on disk. """
    return os.path.join(self.getUser().homeDir,".subuser","repositories",self.getName())

  def updateSources(self):
    """ Pull(or clone) the repo's ProgramSources from git origin. """
    if not os.path.exists(self.getRepoPath()):
      subuserlib.subprocessExtras.subprocessCheckedCall(["git","clone",self.getGitOriginURI(),self.getRepoPath()])
    else:
      subprocess.POpen(["git","pull"],cwd=self.getGitOriginURI()).communicate()

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