# ckanext-cadasta

### Add extension to your installed CKAN instance (assumes you've installed CKAN already)
In order to install the ckanext-cadasta extension, clone this repo into the src folder at /usr/lib/ckan/default/src

###Cadasta Roles and Permissions
[See the permissions matrix for details](Permissions.md)

Then run the following command:
```
cd ckanext-cadasta
python setup.py develop
```

###Add the cadasta plugin to your development file:
```
sudo vim /etc/ckan/default/development.ini
```
add "cadasta" to the end of the list of ckan.plugins

also make sure that your ip is correct, especially if deploying to a non-localhost machine.

#Start CKAN Instance

###start virtualenv 

    . /usr/lib/ckan/default/bin/activate
    
    cd /usr/lib/ckan/default/src/ckan
    
###start ckan

    /usr/lib/ckan/default/bin/paster serve /etc/ckan/default/development.ini
