# UB-Teaching-Helpers
Repo to hold tools to make teaching a little easier

# Usage  
Program is set to take in either a quiz repo or lab repo or both  

If only  a quiz or lab repo is present it will check that out  
ELSE:  
We will look at user's current time and give quiz if < 30 mins in recitation  

## Config  
Script is based off of the config file.  
Use the `template.json` file as a base and rename it to `config.json` before releasing  
  
Section repo list MUST be organized in the order the repos appear in order to work properly.  

## Setup and deployment  
If you look in the code the code references a class list and a section time  
  
In order for security you will need to use the 2 script to pickle your class list in format `username,section`  
As well as pickle your sections in the form of `section_name,day,start_hour,end_hour,am_or_pm`  
  
In section list the day must be formatted as  
  
  M = Monday  
  T = Tuesday  
  W = Wednesday  
  Th = Thursday  
  F = Friday  
  S = Saturday  
  Su = Sunday  
  
When specifying am or pm just put `A` for am and `P` for pm 
  
### Deployment  
Put all pickled objects as well as the config and script in the same folder in a central location  
Students will be able to call the script with python3 and it will run from the central location
