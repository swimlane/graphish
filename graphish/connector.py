import requests
import pendulum

from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


__AUTHORITY_URL__ = 'https://login.microsoftonline.com/{tenant}'
__TOKEN_ENDPOINT__ = '/oauth2/v2.0/token'
__API_VERSION__ = 'v1.0'
__BASE_URL__ = 'https://graph.microsoft.com'



class GraphConnector(object):
    """GraphConnector is the main authentication mechanism for graphphish
    """
    
    def __init__(self, clientId, clientSecret, tenantId, username=None, password=None, scopes=['https://graph.microsoft.com/.default'], verify_ssl=True):
        """GraphConnector is the base (parent) class of both Search and Delete classes.  It is used to perform either delegated authentication flows
        like: (Single-Page, Web Apps, Mobile & Native Apps - Grant Auth Flow) or you can use it in the application authentication auth flows like: (Client Credentials Grant Auth Flow)

        
        Args:
            clientId (str): Your Azure AD Application client ID
            clientSecret (str): Your Azure AD Application client secret
            tenantId (str): Your Azure AD tenant ID
            username (str, optional): A username used to authenticate to Azure or Office 365. Defaults to None. If provided, will use delegated authentication flows
            password (str, optional): The password used to authenticate to Azure or Office 365. Defaults to None. If provided, will use delegated authentication flows
            scopes (list, optional): A list of scopes defined during your Azure AD application registration. Defaults to ['https://graph.microsoft.com/.default'].
            verify_ssl (bool, optional): Whether to verify SSL or not. Defaults to True.
        """
        self.username = username
        self.password = password
        self.client_id = clientId
        self.client_secret = clientSecret
        self.tenant_id = tenantId
        self.scopes = []
        if isinstance(scopes, list):
            for scope in scopes:
                self.scopes.append(scope)
        else:
            self.scopes.append(scopes)

        self.verify = verify_ssl
        self.access_token = None
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session.verify = self.verify
        self.expiration = None


    @staticmethod
    def build_endpoint(uri):
        return f'{__BASE_URL__}/{__API_VERSION__}/{uri}'

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def expiration(self):
        return self._expiration

    @expiration.setter
    def expiration(self, value):
        self._expiration = value

    def legacy_app_flow(self):
        oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
        url = __AUTHORITY_URL__.format(tenant=self.tenant_id) + __TOKEN_ENDPOINT__
        token = oauth.fetch_token(token_url=url, username=self.username,
                                  password=self.password, client_id=self.client_id,
                                  client_secret=self.client_secret, scope=self.scopes,
                                  verify=self.verify)
        self.token = token['access_token']
        self.session.headers['Authorization'] = 'Bearer ' + self.token

    def backend_app_flow(self):
        url = __AUTHORITY_URL__.format(tenant=self.tenant_id) + __TOKEN_ENDPOINT__
        self.scope = 'https://graph.microsoft.com/.default'
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=url, 
            client_id=self.client_id, 
            client_secret=self.client_secret,
            scope=['https://graph.microsoft.com/.default']
        )
        
        self.token = token['access_token']
        self.expiration = pendulum.from_timestamp(token['expires_at'])
        self.session.headers['Authorization'] = 'Bearer ' + self.token

    def invoke(self, method, uri, data=None):
        if self.username and self.password:
            self.legacy_app_flow()
        else:
            if self.expiration is None:
                self.backend_app_flow()
            elif self.expiration > pendulum.now().subtract(minutes=30):
                self.backend_app_flow()

        url = self.build_endpoint(uri)
        response = self.session.request(method, url, json=data)
        return response
