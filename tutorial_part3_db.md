## Database Configuration

When conducting an online experiment, we want to record a participant's behavior for latter analysis. In this part, you will learn how to use a mySQL database to store information from the experiment. Companion code for this part can be found in the directory `\db-tutorial-wrapper`. In order to store information in a mySQL database, you will need a mySQL username and password. Request this information from an admin if it hasn't already been provided. In addition, your admin will need to grant you access to the mySQL database 'website_tutorial'.

In this part of the tutorial, we will be introducing two additional programming languages. The first language is SQL, which is a language designed for querying a relational database such as mySQL. The second language is PHP, which we will use to send data between the client's machine and the server and vice versa.

### Data to Record

Before describing the new additions, let us first describe the data we want to save and the corresponding changes that have been made to existing code. During the experiment we will be passing three types of information to the database. First, when a participant starts the experiment we will record some basic information such as the time they started, which browser they are using (some issues are browser specific), and their IP address. Second, we will record information about every trial such as the start/end time of a trial and their particular response. Lastly, we will record when a participant has completed the experiment.

Initial information about a participant is recorded when the page finishes loading and is located in `index.html`. Using a new function `Get_User_System_Info()` included in `utils.js` we retrieve basic information about the user. The initial information is packaged up and posted to the server using a PHP file `initialize-assignment.php`.

During the actual experiment, data for each trial is sent to the sever using the PHP file `post-trial.php`. When a participant has completed the experiment, we update their initial information and indicate that they have completed the experiment using `update-assignment.php`. Both of these recording events are initiated by code in `AppController.js`.

In the configuration file, we have added an additional variable `doRecord`, which we can use to control whether information is sent to the database. When you are debugging your experiment, you will often want to set this variable to false so that you do not have to remove garbage data generated during debugging.

### The mySQL Database

A database may need to be created for you by your server admin. To login to the mySQL database, first login to the server and then execute the following command:
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
Unless the database was recently created or purged, you should see data entries. For more complicated queries, do a web search for SQL query syntax.

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
  * Change the ipaddr to the appropriate IP address of your server
  * Change the website name (e.g., `website = ‘yourusername-db-tutorial’`)
  * Change the htdocsUrl to the actual URL of your server. AMT requires https to run external HITS.
5. Modify `DatabaseConfiguration.php`
  * Change the mysql username (e.g., `$this->username = "yourMysqlUsername";`);
  * Change the mysql password (e.g., ` $this->password = “yourMysqlPassword”;`)
6. Deploy the website by running `python deploy_website.py v0` from a terminal on your local machine while within the wrapper directory (`\db-tutorial-wrapper`).
7. If everything worked you should now be able to view the website at www.mozerlab.us/yourusername-db-tutorial.
8. Modify the code as you see fit and redeploy. If you want to try saving different data to a database, you will need to create your own database and update `$this->dbname = "your_new_db_name";` in `DatabaseConfiguration.php`.
