class Message(object):

    def __init__(self, graphConnector, messageObject, userPrincipalName):
        self.connector = graphConnector
        if userPrincipalName == 'me':
            self.user = 'me'
        else:
            self.user = f'users/{userPrincipalName}'
        
        self.__message__ = messageObject
        self.headers = self._get_headers(messageObject['id'])

    @property
    def sentDateTime(self):
        return self.__message__.get('sentDateTime')

    @property
    def conversationId(self):
        return self.__message__.get('conversationId')

    @property
    def internetMessageId(self):
        return self.__message__.get('internetMessageId')

    @property
    def id(self):
        return self.__message__.get('id')

    @property
    def isReadReceiptRequested(self):
        return self.__message__.get('isReadReceiptRequested')

    @property
    def subject(self):
        return self.__message__.get('subject')

    @property
    def lastModifiedDateTime(self):
        return self.__message__.get('lastModifiedDateTime')

    @property
    def bodyPreview(self):
        return self.__message__.get('bodyPreview')

    @property
    def fromAddress(self):
        return self.__message__['from']['emailAddress']['address']

    @property
    def fromName(self):
        return self.__message__['from']['emailAddress']['name']

    @property
    def flag(self):
        if self.__message__.get('flag'):
            return self.__message__['flag']['flagStatus']
        else:
            return None

    @property
    def isDraft(self):
        return self.__message__.get('isDraft')

    @property
    def replyTo(self):
        reply_list = []
        for item in self.__message__.get('replyTo'):
            reply_list.append(item)
        return reply_list

    @property
    def changeKey(self):
        return self.__message__.get('changeKey')

    @property
    def receivedDateTime(self):
        return self.__message__.get('receivedDateTime')

    @property
    def parentFolderId(self):
        return self.__message__.get('parentFolderId')

    @property
    def body(self):
        return self.__message__['body']['content']

    @property
    def bodyContentType(self):
        return self.__message__['body']['contentType']

    @property
    def isDeliveryReceiptRequested(self):
        return self.__message__.get('isDeliveryReceiptRequested')

    @property
    def importance(self):
        return self.__message__.get('importance')

    @property
    def toRecipients(self):
        recipients_list = []
        for recipient in self.__message__['toRecipients']:
            recipients_list.append({
                recipient['emailAddress']['name']: recipient['emailAddress']['address']
            })
        return recipients_list

    @property
    def ccRecipients(self):
        recipients_list = []
        for recipient in self.__message__['ccRecipients']:
            recipients_list.append({
                recipient['emailAddress']['name']: recipient['emailAddress']['address']
            })
        return recipients_list

    @property
    def isRead(self):
        return self.__message__.get('isRead')

    @property
    def categories(self):
        cat_list = []
        for item in self.__message__['categories']:
            cat_list.append(item)
        return cat_list

    @property
    def sender(self):
        return self.__message__['sender']['emailAddress']['address']

    @property
    def senderName(self):
        return self.__message__['sender']['emailAddress']['name']

    @property
    def createdDateTime(self):
        return self.__message__['createdDateTime']

    @property
    def webLink(self):
        return self.__message__['webLink']

    @property
    def hasAttachments(self):
        return self.__message__.get('hasAttachments')

    @property
    def bccRecipients(self):
        recipients_list = []
        for recipient in self.__message__['bccRecipients']:
            recipients_list.append({
                recipient['emailAddress']['name']: recipient['emailAddress']['address']
            })
        return recipients_list

    @property
    def inferenceClassification(self):
        return self.__message__['inferenceClassification']

    @property
    def focused(self):
        if self.__message__.get('focused'):
            return self.__message__.get('focused')

    @property
    def odataTag(self):
        return self.__message__['@odata.etag']


    def _get_headers(self, messageId):
        extendedPropertyValue = 'String 0x7D'
        uri = f"{self.user}/messages/{messageId}?$expand=SingleValueExtendedProperties($filter=id eq '{extendedPropertyValue}')"
        response = self.connector.invoke('GET', uri)
        headers = response.json()
        for header in headers['singleValueExtendedProperties']:
            return header['value']
