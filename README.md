# Web Experiment Tutorial

## Authors

* **Brett D. Roads** - *Initial writing, tutorial organization, and code contributor.* - [personal
 website](bdroads.com)
* **Mohammad Khajah** - *Code contributor.*

## Current Admin(s)
* **Adam Winchell** - adwi8859@colorado.edu
* **Brett D. Roads** - brett.roads@colorado.edu

## Introduction
The following tutorial is designed to help you deploy an online web experiment on Amazon Mechanical Turk (AMT). The tutorial is organized into four parts. Each part builds upon the previous part.
1. Website Construction `\website-tutorial-wrapper`
2. Website Deployment `\server-tutorial-wrapper`
3. Database Configuration `\db-tutorial-wrapper`
4. AMT Configuration `\amt-tutorial-wrapper`

Each part is describe in more detail in its own section below. Companion code can found in the directories listed next to each part. The companion code is designed to serve as near-ready working examples that you can modify. The best teacher is modifying the code to get it to do something new and relevant for your goals. Throughout the tutorial, you will have many unanswered questions. Both
[w3schools.com](https://www.w3schools.com) and [stackoverflow.com](https://stackoverflow.com) are excellent resources for learning more about web development.

NOTE: The tutorial is designed to cover details pertinent to deploying a web experiment. This tutorial does not cover website design or experimental design.

### Requirements
In order to complete this tutorial you will need the following:
1. Server Credentials
  * User account and password
  * Database account and password
2. Amazon Web Services (AWS) Credentials
  * Access Key ID
  * Secret Access Key

If your admin has not already provided you with these credentials, you should go ahead and request them. If you will not be deploying your experiment on AMT, you will not need AWS credentials.

NOTE: If you will be running an actual experiment you *must* have prior IRB approval and current CITI certification (see: https://www.colorado.edu/researchinnovation/irb).


## Web Site Construction
In this part, we will construct a simple website in order to conduct a silly experiment. Construction of this simple website will introduce some fundamental concepts and give us something to use in later parts of the tutorial. Companion code for this part can be found in the directory `\website-tutorial-wrapper`. The companion code can be run directly from you local machine by opening `index.html` with your preferred browser. Right click `index.html`, select "open as...", and select a browser. In this part of the tutorial, the website will not be made publicly accessible.

### The Simple Experiment
In the web experiment, participants will be shown one of two letters (A or B). Upon seeing the letters, participants must click one of two buttons labeled "A" or "B". After responding, participants will receive feedback if they were correct. A working version of this experiment can be seen at [www.mozerlab.us/server-tutorial](https://www.mozerlab.us/server-tutorial).

### Three Conceptual Pieces
In order to construct this website, we will follow best practices and split the construction of the website into three different conceptual pieces: content, style, and behavior. We will place each conceptual piece in a separate file:
* Content - `index.html`
* Style - `general.css`
* Behavior - `AppController.js`

As you can see from the filename extensions, we will be using three different languages: HTML, CSS, and JavaScript.

Let's start with the content of the website. The `index.html` file specifies all of the web elements that we want to use in our experiment. Web elements include things like paragraphs, buttons, input boxes, and more abstract elements such as divs. When assembled correctly, a collection of web elements create a sensible website. If you are new to HTML, check out the in-depth HTML tutorial at w3schools (https://www.w3schools.com/html/). In the header, we import the files `general.css` and `AppController.js`. We also import the convenient jQuery and Bootstrap libraries ( 'jquery.js', 'bootstrap.js', and 'bootstrap.css'). To make the layout of the page neat and professional, we use Bootstrap's grid system (http://getbootstrap.com/docs/4.0/layout/grid/). All of the content related to the experiment will reside in three divs with the class `begin-content`, `trial-content`, and `end-content`. The experiment instructions are placed in `begin-content`, the trial content in `trial-content`, and the concluding instructions in `end-content`. The three most important elements are the stimulus (`id=trial-content__stimulus`) and the two submission buttons (`class=content__submit-button`). At the bottom of `index.html`, there is a block of JavaScript code that creates an `AppController` object *after* the page elements finish loading. We pass the `AppController` a configuration variable `cfg` that specifies the number of trials and whether we should print debug messages to the browser console.

The style (i.e., look) of the experiment is specified in our `general.css` file. To help keep the code legible, element IDs and classes are named using block, element, modifier (BEM) conventions (http://getbem.com/naming/). While any styling is possible, it is best to make the webpage look as clean and professional as possible.

The behavior of the experiment is governed by the code contained in the `AppController.js` file. Following common practice, we have wrapped most of the behavior code in a JavaScript object called `AppController` in order to limit the number of variables in the global namespace. Since this is a simple experiment, only a handful of functions are necessary to operate the entire website. In addition to `AppController.js`, we have a second JavaScript file called 'utils.js', which provides utility functions. At the moment, the only utility function we have is `Console_Debug` which prints out messages to the browser console if `cfg.debugOn` is true. We can use `Console_Debug` to help us diagnose issues during web development.

To keep our files nice and organized, we will be using the following file architecture:
* `\website-tutorial`
  * `index.html`
  * `\css`
    * `bootstrap.css`
    * `general.css`
  * `\js`
    * `AppController.js`
    * `bootstrap.js`
    * `jquery-1.11.3.js`
    * `jquery-ui-1.12.1.min.js`
    * `utils.js`

NOTE: In principle, we could also specify style and behavior in the `index.html` file, but best practice is to keep them separate.

### Additional Resources
More in-depth tutorials of each of the languages and libraries used in this part can be found at w3schools:
* HTML (https://www.w3schools.com/html/)
* CSS (https://www.w3schools.com/css/)
* JavaScript (https://www.w3schools.com/js/)
* jQuery (https://www.w3schools.com/jquery/)
* Bootstrap (https://www.w3schools.com/bootstrap/)

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

## Database Configuration

When conducting an online experiment, we want to record a participant's behavior for latter analysis. In this part, you will learn how to use a mySQL database to store information from the experiment. Companion code for this part can be found in the directory `\db-tutorial-wrapper`. In order to store information in a mySQL database, you will need a mySQL username and password. Request this information from an admin if it hasn't already been provided. In addition, your admin will need to grant you access to the mySQL database 'website_tutorial'.

In this part of the tutorial, we will be introducing two additional programming languages. The first language is SQL, which is a language designed for querying a relational database such as mySQL. The second language is PHP, which we will use to send data between the client's machine and the server and vice versa.

### Data to Record

Before describing the new additions, let us first describe the data we want to save and the corresponding changes that have been made to existing code. During the experiment we will be passing three types of information to the database. First, when a participant starts the experiment we will record some basic information such as the time they started, which browser they are using (some issues are browser specific), and their IP address. Second, we will record information about every trial such as the start/end time of a trial and their particular response. Lastly, we will record when a participant has completed the experiment.

Initial information about a participant is recorded when the page finishes loading and is located in `index.html`. Using a new function `Get_User_System_Info()` included in `utils.js` we retrieve basic information about the user. The initial information is packaged up and posted to the server using a PHP file `initialize-assignment.php`.

During the actual experiment, data for each trial is sent to the sever using the PHP file `post-trial.php`. When a participant has completed the experiment, we update their initial information and indicate that they have completed the experiment using `update-assignment.php`. Both of these recording events are initiated by code in `AppController.js`.

In the configuration file, we have added an additional variable `doRecord`, which we can use to control whether information is sent to the database. When you are debugging your experiment, you will often want to set this variable to false so that you do not have to remove garbage data generated during debugging.

### The mySQL Database

A database has already been created for this tutorial. To login to the mySQL database, first login to the server and then execute the following command:
```script
mysql -u yourusername -p
```
You will be prompted for your password. After correctly entering your password you will now be logged into mySQL. The mySQL system is organized into different *databases*. To display all the accessible databases type:
```sql
SHOW DATABASES;
```
If you have been correctly added by your admin, you should see `website_tutorial` listed. While SQL commands and keywords are not case-sensitive, it is conventional to write all SQL commands and keywords in uppercase. Note that any names or variables you define in SQL *are* case-sensitive. Also note that an SQL command requires a semi-colon at the end of the command.

To open and use a particular database (e.g., the website_tutorial), execute:
```sql
USE website_tutorial;
```

Each database is composed of a number of *tables*. To list all the tables associated with a database, execute
```sql
SHOW TABLES;
```
You should see two tables `assignment` and 'trial'. We will use these two tables to store various information about the experiment. To see what type of information is stored in the `assignment` table execute:
 ```sql
 DESCRIBE assignment
 ```
To see everything that is currently stored in the `assignment` table, enter the following:
```sql
SELECT * FROM assignment;
```
Unless the database was recently purged, you should see data entries. For more complicated queries, do a web search for SQL query syntax.

Relational databases such as mySQL are organized in order to minimize redundancy of stored information. To help explain this concept, consider a bad way to store information. On each trial, we could store information about the user, the trial, and their response in one massive table. However, information about the user doesn't change across the experiment, so we would be storing the same information over and over again. Alternatively, we can use the relational approach and define two tables. The first table stores information about the user (`assignment`) and the second table stores information about each trial (`trial`). The tables are linked up in such a way that particular entries in the `trial` table correspond to particular entries in the `assignment` table. In other words, we reduce redundancy by defining relationships between the different table. Now user information is only stored once, reducing redundancy.

Although you do not have to create your own database for this tutorial, you will eventually need to create one for your own experiment. As an example, the code to create the database used in this tutorial is included below:
Create Database
```sql
CREATE DATABASE website_tutorial;
```
Open Database
```sql
USE website_tutorial;
```

Create `assignment` Table
```sql
CREATE TABLE assignment (
assignment_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
mturk_assignment_id VARCHAR(128) NOT NULL,
mturk_worker_id VARCHAR(128) NOT NULL,
mturk_hit_id VARCHAR(128) NOT NULL,
ipaddress VARCHAR(128) NOT NULL,
browser VARCHAR(128) NOT NULL,
platform VARCHAR(128) NOT NULL,
language VARCHAR(128) NOT NULL,
code_version VARCHAR(128) NOT NULL,
experiment_condition INT NOT NULL,
begin_hit VARCHAR(32) NOT NULL,
end_hit VARCHAR(32),
status VARCHAR(128) NOT NULL
);
```

Create `trial` Table
```sql
CREATE TABLE trial (
trial_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
assignment_id INT NOT NULL,
trial_no INT NOT NULL,
query_letter VARCHAR(32) NOT NULL,
submitted_letter VARCHAR(32) NOT NULL,
start_time_ms VARCHAR(32) NOT NULL,
end_time_ms VARCHAR(32),
FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id)
ON DELETE CASCADE
);
```
Relationships between tables are defined using the `FOREIGN KEY (somekey) REFERENCES sometable(somekey)` syntax.

### The PHP Files
Now that we have a database set up, we need to specify how information is sent to and retrieved from the database. In short, we will use PHP files to send and retrieve data. The central PHP file is `DatabaseConfiguration.php`. This file stores our mySQL credentials and indicates which mySQL database we will use. Our other PHP files will call this file in order to create a convenient PHP object. The remaining PHP files all establish a connection to the database and make appropriate SQL queries.

Other resources can be found that cover appropriate mySQL and PHP syntax. As usual, w3schools provides a good place to start (https://www.w3schools.com/php/php_mysql_intro.asp). However, two things are worth mentioning here. The PHP files provided in this tutorial follow best practice for protecting against *mySQL injection attacks*. Since the lab database is shared with other lab members it is very important that any code you write also sanitize input in order to protect against mySQL injection attacks. Second, PHP files can be tricky to debug since it can be difficult to generate useful error messages. The are tools that you can use to help generate useful error messages. However, the best advice when creating a new PHP file is to start simple and slowly build towards your goal.

### Your Own Version

If you would like to create your own version of this website to play around with and modify, do the following.
1. Make a copy of the `\db-tutorial-wrapper` directory.
2. Rename the *website directory* `\db-tutorial` by prefixing it with your user name (e.g., `\yourusername-db-tutorial`)
3. Change the website name in the deploy_website.py file
  * `website = 'yourusername-db-tutorial'`)
4. Modify the `_v0.config.py` configuration file.
  * Change the user name (e.g., `username = 'yourusername'`
  * Change the password to the appropriate password (e.g. `password = ‘yourpassword’`)
  * Change the website name (e.g., `website = ‘yourusername-db-tutorial’`)
5. Modify `DatabaseConfiguration.php`
  * Change the mysql username (e.g., `$this->username = "yourMysqlUsername";`);
  * Change the mysql password (e.g., ` $this->password = “yourMysqlPassword”;`)
6. Deploy the website by running `python3 deploy_website.py v0` from a terminal on your local machine while within the wrapper directory (`\db-tutorial-wrapper`).
7. If everything worked you should now be able to view the website at www.mozerlab.us/yourusername-db-tutorial.
8. Modify the code as you see fit and redeploy. If you want to try saving different data to a database, you will need to create your own database and update `$this->dbname = "your_new_db_name";` in `DatabaseConfiguration.php`.

## AMT Configuration
So far we have created a simple website hosted on a lab server that records participant data to mySQL database. The next step is to obtain participants for your experiment. One convenient platform for recruiting and paying participants is Amazon Mechanical Turk (AMT). This part of the tutorial will cover how the website we have created can be integrated with AMT. Companion code for this part can be found in the directory `\amt-tutorial-wrapper`. In order to integrate with AMT you will need Amazon Web Services (AWS) credentials (Access Key Id, Secret Access Key). These should be obtained from you admin.

### AMT Basics
In order to understand the changes we need to make to our website, we first need to discuss a few facets of AMT. On AMT, *requesters* publish jobs that they would like AMT *workers* to complete. AMT refers to a job as a Human Intelligence Task (HIT). When a requester publishes a HIT, they specify how many workers they would like to complete the HIT. On AMT, this is referred to as the number of *assignments* requested for a HIT. For our purposes, we will create one assignment for every participant we want to run in our experiment. It should now be clear why we previously named the first mySQL table `assignment`.

In principle, you could create one HIT with N assignments, where N is the total number of participants you want to run. However, AMT has a pricing structure that discourages this. For every assignment completed, Amazon takes a commission. If a HIT is composed of nine or fewer assignments, the commission is 20%. If the HIT is composed of ten or more assignments, the commission is 40%. In practice, we will break up our experiment into multiple HITs composed of no more than nine assignments in order to reduce the cost of running the experiment.

When you publish a HIT, it will be posted along with many other HITs that are currently available. Workers shop around for HITs that sound appealing and pay well. A worker can view an advertisement or preview of a HIT to help decide if it worth completing.

Once a worker accepts a HIT, one of two things will happen depending on the type of HIT accepted. AMT allows you to create two different types of HITs. In the first type of HIT, you use AMT pre-defined format in order gather information. The pre-defined formats are great for simple surveys and handful of other situations. For our experiment we want to use the second type of HIT: an *external question*. When creating an external question, we will redirect AMT workers from the AMT website to our own website. Once they have completed our experiment, we will then redirect them back to the AMT website.

In addition to these two different types of HITs, HITs can also be deployed on a live AMT site or a sandboxed AMT site. The live site (https://www.mturk.com/mturk/welcome) and sandbox site (https://workersandbox.mturk.com/mturk/welcome) of AMT look almost identical except for some color differences. In the live version, real money is involved. The sandbox website is not tied to real money and allows you to test to see if your website is appropriately hooked up to AMT.

### Expanded Configuration File
To handle the additional functionality, there are a bunch of new itms in the configuration file. The first thing to notice in the configuration file is that we need to specify a payment rate. In a real experiment, the payment rate will have received prior IRB approval. You should be very careful that this variable is set correctly. When an experiment goes live, you don't want to accidentally pay participants $100 rather than $10.

Next we have the dictionary variable `turkConfig`. The meaning of each variable in `turkConfig` is described below:
* `'live' : False` - Controls whether the HIT will be deployed on the live or sandbox AMT site. The current value is set to False and should not be changed for this silly experiment.
* `'questionUrl' : '%s/cgi-bin/turkserv.py' % (htdocsUrl)` - Tells AMT what webpage should be shown first.
* `'questionFrameHeight' : 600` - Tells AMT how tall the embedded consent form should be.
* `'hitTitle' : "Identify a letter as rapidly as possible."` - The title of the HIT that workers see.
* `'hitDescription' : 'Identify a letter as rapidly as possible.'` - The description of the HIT that workers see.
* `'hitKeywords' : "experiment, psychology"` - Keywords that help workers evaluate the HIT.
* `'hitDurationSec' :  1800` - How long workers have to complete the HIT. Since workers may accept a HIT and then complete it later, this should be longer rather than shorter. A good rule of thumb is give three times as much time as the experiment is designed to take.
* `'hitRewardDollar' : hitRewardDollar` - How much each participant is paid (this does not include AMT's fee).
* `'maxAssignments' : 1` - The number of assignments to create when the HIT is published. When going live for the first time, it is best to keep this as 1. If something goes wrong, it is better to have one upset person rather than many. You can always add more assignments using the online AMT console.
* `'awsAccessId' : 'AFAKEKEYAFAKEKEY',` - The first required AWS credential.
* `'awsSecretKey' : 'AFAKESECRETKEYAFAKESECRETKEY'` - The second required AWS credential.
* `'quals'` - A list of AMT qualifications. You can use predefined qualifications or create your own.

The qualifications included in this configuration file are commonly used in human subject experiments:
* `['NumberHitsApprovedRequirement', 'GreaterThanOrEqualTo', 100]` - Restricts the HIT to workers that have completed at least 100 approved HITs.
* '['PercentAssignmentsApprovedRequirement', 'GreaterThanOrEqualTo', 90]' - Restricts the HIT to workers that have a 90% approval rating. This can be relaxed some if want to deepen your potential subject pool.
* `['LocaleRequirement', 'EqualTo', 'US']` - Restricts the HIT to workers residing in the US. Depending on your IRB, you may be limited to running US subjects. Historically, AMT included workers from around the globe. However, new worker accounts can only be created if the workers reside in the US.  

You can create a custom qualification from the online AMT console. From the home page, select "Manage", then select "Qualification Types", then select "Create New Qualification Type". After filling out the form, a new qualification type will be created that has an unique ID. For example, let's say you only want participants to do your experiment once. After a participant completes your experiment, you could assign them your custom qualification ID. To add that custom qualification as a requirement for your experiment you would have something that now looks like the following:
```python
'quals' : 	[
    ['NumberHitsApprovedRequirement', 'GreaterThanOrEqualTo', 100],
    ['PercentAssignmentsApprovedRequirement', 'GreaterThanOrEqualTo', 90],
    ['LocaleRequirement', 'EqualTo', 'US'],
    ['Requirement', qualTypeId, 'DoesNotExist']
]
```
where `qualTypeId` is a python variable that has been assigned the string of your custom qualification ID.

Next in the configuration file we have the variable `submitUrl`. The submitUrl controls what happens when a participant finishes the experiment. If the experiment is live, we want to direct the submission data back to the live AMT site. If the experiment is not live, we want to direct the submission data to the sandbox AMT site.

The `submitUrl` and `expTimeMin` are included in the dictionary variable `expConfig` so that they are available client-side.

### Creating a HIT
Using the python script `create_hit.py`, a HIT is created similar to the way we deploy a website. To create a HIT, first make sure you have copied the latest version of the experiment to the server using `deploy_website.py'. Then execute the following command from the same directory level as `create_hit.py`:
```shell
python3 create_hit.py v0
```

In short, `create_hit.py` loads the specified configuration file and publishes a HIT on AMT (live or sandbox depending on the configuration file). The configuration file specifies `turkserv.py` as the first page to show to workers.

The file `turkserv.py ` serves two different pages. If a worker has not yet accepted the HIT, it serves `preview.html`. If the worker has accepted the HIT, `turkserv.py` serves `consent.html`. The html file `preview.html` acts as an advertisement and provides a very brief description of the experiment and requirements to participate. The file `consent.html` provides the full consent form. The bottom of `consent.html` includes a button that redirects the worker to `index.html` and then the actual experiment begins.

Due to the manner in which content is served to the AMT website, both 'preview.html' and 'consent.html' must also include any css styling relevant to the page.

The files 'preview.html' and 'consent.html' used in this tutorial were taken from an actual experiment and are included as examples.

### Redirect from AMT to External Question
When a participant agrees to the consent form, they are automatically redirected to the external website (in a new browser tab) and we append a worker ID, assignment ID and HIT ID to the URL. The information is taken from the url using the convenient QueryString library. This information is grabbed from the URL after we retrieve the configuration file. After grabbing this information, we fill out the form `id=mturk_form`, which is unseen to the participant. We will use this form at the end of the experiment to let AMT know that the external question was completed successfully. If a participant lands at the website without using AMT, the worker ID, HIT ID, and assignment ID will be "undefined".

### Redirect from External Question to AMT
Once a participant has completed the experiment, we need to let AMT know that the assignment was completed. To do so, we submit a form back to AMT using the url contained in `cfg.subitUrl`. The relevant submission code is contained in `appController.js`. The submission code is contained in the function that governs what happens when a user clicks the `#submit-button` button. If the submission is successful, the participant will end up back at the AMT page.

### Your Own Version
If you would like to create your own version of this website to play around with and modify, do the following.
1. Make a copy of the `\amt-tutorial-wrapper` directory.
2. Rename the *website directory* `\amt-tutorial` by prefixing it with your user name (e.g., `\yourusername-amt-tutorial`)
3. Change the website name in the `deploy_website.py` file.
  * `website = 'yourusername-amt-tutorial'`
4. Change the website name in the `create_hit.py` file.
  * `website = 'yourusername-amt-tutorial'`
4. Modify the `_v0.config.py` configuration file.
  * Change the user name (e.g., `username = 'yourusername'`
  * Change the password to the appropriate password (e.g. `password = ‘yourpassword’`)
  * Change the website name (e.g., `website = ‘yourusername-db-tutorial’`)
  * Change the AWS access id `awsAccessId`.
  * Change the AWS secret key `awsSecretKey`.
5. Modify `DatabaseConfiguration.php`
  * Change the mysql username (e.g., `$this->username = "yourMysqlUsername";`);
  * Change the mysql password (e.g., ` $this->password = “yourMysqlPassword”;`)
6. Deploy the website by running `python3 deploy_website.py v0` from a terminal on your local machine while within the wrapper directory (`\amt-tutorial-wrapper`).
6. Create a HIT using `python3 create_hit.py v0` from a terminal on your local machine while within the wrapper directory (`\amt-tutorial-wrapper`).
7. If everything worked you should now be able to view the website at www.mozerlab.us/yourusername-amt-tutorial and accept a HIT on the sandboxed AMT worker website.

### Managing Participants
When running an actual experiment, there are a number of things you may want to do.

#### Add Assignments
Once you have created a HIT you can add more assignments (up to nine). To do so, from the main requester page select "Manage", then "Manage HITs individually", find the HIT you want and click "Add assignments". You will only be able to add assignments if thre is still time remaining on the HIT.

#### Approve assignments
Once an assignment has been completed click "Manage", "Manage HITs individually", and then "Review assignments".

#### Compensate Bad HITs
Without fail a participant will eventually contact you regarding an issue with the HIT. Most often the issue is that they completed the experiment but AMT did not successfully receive the submission. This typically occurs because AMT will auto-log-out a worker or the worker submitted a HIT beyond the time allotted. In general, workers should always be compensated. It is very important to keep workers happy because there are a number of third-party websites that allow workers to rate requesters and word gets around. To compensate a worker, the best thing to do is create a dummy HIT that takes a few seconds to complete but pays the full amount of the original HIT. A dummy HIT can be created using AMT in-house survey template that asks a simple question (e.g., What's your favorite color?). When you create the dummy HIT, make sure that only workers with a custom qualification (that you create for this purpose) can see and accept the HIT. Then assign the qualification to the appropriate worker and revoke the qualification when they complete the dummy HIT.

When responding to the email of a worker, always give them the benefit of the doubt, unless you have a *very* good reason otherwise. I typically reply with an email using the following template with the `XXX` substituted in appropriately:
```
Hi XXX,

Thank you for accepting my HIT. I really appreciate your work. My apologies that it didn't successfully submit back to AmazonMechanical Turk. My records indicate that you have successfully completed the HIT.

I've created a fake HIT that only you can see. Regardless of your response to the fake HIT you will be paid.

Title: XXX Compensation HIT
Requester:  XXX

Let me know if you have any additional issues. Thank you again for accepting my HIT!

Regards,
XXX
```

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
