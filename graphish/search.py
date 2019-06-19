from message import Message


class Search(object):
    """
    This class allows you to interact with and search mailboxes using Microsoft Graph API.  It's parent class is GraphConnector which handles all authentication.
    """
    def __init__(self, graphConnector, includeNestedFolders=True, userPrincipalName='me'):
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
        if userPrincipalName is not 'me':
            self.user = 'users/%s' % userPrincipalName
        else:
            self.user = userPrincipalName

        self.includeNestedFolders = includeNestedFolders

    @property
    def folderId(self):
        return self._folderId

    @folderId.setter
    def folderId(self, value):
        self._folderId = value

    def folders(self):
        uri = '%s/mailFolders/%s' % (self.user, self.folderId)
        return self.connector.invoke('GET', uri).json()

    def messages(self):
        uri = '%s/mailFolders/%s/messages' % (self.user, self.folderId)
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
        return message_list

    def create(self, searchFolderName, sourceFolder, filterQuery):
        uri = '%s/mailFolders/%s/childFolders' % (self.user, sourceFolder)
        body = {
            "@odata.type": "microsoft.graph.mailSearchFolder",
            "displayName": "%s" % searchFolderName,
            "includeNestedFolders": '%s' % self.includeNestedFolders,
            "sourceFolderIds": ["%s" % sourceFolder],
            "filterQuery": filterQuery
        }
        response = self.connector.invoke('POST', uri, data=body)
        self.folderId = response.json()['id']
        return response.json()

    def update(self, searchFolderName=None, sourceFolder=None, filterQuery=None):
        uri = '%s/mailFolders/%s' % (self.user, self.folderId)
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
        self.folderId = response.json()['id']
        return response.json()

    def delete(self):
        uri = '%s/mailFolders/%s' % (self.user, self.folderId)
        response = self.connector.invoke('DELETE', uri)
        return response.json()