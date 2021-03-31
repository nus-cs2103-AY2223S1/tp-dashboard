#!/bin/bash

# Downloads a specific version of RepoSense.jar of your choice from our repository
## Examples of supported options:
### ./get-reposense.py --release               # Gets the latest release (Stable)
### ./get-reposense.py --master                # Gets the latest master (Beta)
### ./get-reposense.py --tag v1.6.1            # Gets a specific version
### ./get-reposense.py --commit abc123         # Gets a specific commit
### ./get-reposense.py --release --overwrite   # Overwrite RepoSense.jar, if exists, with the latest release

./get-reposense.py --release

# Executes RepoSense
# Do not change the default output folder name (reposense-report)
## Examples of other valid options; For more, please view the user guide
### java -jar RepoSense.jar --repos https://github.com/reposense/RepoSense.git

java -jar RepoSense.jar --config ./configs
