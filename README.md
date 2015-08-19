# ckanext-cadasta

In order to install the ckanext-cadasta extension, clone this repo into the src folder at /usr/lib/ckan/default/src

Then run the following command:
```
cd ckanext-cadasta
python setup.py develop
```

Add the cadasta plugin to your development file:
```
sudo vim /etc/ckan/default/development.ini
```
add "cadasta" to the list of ckan.plugins

1. edit config file /etc/ckan/default/development.ini so that your ip is correct.
2. start virtualenv 

    . /usr/lib/ckan/default/bin/activate
    
    cd /usr/lib/ckan/default/src/ckan
    
3. start ckan

    /usr/lib/ckan/default/bin/paster serve /etc/ckan/default/development.ini
