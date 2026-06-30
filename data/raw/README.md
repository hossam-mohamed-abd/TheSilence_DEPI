# Raw Data Storage

## Overview

The MediSearch project uses **Backblaze B2 Cloud Storage** as the primary storage layer for all raw and historical datasets.

This storage is responsible for storing:

- Raw web scraping data
- Historical datasets
- Logs
- Pharmacy exports
- AI training datasets
- Large files that should not be stored inside GitHub.

---

# Usage Guide

This document provides a high-level overview of the Raw Data Storage architecture.

For implementation details and code examples, including:

- Uploading files
- Downloading files
- Listing files
- Deleting files
- Connecting using Python and boto3
- Working with folders and datasets

Please refer to:

```text
infrastructure/raw_data_storage_guide.md
```

or:

```text
infrastructure/raw_data_storage_usage.md
```

GitHub Link:

https://github.com/hossam-mohamed-abd/TheSilence_DEPI/blob/main/infrastructure/raw_data_storage.md

This guide is required for all developers who need to interact with the Raw Data Storage.
