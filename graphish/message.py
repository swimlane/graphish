

class Message(object):

    def __init__(self, graphConnector, messageObject, userPrincipalName):
        self.connector = graphConnector
        self.user = userPrincipalName
        for key in messageObject:
            setattr(self, key, messageObject[key])

        self.headers = messageObject['id']

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, messageId):
        extendedPropertyValue = 'String 0x7D'
        uri = "%s/messages/%s?$expand=SingleValueExtendedProperties($filter=id eq '%s')" % (
            self.user,
            messageId,
            extendedPropertyValue
        )
        response = self.connector.invoke('GET', uri)
        headers = response.json()
        for header in headers['singleValueExtendedProperties']:
            self._headers = header['value']