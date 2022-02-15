from .message import Message
from .users import Users


class Search:
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
                self.user = ['me']
            else:
                self.user = Users(self.connector).get
        else:
            self.user = [userPrincipalName]
        
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
        for user in self.user:
            uri = ''
            if user == 'me':
                uri = f'{self.user}/mailFolders/{self._get_folder_id(user)}'
            else:
                uri = f'users/{user}/mailFolders/{self._get_folder_id(user)}'
            return_list.append({user: self.connector.invoke('GET', uri).json()})
        return return_list

    def messages(self):
        for user in self.user:
            uri = ''
            if user == 'me':
                uri = f'{user}/mailFolders/{self._get_folder_id(user)}/messages'
            else:
                uri = f'users/{user}/mailFolders/{self._get_folder_id(user)}/messages'
            response = self.connector.invoke('GET', uri).json()
            message_list = []
            for message in response['value']:
                message_obj = Message(
                        self.connector,
                        message,
                        user
                    )
                message_dict = {}
                for item in dir(message_obj):
                    if not item.startswith('_') or not item.endswith('_'):
                        message_dict.update({
                            item: getattr(message_obj, item)
                        })
                message_list.append(message_dict)
        return message_list

    def create(self, searchFolderName, sourceFolder, filterQuery):
        return_list = []
        folder_id_list = []
        for user in self.user:
            uri = ''
            if user == 'me':
                uri = f'{user}/mailFolders/{sourceFolder}/childFolders'
            else:
                uri = f'users/{user}/mailFolders/{sourceFolder}/childFolders'
            body = {
                "@odata.type": "microsoft.graph.mailSearchFolder",
                "displayName": f"{searchFolderName}",
                "includeNestedFolders": f'{self.includeNestedFolders}',
                "sourceFolderIds": [f"{sourceFolder}"],
                "filterQuery": filterQuery
            }
            response = self.connector.invoke('POST', uri, data=body)
            if response.json().get('error'):
                raise AssertionError('Error when creating search folder:{}'.format(response.json()))
            else:
                folder_id_list.append({user: response.json()[u'id']})
                return_list.append({user: response.json()})
        self.folderId = folder_id_list
        return return_list

    def update(self, searchFolderName=None, sourceFolder=None, filterQuery=None):
        return_list = []
        folder_id_list = []
        for user in self.user:
            uri = ''
            if user == 'me':
                uri = f'{user}/mailFolders/{self._get_folder_id(user)}'
            else:
                uri = f'users/{user}/mailFolders/{self._get_folder_id(user)}'
            body = {}
            body['@odata.type'] = "microsoft.graph.mailSearchFolder"
            if searchFolderName:
                body['displayName'] = searchFolderName
            if sourceFolder:
                body['sourceFolderIds'] = sourceFolder
            if filterQuery:
                body['filterQuery'] = filterQuery
            body['includeNestedFolders'] = f'{self.includeNestedFolders}'

            response = self.connector.invoke('POST', uri, data=body)
            if u'id' in response.json():
                folder_id_list.append({user: response.json()[u'id']})
                return_list.append({user: response.json()})
            else:
                raise AssertionError('The response when updating a search contains no id property')
        self.folderId = folder_id_list
        return return_list

    def delete(self):
        return_list = []
        for user in self.user:
            uri = ''
            if user == 'me':
                uri = f'{user}/mailFolders/{self._get_folder_id(user)}'
            else:
                uri = f'users/{user}/mailFolders/{self._get_folder_id(user)}'
            response = self.connector.invoke('DELETE', uri)
            return_list.append({user: response.json()})
        return return_list
