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
