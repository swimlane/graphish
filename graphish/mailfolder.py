
WELL_KNOWN_FOLDER_NAMES = [
    'archive',
    'clutter',
    'conflicts',
    'conversationhistory',
    'deleteditems',
    'drafts',
    'inbox',
    'junkemail',
    'localfailures',
    'msgfolderroot',
    'outbox',
    'recoverableitemsdeletions',
    'scheduled',
    'searchfolders',
    'sentitems',
    'serverfailures',
    'syncissues'
]


class MailFolder(object):

    def __init__(self, graphConnector, userPrincipalName):
        self.connector = graphConnector
        if userPrincipalName == 'me':
            self.user = 'me/mailFolders'
        else:
            self.user = 'users/{}/mailFolders'.format(userPrincipalName)

    def create(self, folder_name):
        body = {
            'displayName': folder_name
        }
        response = self.connector.invoke('POST', self.user, data=body)
        return response.json()

    
    def list_messages(self, folder_name):
        from message import Message
        return_list = []
        uri = '{user}/{folder}/messages'.format(
            user=self.user,
            folder=folder_name
        )
        response = self.connector.invoke('GET', uri)
        for message in response.json()['value']:
            message_obj = Message(
                        self.connector,
                        message,
                        self.user
                    )
            message_dict = {}
            for item in dir(message_obj):
                if not item.startswith('_') or not item.endswith('_'):
                    message_dict.update({
                        item: getattr(message_obj, item)
                    })
            return_list.append(message)
        return return_list


    def move_message(self, message_id, folder_name):
        uri = '{user}/{folder}/messages/{msg_id}/move'.format(
            user=self.user,
            folder=folder_name,
            msg_id=message_id
        )

        body = {
            'destinationId': folder_name
        }
        response = self.connector.invoke('POST', uri, data=body)
        return response.json()
