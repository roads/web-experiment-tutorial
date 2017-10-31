## Web Site Deployment

In this part, we will cover the basics of deploying a website to a server and making it accessible to the outside world. Companion code for this part can be found in the directory `\server-tutorial-wrapper`. This part builds upon the companion website code from the previous part. To help you identify what has been added, new code will be marked using comments *BEGIN NEW CODE* and *END NEW CODE*. The remainder of this tutorial assumes that the server is configured using a LAMP stack and is written for the Mozer Lab server (i.e., https://www.mozerlab.us/).

### Signing into the Server
In order to deploy the website to a server, you need server credentials (i.e, a username and password). Your admin should have provided you will these. In case you are interested, creating a new user is straightforward. An existing user with sudo privileges (i.e., your admin) issues the following commands on the server:
```shell
sudo adduser user_name
sudo adduser user_name lab
```
where `user_name` would be the actual name of the new user. The first line creates the new user and the second line adds them to the group `lab`. Belonging to the group `lab` is important because it grants the user privileges that will be important later. When your account is initially created, the person creating your account may assign you a temporary password. You can change your password at any time by issuing the following command once you are signed in with your temporary password:
```shell
passwd
```

Once you have a user account, you sign into the server from your local machine using a secure shell protocol (SSH). To sign in you issue the following command from a shell terminal on your local machine:
```shell
ssh -p 22 user_name@159.203.207.54
```
The numbers at the end of the command indicate the IP address of the lab server. The `-p 22` indicates port 22. Upon issuing this command you should be prompted for your password. If your password is correct you will now be logged into the server. To exit the server type `exit`.

### Copying Files from a Local Machine to the Server
In order for the server to host a website, the website files need to be moved to the appropriate location on the server. In our case, we want to move the directory containing our website to a standard server directory for hosting websites: `/var/www/html`. Since you were added to the the group `lab`, you have the appropriate access privileges to the directory `/var/www/html`. Since this is a shared directory, you will need to be careful that your directory name is not already being used by another user. If you are logged into the server, you can see which directory names are being used by listing them all.
```shell
cd /var/www/html
ls
```

When you are developing a website, you will modify web code on your local machine and copy it to the server. Since you will be making numerous changes to your code during development you will want to have a way to easily update the relevant web files on the server. This is accomplished using a handy python script `deploy_website.py`. When you have new files you would like to upload to the server (i.e., copy to `/var/www/html`) you execute the following code from a terminal on your local machine:
```shell
python3 deploy_website.py v0
```
The code should be executed after you have moved to the directory level where the directory `\web-tutorial` resides. The argument "v0" indicates that the web files are being uploaded using the configuration file `_v0.config.py`.

### Configuration File
The configuration file is where we will store server credentials, AWS credentials, and experiment parameters. If you open `_v0.config.py` you will see three different sets of vairables. The first set of variables store server information and credentials (username, password, ipaddr, port), These are filled out with the same information that you would use for an SSH session. The second set of variables define the URL of the website (htdocsUrl) and indicate the location of the web files on the server (htdocsPath). Note that in this setup, the directory name of the website should be the same as the last part of the URL. The last set of variables is stored in the dictionary `expConfig`. The variable `expConfig' holds basic information basic information (`codeVersion`, `website`, `htdocsUrl`) as well as experiment paramters. For example, we have moved the variables `nScreen` and `debugOn` from being hard-coded in `index.html` to  `_v0.config.py`. An advantage of using configuration files is that you can parameterize your experiment and create different experiment versions using different configuration files.

The information contained in the configuration file is loaded by the server and provided to the webpage using Common Gateway Interface (CGI) scripts stored in the directory `cgi-bin`. The `index.html` file has been modified to load the configuration file.

### Your Own Version

If you would like to create your own version of this website to play around with and modify, do the following.
1. Make a copy of the `\server-tutorial-wrapper` directory.
2. Rename the website directory `\server-tutorial` by prefixing it with your user name (e.g., `\yourusername-server-tutorial`)
3. Change the website name in the deploy_website.py file
  * `website = 'yourusername-server-tutorial'`)
4. Modify the `_v0.config.py` configuration file.
  * Change the user name (e.g., `username = 'yourusername'`
  * Change the password to the appropriate password (e.g. `password = ‘yourpassword’`)
  * Change the website name (e.g., `website = ‘yourusername-server-tutorial’`)
5. Deploy the website by running `python3 deploy_website.py v0` from a terminal on your local machine while within the wrapper directory (`\server-tutorial-wrapper`).
6. If everything worked you should now be able to view the website at www.mozerlab.us/yourusername-server-tutorial.
7. Modify the code as you see fit and redeploy.
