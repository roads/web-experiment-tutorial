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

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
