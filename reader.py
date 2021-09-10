import yaml


class YamlReader:
  data = {}

  def __init__(self, *args):
    self.load_multiple_yaml_file(args)


  def load_multiple_yaml_file(self, args):
    """
    Load multiple yaml files into a dictionary.
    """
    sList = []
    for file in args:
      with open (file , "r") as stream:
        sList.append(stream.read())
    fString = ''
    for s in sList:
      fString = fString + "\n" + s
    self.data = yaml.load(fString)

"""

  def get_app_json(self, appName):
    for app in self.data:
      if app["name"] == appName:
        return app
    return None


  def get_fctId_for_bankId(self, appName, bankId):
    
   # Returns the list of functional IDs for a given 1bankid in a single yaml file
    
    appJson = self.get_app_json(appName)
    if appJson:
      fctId = []
      userList = appJson["users"]
      #the key name is actually the functionalID
      for user in userList:
        currentfctId = user["name"]
        if bankId in user["1bankids"].split(","):
          fctId.append(currentfctId)
      return fctId
    return None
"""