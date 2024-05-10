# ultralytics-docker-vscode
This is a simple tutorial on how to use [Ultralytics](https://www.ultralytics.com/) inside Docker in VS Code.

1. Please make sure to have the following directory structure:
    ```console
    ravi@dell:~/ultralytics_ws$ tree -a
    .
    ├── .devcontainer
    │   ├── devcontainer.json
    │   └── Dockerfile
    └── src
    ```
2. Below is the content of `devcontainer.json`
    ```json
    {
        "name": "Ultralytics Container",
        "privileged": true,
        "remoteUser": "ravi",
        "build": {
            "dockerfile": "Dockerfile",
            "args": {
                "USERNAME": "ravi"
            }
        },
        "workspaceFolder": "/home/ws",
        "workspaceMount": "source=${localWorkspaceFolder},target=/home/ws/src,type=bind",
        "customizations": {
            "vscode": {
                "extensions":[
                    "twxs.cmake",
                    "donjayamanne.python-extension-pack",
                    "eamodio.gitlens"
                ]
            }
        },
        "containerEnv": {
            "DISPLAY": "unix:0",
        },
        "runArgs": [
            "--net=host",
            "--ipc=host",
            "--gpus=all",
            "-e", "DISPLAY=${env:DISPLAY}"
        ],
        "mounts": [
           "source=/tmp/.X11-unix,target=/tmp/.X11-unix,type=bind,consistency=cached",
           "source=/dev/dri,target=/dev/dri,type=bind,consistency=cached"
        ],
        "postCreateCommand": "sudo chown -R $(whoami) /home/ws/"
    }
    ```
    Do not forget to update the `remoteUser` and `USERNAME` as per the username of your machine.

3. Below is the content of `Dockerfile`
    ```dockerfile
    FROM ultralytics/ultralytics:latest
    ARG USERNAME=USERNAME
    ARG USER_UID=1000
    ARG USER_GID=$USER_UID
    
    # Set the timezone to Tokyo. Otherwise, it asks to set the geographic area later
    ENV TZ=Asia/Tokyo
    RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
    
    # Create the user
    RUN groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
        #
        # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
        && apt-get update \
        && apt-get install -y sudo \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME
    
    RUN apt-get update && apt-get upgrade -y
    RUN apt-get install -y python3-pip
    
    # Install linux packages
    # g++ required to build 'tflite_support' and 'lap' packages, libusb-1.0-0 required for 'tflite_support' package
    RUN apt update \
        && apt install --no-install-recommends -y gcc git zip curl htop libgl1 libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0
    
    # Security updates
    # https://security.snyk.io/vuln/SNYK-UBUNTU1804-OPENSSL-3314796
    RUN apt upgrade --no-install-recommends -y openssl tar
    
    # Install pip packages
    RUN python3 -m pip install --upgrade pip wheel
    
    # Install OpenCV
    RUN apt install -y libopencv-dev python3-opencv
    
    # Needed for imshow in OpenCV
    RUN apt-get update && apt-get install -y libsm6
    
    # Set environment variables
    ENV OMP_NUM_THREADS=1
    
    # Avoid DDP error "MKL_THREADING_LAYER=INTEL is incompatible with libgomp.so.1 library" https://github.com/pytorch/pytorch/issues/37377
    ENV MKL_THREADING_LAYER=GNU
    
    ENV SHELL /bin/bash
    
    # [Optional] Set the default user. Omit if you want to keep the default as root.
    USER $USERNAME
    CMD ["/bin/bash"]
    ```
4. Inside VS Code, please search in Extensions or press <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>X</kbd> for the `Remote Development` Extension and install it.
5. Open VS Code at the project root as shown below:
    ```console
    ravi@dell:~/ultralytics_ws$ code .
    ```
6. Press <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> to open the command palette and search for the command `Dev Containers: Reopen in Container` and execute it. Please wait as it takes some time.
7. You can open a terminal inside VS Code and execute various commands as show below:
    ```console
    ravi@dell:/home/ws$ yolo version
    8.2.11
    ```

# References
* [Ultralytics](https://www.ultralytics.com/)
* [Setup ROS 2 with VSCode and Docker](https://docs.ros.org/en/iron/How-To-Guides/Setup-ROS-2-with-VSCode-and-Docker-Container.html)
* [Dockerfile](https://github.com/ravijo/simple-telnet-client/blob/main/Dockerfile)
  
