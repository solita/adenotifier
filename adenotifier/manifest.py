import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from typing import List, Set, Dict, Tuple, Optional

class Manifest:
    """Manages source data file manifests with ADE Notify API."""
    __base_url: str = None
    __created: str = None
    __format: str = None
    __id: str = None
    __latest_response: requests.Response = None
    __manifest_entries: object = None
    __modified: str = None
    __session: requests.Session = None
    __source_entity_name: str = None
    __source_system_name: str = None
    __state: str = None

    batch: int = None
    columns: List[str] = None
    compression: str = None
    delim: str = None
    fullscanned: bool = None
    skiph: int = None

    def __init__(self, base_url: str, source_system_name: str, source_entity_name: str, format: str, notify_api_key: str, notify_api_key_secret: str):
        """Class constructor.

        Args:
            base_url (str): ADE Notify API base url, e.g. https://external-api.{environment}.datahub.{tenant}.saas.agiledataengine.com:443/notify-api.
            source_system_name (str): Source system name defined in ADE source entity.
            source_entity_name (str): ADE source entity name.
            format (str): Source file format.
            notify_api_key (str): ADE Notify API key.
            notify_api_key_secret (str): ADE Notify API key secret.

        """
        self.__base_url = base_url
        self.__source_system_name = source_system_name
        self.__source_entity_name = source_entity_name
        self.__format = format
        self.__session = requests.Session()
        self.__session.auth = (notify_api_key, notify_api_key_secret)
        self.__session.headers.update({"Content-Type": "application/json"})
        self.__session.mount('https://', HTTPAdapter(max_retries=Retry(total=3, status_forcelist=[429, 500, 502, 503, 504], backoff_factor=2))) # HTTP request retry settings.

    def __api_caller(self, http_method: str, request_url: str, request_body: str = None):
        """Handles ADE Notify API calls.

        Args:
            http_method (str): Supported values: "get", "post" or "put".
            request_url (str): Request url.
            request_body (str, optional): Request body, if expected by ADE Notify API.
        
        Returns:
            requests.Response object.

        Raises:
            All exceptions if request fails after retries.

        """
        response = None
        
        try:
            if (http_method == "get"):
                response = self.__session.get(request_url, data=json.dumps(request_body))
            elif (http_method == "post"):
                response = self.__session.post(request_url, data=json.dumps(request_body))
            elif (http_method == "put"):  
                response = self.__session.put(request_url, data=json.dumps(request_body))            
        except Exception as e:
            self.__latest_response = response
            raise Exception(e)

        self.__latest_response = response
        return response

    def __refresh_manifest(self):
        """Gets manifest from ADE Notify API, updates object attribute values."""
        request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests/{3}"\
            .format(self.__base_url, self.__source_system_name, self.__source_entity_name, self.__id)

        response = self.__api_caller("get", request_url)
        response_body = response.json()
        self.batch = response_body['batch']
        self.columns = response_body['columns']
        self.compression = response_body['compression']
        self.__created = response_body['created']
        self.delim = response_body['delim']
        self.__format = response_body['format']
        self.fullscanned = response_body['fullscanned']
        self.__id = response_body['id']
        self.__modified = response_body['modified']
        self.skiph = response_body['skiph']
        self.__state = response_body['state']

    def __refresh_manifest_entries(self):
        """Gets manifest entries from Notify API, sets object attribute values."""
        request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests/{3}/entries"\
            .format(self.__base_url, self.__source_system_name, self.__source_entity_name, self.__id)

        response = self.__api_caller("get", request_url)
        self.__manifest_entries = response.json()

    """Getters for private attributes."""
    @property
    def base_url(self):
        return self.__base_url
    @property
    def created(self):
        return self.__created
    @property
    def format(self):
        return self.__format
    @property
    def id(self):
        return self.__id
    @property
    def latest_response(self):
        return self.__latest_response
    @property
    def manifest_entries(self):
        return self.__manifest_entries
    @property
    def modified(self):
        return self.__modified
    @property
    def source_entity_name(self):
        return self.__source_entity_name
    @property
    def source_system_name(self):
        return self.__source_system_name
    @property
    def state(self):
        return self.__state
    
    def create(self):
        """Creates new manifest in ADE Notify API, sets object attribute values from response."""
        request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests"\
            .format(self.__base_url, self.__source_system_name, self.__source_entity_name)

        request_body = {}
        request_body['format'] = self.__format

        # Set optional manifest attributes if defined.
        if self.batch != None:
            request_body['batch'] = self.batch
        if self.columns != None:
            request_body['columns'] = self.columns
        if self.compression != None:
            request_body['compression'] = self.compression
        if self.delim != None:
            request_body['delim'] = self.delim
        if self.fullscanned != None:
            request_body['fullscanned'] = self.fullscanned
        if self.skiph != None:
            request_body['skiph'] = self.skiph

        response = self.__api_caller("post", request_url, request_body)
        response_body = response.json()
        self.batch = response_body['batch']
        self.columns = response_body['columns']
        self.compression = response_body['compression']
        self.__created = response_body['created']
        self.delim = response_body['delim']
        self.__format = response_body['format']
        self.fullscanned = response_body['fullscanned']
        self.__id = response_body['id']
        self.__modified = response_body['modified']
        self.skiph = response_body['skiph']
        self.__state = response_body['state']

    def fetch_manifest(self, id: str = None):
        """Calls __refresh_manifest().

        Args:
            id (str, optional): Manifest id.

        Raises:
            ValueError if manifest id is not set.

        """
        if (id != None):
            self.__id = id
        
        if (self.__id != None):
            self.__refresh_manifest()
        else:
            raise ValueError("Manifest id = None. Create or get manifest before notifying.")

    def fetch_manifest_entries(self):
        """Calls __refresh_manifest_entries().

        Raises:
            ValueError if manifest id is not set.

        """
        if (self.__id != None):
            self.__refresh_manifest_entries()
        else:
            raise ValueError("Manifest id = None. Create or get manifest before notifying.")

    def notify(self, id: str = None):
        """Notifies manifest in Notify API.

        Args:
            id (str, optional): Manifest id.

        Raises:
            ValueError if manifest id is not set.

        """
        if (id != None):
            self.__id = id
            #self.__refresh_manifest ## Disabled by default to reduce API calls, use fetch_manifest().

        if (self.__id != None):
            request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests/{3}/notify"\
                .format(self.__base_url, self.__source_system_name, self.__source_entity_name, self.__id)
            self.__api_caller("post", request_url)
            #self.__refresh_manifest ## Disabled by default to reduce API calls, use fetch_manifest().
        else:
            raise ValueError("Manifest id = None. Create or get manifest before notifying.")

    def add_entry(self, source_file: str, batch: int = None, content_length: int = None):   
        """Appends single entry to manifest in Notify API.

        Args:
            source_file (str): Source file url.
            batch (int, optional): Batch number.
            content_length (int, optional): Content length.

        """
        if (self.__id == None):
            self.create()
        
        request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests/{3}/entries"\
            .format(self.__base_url, self.__source_system_name, self.__source_entity_name, self.__id)

        request_body = {}
        request_body['sourceFile'] = source_file

        # Set optional manifest entry attributes if defined.
        if (batch != None):
            request_body['batch'] = batch
        if (content_length != None):
            request_body['contentLength'] = content_length

        self.__api_caller("post", request_url, request_body)
        #self.__refresh_manifest_entries ## Disabled by default to reduce API calls, use fetch_manifest_entries().

    def add_entries(self, entries: List[dict]):
        """Adds/overwrites multiple entries to manifest in Notify API.

        Args:
            entries (list[dict]): List of manifest entry dictionaries.

        """
        if (self.__id == None):
            self.create()

        request_url = "{0}/tenants/local/installations/local/environments/local/source-systems/{1}/source-entities/{2}/manifests/{3}/entries"\
            .format(self.__base_url, self.__source_system_name, self.__source_entity_name, self.__id)
        
        self.__api_caller("put", request_url, entries)
        #self.__refresh_manifest_entries ## Disabled by default to reduce API calls, use fetch_manifest_entries().
