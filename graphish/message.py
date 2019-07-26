

class Message(object):

    def __init__(self, graphConnector, messageObject, userPrincipalName):
        self.connector = graphConnector
        if userPrincipalName == 'me':
            self.user = 'me'
        else:
            self.user = 'users/{}'.format(userPrincipalName)
        for key, val in self._recursive_items(messageObject):
            if not hasattr(self, key):
                setattr(self, key, val)
        self.headers = self._get_headers(messageObject['id'])

    def _get_headers(self, messageId):
        extendedPropertyValue = 'String 0x7D'
        uri = "%s/messages/%s?$expand=SingleValueExtendedProperties($filter=id eq '%s')" % (
            self.user,
            messageId,
            extendedPropertyValue
        )
        response = self.connector.invoke('GET', uri)
        headers = response.json()
        for header in headers['singleValueExtendedProperties']:
            return header['value']
    
    def _recursive_items(self, dictionary):
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if type(value) is dict:
                    for item in self._recursive_items(value):
                        yield item
                elif type(value) is list:
                    for item in self._recursive_items(value):
                        for key, val in self._recursive_items(item):
                            yield (key, val)
                else:
                    yield (key, value)
        elif isinstance(dictionary, list):
            for _dict in dictionary:
                for key, value in _dict.items():
                    if type(value) is dict:
                        for item in self._recursive_items(value):
                            yield item
                    elif type(value) is list:
                        for item in self._recursive_items(value):
                            for key, val in self._recursive_items(item):
                                yield (key, val)
                    else:
                        yield (key, value)