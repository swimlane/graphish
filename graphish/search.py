from message import Message
from users import Users


class Search(object):
    """
    This class allows you to interact with and search mailboxes using Microsoft Graph API.
    """
    def __init__(self, graphConnector, includeNestedFolders=True, userPrincipalName=None):
        """The Search class allows you to:
           * Create a new Search
           * Update an existing Search
           * Retrieve messages identified during a search
           * Find search folders on mailboxes
           * Delete a search
        
        Args:
            graphConnector (GraphConnector): A generated GraphConnector object
            includeNestedFolders (bool, optional): When creating a search you can define if you want to search all nested folders or not. Defaults to True.
            userPrincipalName (str, optional): Defaults to the current user, but can be any user defined or provided in this parameter. Defaults to 'me'.
        """
        self.connector = graphConnector
        if not userPrincipalName:
            if self.connector.username and self.connector.password:
                self.user = 'me'
            else:
                self.user = Users(self.connector).get
        else:
            self.user = 'users/%s' % userPrincipalName
        

        self.includeNestedFolders = includeNestedFolders

    def _get_folder_id(self, user):
        for folder in self.folderId:
            for key, val in folder.iteritems():
                if user == key:
                    return val

    @property
    def folderId(self):
        return self._folderId

    @folderId.setter
    def folderId(self, value):
        self._folderId = value

    def folders(self):
        return_list = []
        if isinstance(self.user, list):
            for user in self.user:
                folder_id = self._get_folder_id(user)
                uri = 'users/%s/mailFolders/%s' % (user, folder_id)
                return_list.append({user: self.connector.invoke('GET', uri).json()})
            return return_list
        else:
            folder_id = self._get_folder_id(self.user)
            uri = '%s/mailFolders/%s' % (self.user, folder_id)
            return [{self.user: self.connector.invoke('GET', uri).json()}]

    def messages(self):
        return_list = []
        #folder_id_list = []
        if isinstance(self.user, list):
            for user in self.user:
                folder_id = self._get_folder_id(user)
                uri = 'users/%s/mailFolders/%s/messages' % (user, folder_id)
                response = self.connector.invoke('GET', uri).json()
                message_list = []
                for message in response['value']:
                    message_list.append(
                        Message(
                            self.connector,
                            message,
                            self.user
                        )
                    )
                return_list.append({
                    user: message_list
                })
            return return_list
        else:
            folder_id = self._get_folder_id(self.user)
            uri = '%s/mailFolders/%s/messages' % (self.user, folder_id)
            response = self.connector.invoke('GET', uri).json()
            message_list = []
            for message in response['value']:
                message_list.append(
                    Message(
                        self.connector,
                        message,
                        self.user
                    )
                )
            return [{self.user: message_list}]

    def create(self, searchFolderName, sourceFolder, filterQuery):
        return_list = []
        folder_id_list = []
        if isinstance(self.user, list):
            for user in self.user:
                uri = 'users/%s/mailFolders/%s/childFolders' % (user, sourceFolder)
                body = {
                    "@odata.type": "microsoft.graph.mailSearchFolder",
                    "displayName": "%s" % searchFolderName,
                    "includeNestedFolders": '%s' % self.includeNestedFolders,
                    "sourceFolderIds": ["%s" % sourceFolder],
                    "filterQuery": filterQuery
                }
                response = self.connector.invoke('POST', uri, data=body)
                return_list.append({user: response.json()})
                folder_id_list.append({user: response.json()['id']})
            self.folderId = folder_id_list
            return return_list
        else:
            uri = '%s/mailFolders/%s/childFolders' % (self.user, sourceFolder)
            body = {
                "@odata.type": "microsoft.graph.mailSearchFolder",
                "displayName": "%s" % searchFolderName,
                "includeNestedFolders": '%s' % self.includeNestedFolders,
                "sourceFolderIds": ["%s" % sourceFolder],
                "filterQuery": filterQuery
            }
            response = self.connector.invoke('POST', uri, data=body)
            self.folderId = [{self.user: response.json()['id']}]
            return [response.json()]

    def update(self, searchFolderName=None, sourceFolder=None, filterQuery=None):
        return_list = []
        folder_id_list = []
        if isinstance(self.user, list):
            for user in self.user:
                uri = 'users/%s/mailFolders/%s' % (user, self._get_folder_id(user))
                body = {}
                body['@odata.type'] = "microsoft.graph.mailSearchFolder"
                
                if searchFolderName:
                    body['displayName'] = searchFolderName
                if sourceFolder:
                    body['sourceFolderIds'] = sourceFolder
                if filterQuery:
                    body['filterQuery'] = filterQuery
                body['includeNestedFolders'] ='%s' % self.includeNestedFolders

                response = self.connector.invoke('POST', uri, data=body)
                folder_id_list.append({user: response.json()['id']})
                return_list.append({user: response.json()})
            self.folderId = folder_id_list
            return return_list
        else:
            uri = '%s/mailFolders/%s' % (self.user, self._get_folder_id(self.user))
            body = {}
            body['@odata.type'] = "microsoft.graph.mailSearchFolder"
            
            if searchFolderName:
                body['displayName'] = searchFolderName
            if sourceFolder:
                body['sourceFolderIds'] = sourceFolder
            if filterQuery:
                body['filterQuery'] = filterQuery
            body['includeNestedFolders'] ='%s' % self.includeNestedFolders

            response = self.connector.invoke('POST', uri, data=body)
            self.folderId = [{self.user: response.json()['id']}]
            return [response.json()]


    def delete(self):
        return_list = []
        if isinstance(self.user, list):
            for user in self.user:
                uri = 'users/%s/mailFolders/%s' % (user, self._get_folder_id(user))
                response = self.connector.invoke('DELETE', uri)
                return_list.append({user: response.json()})
            return return_list
        else:
            uri = '%s/mailFolders/%s' % (self.user, self._get_folder_id(self.user))
            response = self.connector.invoke('DELETE', uri)
            return [{self.user: response.json()}]