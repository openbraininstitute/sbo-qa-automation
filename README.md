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
