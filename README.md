# Welcome to graphish documentation!

```
  _______ .______          ___      .______    __    __   __       _______. __    __  
 /  _____||   _  \        /   \     |   _  \  |  |  |  | |  |     /       ||  |  |  | 
|  |  __  |  |_)  |      /  ^  \    |  |_)  | |  |__|  | |  |    |   (----`|  |__|  | 
|  | |_ | |      /      /  /_\  \   |   ___/  |   __   | |  |     \   \    |   __   | 
|  |__| | |  |\  \----./  _____  \  |  |      |  |  |  | |  | .----)   |   |  |  |  | 
 \______| | _| `._____/__/     \__\ | _|      |__|  |__| |__| |_______/    |__|  |__| 
                                                                                      

A Python package to search & delete messages from mailboxes in Office 365 using Microsoft Graph API
```

## Current Features

    * Searching
        * Create new Search
        * Update a Search
        * Get Search Folder
        * Get Search messages
        * Delete Search
    * Deleting
        * Delete a Message
    * Mailbox Rules
        * List Mailbox Rules
    * Users
        * Return a list of email addresses in your Azure AD Tenant
    * MailFolder
        * Create MailFolder
        * Move message to a MailFolder
        * List messages in a MailFolder

## Installation

To use, please install the package locally:

## Installation

Locally:

``bash
git clone git@github.com:swimlane/graphish.git
cd graphish
pip install setup.py
``

OS X & Linux:

```bash
pip install graphish
```

Windows:

```bash
pip install graphish
```

## Usage

To use, you will need to have created a new application in Azure AD.  Follow these instructions to obtain the appropriate secrets:

https://docs.microsoft.com/en-us/graph/auth-register-app-v2

Please also checkout this blog post about `graphish` [https://swimlane.com/blog/swimlane-open-sources-graphish/](https://swimlane.com/blog/swimlane-open-sources-graphish/)

Additionally, if you would like `graphish` to search all users within your Azure tenant you need to provide `User.Read.All` permissions to your Azure AD application during registration.

Once you have this information, then you can do the following:

### GraphConnector

To use `graphish` you must first create a `GraphConnector` object that contains all your authentication information.  Once you have created this connector object then a user will provide this object as a mandatory parameter to other classes within this package.

Here are the different ways to generate a `GraphConnector` object and are dependent on which authentication workflow method you have choose for your application.

#### Delegated Authentication

To use `graphish` with delegated permissions and a username and password you will need to supply the clientId, clientSecret, tenantId, as well as your accounts username and password.

By using the delegated authentication (Single-Page, Web Apps, Mobile & Native Apps - Grant Auth Flow) you can search your own mailbox by not passing a `userPrincipalName` or if you would like to search another mailbox then provide the `userPrincipalName` (e-mail address):

#### Creating connector for your account using a (Single-Page, Web Apps, Mobile & Native Apps) authentication flow:

```python
from graphish import GraphConnector

connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41',        # your applications Azure Tenant ID
    userPrincipalName='first.last@myorg.onmicrosoft.com',   # the user's mailbox you want to search
    password='somepassword'                                 # password of your normal or admin account
)
```
#### Creating connector for another users mailbox using a (Single-Page, Web Apps, Mobile & Native Apps) authentication flow:

```python
from graphish import GraphConnector

# For legacy app grant flow provide a username and password
connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41',        # your applications Azure Tenant ID
    userPrincipalName='first.last@myorg.onmicrosoft.com',   # the user's mailbox you want to search
    password='somepassword'                                 # password of your normal or admin account
    userPrincipalName='some.account@myorg.onmicrosoft.com'  # the user's mailbox you want to search
)
```

### Application Authentication

To use `graphish` with application permissions you will need to supply the clientId, clientSecret, and tenantId.

By using the application authentication (Client Credentials Grant Auth Flow) you can search a specific mailbox or ALL mailboxes. 

#### Creating a connector for your account using a service/daemon authentication flow:

```python
from graphish import GraphConnector

# For backend / client_credential auth flow just supply the following
connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41',        # your applications Azure Tenant ID
)
```

#### Creating a connector for another users mailbox using a service/daemon authentication flow:

```python
from graphish import GraphConnector

# For backend / client_credential auth flow just supply the following
connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41',        # your applications Azure Tenant ID
    scopes=['https://graph.microsoft.com/.default']         # the scopes (default value of https://graph.microsoft.com/.default)
)
```

### Creating a new Search

Once you have determined your appropriate authentication and have created a `GraphConnector` object, then you can create a new `Search` Object.  Once you have your `Search` Object then you can create a new search, retrieve messages from your search, get search folders, update a search folder, or delete a search.  When you create a new search, this will create a hidden folder in the users mailbox (that the user is unable to see) and it will populate based on your search filterQuery.  

When you create (or instantiate) a `Search` object you can specify the scope of your search. There are three use-cases related to specifying a search:

- Provide a user principal name to the `userPrincipalName` parameter on the `Search` class
- Provide 'me' to the `userPrincipalName` parameter on the `Search` class when you are using username and password authentication workflow
- **DEFAULT**: Provide no value to the `userPrincipalName` parameter on the `Search` class.  This will pull in all users within your Azure AD via the ListUsers endpoint.

**NOTE: If using application authentication workflow, you can either pass in a single or list of  userPrincipalName's.  If you DO NOT pass in a userPrincipalName then Search will attempt to search all mailboxes in your Azure AD tenant!**

```python
from graphish import Search

search = Search(connector)

new_search = search.create(
    searchFolderName='Phishing Search',
    sourceFolder='inbox',
    filterQuery="contains(subject, 'EXPIRES')"
)
```

### Getting messages from a Search

You can retrieve messages identified during your search by using the same instance of your Search object and using the `messages` method:

```python
# get all the messages in your search folder

for message in search.messages():
    print(message) # Returns all attributes from a message
    print(message['id']) # returns the message ID
    print(message['headers']) # Returns the RFC822 headers of the message
```

### Getting a list of mail folders

If you are needing a list of mail folders in a mailbox you can use the `folders` method to retrieve them:

```python
# get a list of search folders
search.folders()
```


### Getting a list of users

If you are needing a list of all users within your search scope:

```python
# get a list of users
search.user
```

### Moving a message to a folder

If you have performed a search and want to move a message to a mail folder, you can do so by doing the following:

```python
from graphish import Search
from graphish import GraphConnector
from graphish import MailFolder


connector = GraphConnector(
    clientId='14b8e5asd-c5a2-4ee7-af26-53461f121eed',       # you applications clientId
    clientSecret='OdhG1hXb*UB/ho]A?0ZCci13KMflsHDy',        # your applications clientSecret
    tenantId='c1141d00-072f-1eb9-2526-12802571dd41'         # your applications Azure Tenant ID
)

search = Search(connector, userPrincipalName='some.account@myorg.onmicrosoft.com')

new_search = search.create(
    searchFolderName='Phishing Search',
    sourceFolder='inbox',
    filterQuery="contains(subject, 'phishing')"
)

messages = search.messages()
for message in messages:
    print(message['internetMessageId'])
    print(message['fromAddress'])
    print(message['id'])
    mail_folder = MailFolder(connector,'some.account@myorg.onmicrosoft.com')
    moved_message = mail_folder.move_message(message['id'],'junkemail')
    print(moved_message)

```

### Creating a new MailFolder

You can also create a new `MailFolder` using the `MailFolder` class:

```python
from graphish import MailFolder

mail_folder = MailFolder(connector,'some.account@myorg.onmicrosoft.com')
new_mail_folder = mail_folder.create('My Phishing Folder')['id']
```

### Updating a search

If you wanted to make changes to a search performed you can update the search folder and individual criteria like the name of the search folder, the sourceFolder (root to search), or the filterQuery itself:

```python
# update your search folder property's
search.update(
    searchFolderName='Some Phishing Search',
    sourceFolder='inbox',
    filterQuery="contains(subject, 'EXPIRES!')"
)
```

### Deleting a search

You can also delete a search performed by using the `delete` method:

```python
# delete the current search folder
search.delete()
```

### List Mailbox Rules

Additionally, you can list any mailbox rules:

```python
from graphish import Rules

rules = Rules(
    connector,
    userPrincipalName='some.account@myorg.onmicrosoft.com'
)

print(rules.get())
```


### Additional Examples

You can find additional examples [here](bin/graphish-example.py)

## Release History

* 1.0.0
   * Initial release of graphish to PyPi
* 1.3.0
   * Added capabilities to get all users and to move messages to a specified mailfolder

## Meta

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator) – rickardja@live.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/swimlane/graphish/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
