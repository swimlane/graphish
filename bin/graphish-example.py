from graphish import GraphConnector
from graphish import Search
from graphish import Delete


connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41',        # your applications Azure Tenant ID
)

search = Search(
    connector,
    userPrincipalName='some.account@myorg.onmicrosoft.com'   # the user's mailbox you want to search
)

new_search = search.create(
    searchFolderName='Phishing Search',
    sourceFolder='inbox',
    filterQuery="contains(subject, 'phish')"
)

messages = search.messages()

for message in messages:
    print(message.id)


# Delete a message
delete = Delete(
    connector,
    userPrincipalName='first.last@myorg.onmicrosoft.com',   # the user's mailbox you want to search
)

for message in messages:
    delete.delete_search_message(search.folderId, message.id)

