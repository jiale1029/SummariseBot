# SummariseBot for Telegram

## Overview
The SummariseBot is a bot that can be used to summarise the chats in the app - Telegram.

## Getting Started
These instructions will get the bot running on your local machine with your own bot token.

### Installation
Prerequisites
* Have pip installed on your machine.
* Have MySQL installed on your machine.
* Your own bot token from botfather.

Modules Required
* MySQLdb
* networkx
* sklearn
* numpy
* scipy
* telepot
* nltk

In order to install the above mentioned modules, type
```
pip install modules      e.g. pip install networkx
```
### Creating a Database

First, login to your mysql and type in your password. Type the following lines in your command line.

```
mysql -u username -p
```
Next, create a database.

```
mysql> CREATE DATABASE ChatDB;
```
#### Showing the database

Then, in order to show the database is successfully created, type the following lines.

```
mysql> SHOW DATABASES;
```
You will see the database you just created in the console.

#### Creating a table

Next, create a table named content and two columns which are chat_id and messages to store our chat_id and messages into the database.

```
mysql> use ChatDB;
mysql> CREATE TABLE content (chat_id LONGTEXT(4294967295), messages LONGTEXT(4294967295));
```

A database named ChatDB is successfully created.

#### Viewing the data you collected

```
mysql> SELECT chat_id, messages FROM content;
```

### Setting up the bot

#### Changing the token

Open main1.py using a texteditor or even python IDLE. Change the token to your own.

```
bot = telepot.Bot("Token")
```

#### Changing the database information.

Open chatdb.py. Change the information into your own.

```
self.conn = MySQLdb.connect("IP/localhost", "mysqlusername", "password", "databasename(CASE-SENSITIVE)")




