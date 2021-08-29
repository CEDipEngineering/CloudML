# CloudML

**The Neural Network model being trained was not made by me! At most I slightly adapated some parts of it. All credit for the example of ML workload goes to https://jhui.github.io/2018/02/11/Keras-tutorial/.** 

Project for parallel invocation of machine learning in Cloud environments such as AWS Lambda and EKS. MLFlow is used as tool for metric collection and analysis.

This project was done on my windows 10 computer, and as such has no garantees for working at all on Linux or Mac. Although it probably would work fine with minor changes.

### Guidelines

Use of this project is free and open. I'd appreciate a mention if you use this, but I don't really mind if you don't.

### How to

Each directory in this repository has a README.md explaining how to use its files.

Before you can use these files, though, there are some things you need set up.

First, an MLFlow Server.

Open an EC2 machine (or you can run it on your own machine, but you might need to Port Forward, not sure), that has MLFlow installed. Write down the public IPv4. Connect to it via ssh, and make sure it has a permanent directory for your data. I used */mnt/mlflow/params-metrics*. To open it execute:

    mlflow server --backend-store-uri /mnt/mlflow/params-metrics --host 0.0.0.0
    
Make sure the port you used (by default 5000) is open in the security group configs of your EC2 machine configuration.

Second, setup your AWS environment variables properly. If you go to your $HOME directory, on Windows C://Users//**username**//, and create a *.aws* folder, you can put a file in there called *credentials* (no file extension), with the following content:

    [default]
    aws_access_key_id=AAKJ...
    aws_secret_access_key=JkKeKw...

Where you replace the values after the equals signs with your AWS credentials. You also might need another file, called *config* (also no file extension) with other settings. I wasn't using AWS on the default region (us-east-1) so I had to set this up with my region.

    [default]
    region = us-east-2

After doing that, you might want to setup your ssh credentials similarly, using

    $ ssh-keygen -t rsa

Will guide you through making a set o keys. On Windows, I was able to do this on PowerShell out of the box, but you may need to update your WS, or use PuTTYGen. Put you private key (*.pem*) on a directory called *.ssh* on the same home directory as the *.aws* folder. Whenever you need to connect to a machine on EC2 repeatedly, you can just make a file called *authorized_keys* in the *.ssh* directory of the machine, and put your public key inside this file. This can be done easily by just copy pasting it into your console and piping the echo commando into a file, like so

    $ echo "YOUR KEY" >> ./.ssh/authorized_keys

This allows you to ssh into the machine without explicitly supplying a key to you powershell.

This is the basic setup you need.
