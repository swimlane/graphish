from .users import Users


class Rules(object):
    """
    This class allows you to interact with and search mailboxes using Microsoft Graph API.  It's parent class is GraphConnector which handles all authentication.
    """
    def __init__(self, graphConnector, userPrincipalName=None):
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
            self.user = [userPrincipalName]

    def get(self):
        return_list = []
        if isinstance(self.user, list):
            for user in self.user:
                uri = f'users/{user}/mailFolders/inbox/messageRules'
                return_list.append({user: self.connector.invoke('GET', uri).json()})
            return return_list
        else:
            uri = f'{self.user}/mailFolders/inbox/messageRules'
            return [{self.user: self.connector.invoke('GET', uri).json()}]

