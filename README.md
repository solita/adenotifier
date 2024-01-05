# adenotifier
This is a Python library for using Agile Data Engine Notify API. See [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas).

Modules:
- manifest
- notifier

**The repository is provided for reference purposes only and the solution may require modifications to fit your use case. Note that this solution is not part of the Agile Data Engine product. Please use at your own caution.**

## Installation
Install with pip (define version):
```
pip install git+https://github.com/solita/adenotifier.git@v0.2.2
```

Include in requirements.txt (define version):
```
git+https://github.com/solita/adenotifier.git@v0.2.2
```

## Usage
### notifier
- Use the **add_to_manifest** function to add a new entry into a manifest for a given data source. The function will find an open manifest or, if one does not exist, it will create a new one. Arguments:
    - file_url (str): Source file url.
    - source (object): Data source configuration JSON object (see details below).
    - base_url (str): ADE Notify API base url, e.g. https://external-api.{environment}.datahub.{tenant}.saas.agiledataengine.com:443/notify-api.
    - notify_api_key (str): ADE Notify API key.
    - notify_api_key_secret (str): ADE Notify API key secret.
- Use the **notify_manifests** function to notify all open manifests for a given data source. Arguments:
    - source (object): Data source configuration JSON object (see details below).
    - base_url (str): ADE Notify API base url, e.g. https://external-api.{environment}.datahub.{tenant}.saas.agiledataengine.com:443/notify-api.
    - notify_api_key (str): ADE Notify API key.
    - notify_api_key_secret (str): ADE Notify API key secret.

Note that the base URL, key and key secret are specific to your ADE Runtime environment. Also the IP address range of your solution has to be allowed in the ADE service.

The functions expect a data source configuration JSON object in the following format:
```
{
    "id": "example_source/example_entity",
    "attributes": {
        "ade_source_system": "example_source",
        "ade_source_entity": "example_entity",
        "batch_from_file_path_regex": "batch\\.(\\d*)\\.csv\\.gz",
        "path_replace": "https://",
        "path_replace_with": "azure://",
        "single_file_manifest": false,
        "max_files_in_manifest": 1000
    },
    "manifest_parameters": {
        "columns": ["test1", "test2"],
        "compression": "GZIP",
        "delim": "SEMICOLON",
        "format": "CSV",
        "fullscanned": false,
        "skiph": 1
    }
}
```
where:
| Attribute  | Mandatory | Description |
| --- | --- | --- |
| id  | x | Unique identifier for the data source. |
| ade_source_system | x | Source system defined for the source entity in ADE. |
| ade_source_entity | x | Source entity name in ADE. |
| batch_from_file_path_regex | | Regular expression for parsing a batch number from a file name. Supports capturing groups, which are concatenated before casting to integer. |
| path_replace | | Old string value to be replaced in the source file path. |
| path_replace_with | | New string value the source file path will be replaced with. |
| single_file_manifest | | Add_to_manifest calls notify_manifest after file has been added. |
| max_files_in_manifest | | Max files to be added to single manifest. |
| columns | | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |
| compression | | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |
| delim | | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |
| format | x | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |
| fullscanned | | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |
| skiph | | ADE manifest parameter, see [Notify API documentation](https://docs.agiledataengine.com/docs/notify-api-saas) |

In addition to these attributes, you may include other details in the configuration for the purposes of your application. For example, add the storage account name, container name and folder path (Azure) or bucket name and folder path (AWS, GCP) to identify the data source from a file url in a file created event before calling add_to_manifest or notify_manifests.

### manifest
The manifest module contains a class for managing manifests in the ADE Notify API. The Manifest class is used by the functions in the notifier module. Use the Manifest class for custom solutions, see comments in the code.
