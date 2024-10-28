# Configuration of this project

This document will detail the configuration requirements needed to run this project which are contained in a `config.ini`.

## Create `config.ini`
1. Copy `blank_config.ini`
2. Rename the copied `blank_config.ini` `config.ini`
3. Ensure that `config.ini` is in your `.gitignore` file if there is a chance you may commit it.
4. Populate the values as per below

## GITHUB.INTERACTION Section
This section covers the interaction with GitHub for graphQL.
### token
- This should be an appropriate GitHub user token, user will need appropriate levels of admin rights in the organisation.
- At present this should be a classic token with repo, admin:org, and project permissions.

### org_name
- This is the name of the organisation to use
- This has been parameterised for ease of reuse of the code in the future

### user_name
- This should be the GitHub username of the user for whom the token was created

### webhook_secret
- This should match the secret used when setting up the app on GitHub

## WWW.INTERACTION Section
This section is the values to use for linking the web server to the web

### host
This is the IP address to use as the host for this website, this will likely map to a web address elsewhere

### port
This is the port that is open to the web on the computer it is installed on
