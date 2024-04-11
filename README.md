# UI Tests with Selenium Python Pytest
# Documentation

## Features
- The tests use setup/teardown methods for the session. 
- Test with Chrome and Firefox (also in headless).
- Possibility to visually see the execution.
- Possibility to see the screenshots of the errors.
- A html report generated at each test run.

## Install

### Prerequisites:
- Python 3.x installed
- pip package manager installed
- Make sure pip is installed in your system (please see the instructions below).
- Install virtual environment.
- A json file with login credentials would need to be created. 

**Linux/Unix:**
- Run `sudo apt update && sudo apt install python3-pip`

### Setting Up Virtual Environment:
It's recommended to use a virtual environment to manage dependencies. Follow these steps:

**Windows/Linux/Unix:**
1. Install virtualenv if not already installed: 
    ```
    pip install virtualenv
    ```
   or use Python's built-in venv module:
    ```
    python -m venv myenv
2. Create a virtual environment:
    ```
    virtualenv myenv
    ```
3. Activate the virtual environment:
    - **Windows:**
        ```
        myenv\Scripts\activate
        ```
    - **Linux/Unix:**
        ```
        source myenv/bin/activate
        ```
4. Upgrade pip:
    ```
    python -m pip install --upgrade pip
    ```
5. Install dependencies
    ```
    pip install -r requirements.txt
    ```
   
Make sure to replace `myenv` with your preferred name for the virtual environment.

### JSON File for Login Credentials:
Create a JSON file with login credentials to authorize test execution.

### Running Tests:

You can run the tests using pytest. Navigate to the directory containing your test files and run:
   ```
   pytest tests -sv or pytest --headless tests -s -v --cache-clear
   ```

### Accessing the reports and screenshots
* The screenshot of an error is in the 'screenshot' directory.
* The html reports are in the tests/.
* The report.log is in allure_reports/.



# Simulating GitLab locally

## Building a container

You'll need a working [podman installation](https://podman.io/docs/installation) (or docker, if you insist).

The `Dockerfile` in the root of this repository will give you a very similar container to the one GitLab will use when running the tests: based on `python:3.10` and with some basic software pre-installed.
If you want to make modifications, [the Dockerfile reference](https://docs.docker.com/engine/reference/builder/) is a really useful document.

```
podman build -t tester:1 .
```
(do not forget the dot at the end of the command!)

Once this is done, you'll have a container:

```
> podman image list
REPOSITORY                                                       TAG                   IMAGE ID      CREATED        SIZE
localhost/tester                                                 1                     8ba4d2af1298  9 minutes ago  1.72 GB
```

## Using your local container

You can now run your container interactively. Note that you'll want to bind your checked out source directory into the container, or you'll have to go through the trouble of cloning your repository again inside the container.

`-i` gives you an interactive shell
`-t` allocates a tty, which means your interactive shell experience will be *much* more pleasant :-)

```
> podman run -v .:/tests -ti localhost/tester:1 /bin/bash
```

Now you can run your tests:

```
cd /tests
python -m venv container_venv
source container_venv/bin/activate
pip install -r requirements.txt
export BROWSER_NAME=firefox
pytest -sv tests/test_login.py
```

Note that you'll need to explicitly create a separate venv within the container - the one you may already have in your source directory _will not work_ inside the container as it was created with the full path on your host system.
Exiting the container will stop it immediately. You can start it again with `podman start --interactive --attach <container_id>`

Unless you make changes to the `Dockerfile`, there's no need to rebuild the container - if you mess up, you can just remove your container and start a new one!

`podman ps -a` to show all containers (including stopped ones)
`podman rm <container_id>` to remove a container. You can specify multiple IDs at once
`podman image list` to show containers available on your system
`podman rmi <image_id>` to remove an image

If you do make changes to the `Dockerfile` and want to rebuild your container, either remove the existing image or increase the version number.

## Spelling/Links

This README file has been checked for spelling errors and links have been verified.

## Legal Requirements

### Copyright, Funding & Authors

- **Authors**: Okeeva, Heeren
- **Acknowledgment**: 

The development of this software was supported by funding to the Blue Brain Project,
a research center of the École polytechnique fédérale de Lausanne (EPFL), from 
the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.

- **Copyright**: Copyright (c) 2024 Blue Brain Project/EPFL

### Apache-2.0 license
# Apache License, Version 2.0

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

## Terms and Conditions for Use, Reproduction, and Distribution

1. **Definitions**

* "License" shall mean the terms and conditions for use, reproduction,
and distribution as defined by Sections 1 through 9 of this document.
"Licensor" shall mean the copyright owner or entity authorized by
the copyright owner that is granting the License.


* "Legal Entity" shall mean the union of the acting entity and all
other entities that control, are controlled by, or are under common
control with that entity. For the purposes of this definition,
"control" means (i) the power, direct or indirect, to cause the
direction or management of such entity, whether by contract or
otherwise, or (ii) ownership of fifty percent (50%) or more of the
outstanding shares, or (iii) beneficial ownership of such entity.


* "You" (or "Your") shall mean an individual or Legal Entity
exercising permissions granted by this License.


* "Source" form shall mean the preferred form for making modifications,
including but not limited to software source code, documentation
source, and configuration files.


* "Object" form shall mean any form resulting from mechanical
transformation or translation of a Source form, including but
not limited to compiled object code, generated documentation,
and conversions to other media types.


* "Work" shall mean the work of authorship, whether in Source or
Object form, made available under the License, as indicated by a
copyright notice that is included in or attached to the work
(an example is provided in the Appendix below).


* "Derivative Works" shall mean any work, whether in Source or Object
form, that is based on (or derived from) the Work and for which the
editorial revisions, annotations, elaborations, or other modifications
represent, as a whole, an original work of authorship. For the purposes
of this License, Derivative Works shall not include works that remain
separable from, or merely link (or bind by name) to the interfaces of,
the Work and Derivative Works thereof.


* "Contribution" shall mean any work of authorship, including
the original version of the Work and any modifications or additions
to that Work or Derivative Works thereof, that is intentionally
submitted to Licensor for inclusion in the Work by the copyright owner
or by an individual or Legal Entity authorized to submit on behalf of
the copyright owner. For the purposes of this definition, "submitted"
means any form of electronic, verbal, or written communication sent
to the Licensor or its representatives, including but not limited to
communication on electronic mailing lists, source code control systems,
and issue tracking systems that are managed by, or on behalf of, the
Licensor for the purpose of discussing and improving the Work, but
excluding communication that is conspicuously marked or otherwise
designated in writing by the copyright owner as "Not a Contribution."


* "Contributor" shall mean Licensor and any individual or Legal Entity
on behalf of whom a Contribution has been received by Licensor and
subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
   this License, each Contributor hereby grants to You a perpetual,
   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   copyright license to reproduce, prepare Derivative Works of,
   publicly display, publicly perform, sublicense, and distribute the
   Work and such Derivative Works in Source or Object form.


3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.


4. Redistribution. You may reproduce and distribute copies of the
Work or Derivative Works thereof in any medium, with or without
modifications, and in Source or Object form, provided that You
meet the following conditions:


   (a) You must give any other recipients of the Work or
    Derivative Works a copy of this License; and
   
   (b) You must cause any modified files to carry prominent notices
    stating that You changed the files; and

   (c) You must retain, in the Source form of any Derivative Works
    that You distribute, all copyright, patent, trademark, and
    attribution notices from the Source form of the Work,
    excluding those notices that do not pertain to any part of
    the Derivative Works; and

   (d) If the Work includes a "NOTICE" text file as part of its
    distribution, then any Derivative Works that You distribute must
    include a readable copy of the attribution notices contained
    within such NOTICE file, excluding those notices that do not
    pertain to any part of the Derivative Works, in at least one
    of the following places: within a NOTICE text file distributed
    as part of the Derivative Works; within the Source form or
    documentation, if provided along with the Derivative Works; or,
    within a display generated by the Derivative Works, if and
    wherever such third-party notices normally appear. The contents
    of the NOTICE file are for informational purposes only and
    do not modify the License. You may add Your own attribution
    notices within Derivative Works that You distribute, alongside
    or as an addendum to the NOTICE text from the Work, provided
    that such additional attribution notices cannot be construed
    as modifying the License.

   You may add Your own copyright statement to Your modifications and
   may provide additional or different license terms and conditions
   for use, reproduction, or distribution of Your modifications, or
   for any such Derivative Works as a whole, provided Your use,
   reproduction, and distribution of the Work otherwise complies with
   the conditions stated in this License.