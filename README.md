# Pre-Election-Portal

### Major Tasks
* Front-End
* Display all Agendas
* Make Ask Me Anything Portal
* Display Election related stats

##### Front-End
* Design all the relevant web pages

##### Display all Agendas
* Display Agenda Cards for all the candidates.
* Allow filtering based on position candidates are contesting for.

##### Make Ask Me Anything Portal
* ~~Allow authenticated users to ask questions to the candidates.~~
* ~~Allow authenticated users to upvote/downvote questions asked by others.~~
* Allow authenticated users to comment on the answer given by the candidates.
* Questions and comments should be posted only after moderation by election commission.
* ~~Candidates must be able to see all the questions approved by Election Commission and answer them.~~

##### Display Election Related Stats
* Show ratio of votes casted to the no. of residents for each hostel during election
___

#### Install All Requirements

`sudo apt-get install postgresql postgresql-contrib`

`sudo apt-get install libpq-dev python3-dev`

`python3 -m pip install -r requirements.txt`
___

#### Set up Postgresql

###### Creating Database
`CREATE DATABASE db;`

###### Creating User
`CREATE USER admin WITH ENCRYPTED PASSWORD 'admin';`

###### Modifying Connection Parameters
`ALTER ROLE admin SET client_encoding TO 'utf8';`

`ALTER ROLE admin SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE admin SET timezone TO 'UTC';`

###### Granting Permission To The User
`GRANT ALL PRIVILEGES ON DATABASE db TO admin;`


###### Exiting Sql Prompt
`\q`


###### Updating Django to integrate
