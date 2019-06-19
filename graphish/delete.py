


class Delete(object):

    def __init__(self, graphConnector, userPrincipalName='me'):
        """The Delete class deletes a message from a users mailbox.  

            NOTE: Please note that this will do a soft delete and it is only recoverable via "Recoverable Items" feature on a mailbox.
                  This also means that you will not see it in the users delete items folder.
        
        Args:
            graphConnector (GraphConnector): A generated GraphConnector object
            verify_ssl (bool, optional): Whether to verify SSL or not. Defaults to True.
            userPrincipalName (str, optional): Defaults to the current user, but can be any user defined or provided in this parameter. Defaults to 'me'.
        """
        self.connector = graphConnector
        if userPrincipalName is not 'me':
            self.user = 'users/%s' % userPrincipalName
        else:
            self.user = userPrincipalName

    def delete(self, messageId):
        uri = '%s/messages/%s' % (self.user, messageId)
        response = self.connector.invoke('DELETE', uri)
        if response.status_code is '204':
            return True
        return False

    def delete_search_message(self, mailFolder, messageId):
        uri = '%s/mailFolders/%s/messages/%s' % (self.user, mailFolder, messageId)
        response = self.connector.invoke('DELETE', uri)
        if response.status_code is '204':
            return True
        return False