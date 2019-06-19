# graphish

A Python package to search & delete messages from mailboxes in Office 365 using Microsoft Graph API

## Current Features

    * Create new Search
    * Update a Search
    * Get Search Folder
    * Get Search messages
    * Delete Search
    * Delete a Message

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

By using the application authentication (Client Credentials Grant Auth Flow) you can search your own mailbox by not passing a `userPrincipalName` or if you would like to search another mailbox then provide the `userPrincipalName` (e-mail address):

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
    userPrincipalName='some.account@myorg.onmicrosoft.com'  # the user's mailbox you want to search
    scopes=['https://graph.microsoft.com/Mail.ReadWrite']   # the scopes (default value of https://graph.microsoft.com/.default)
)
```

### Creating a new Search

Once you have determined your appropriate authentication and have created a `GraphConnector` object, then you can create a new `Search` Object.  Once you have your `Search` Object then you can create a new search.  This will create a hidden folder in the users mailbox (that the user is unable to see) and it will populate based on your search filterQuery.  

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
print(search.messages())
```

### Getting a list of mail folders

If you are needing a list of mail folders in a mailbox you can use the `folders` method to retrieve them:

```python
# get a list of search folders
search.folders()
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

### Additional Examples

You can find additional examples [here](bin/graphish-example.py)

## Release History

* 1.0.0
   * Initial release of graphish to PyPi

## Meta

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator) – rickardja@live.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/swimlane/graphish/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request