**create virtual env for the project**
```
#python3 -m <name_of_the_env> <location_of_the_env>
python3 -m venv ./venv

#activate the environment
source venv/bin/activate

#Install the dependencies
pip3 install -r requirement.txt
```

**Download the chrome driver by checking the chrome version in settings**
``` 
#change the permission of chrome driver using following command 
xattr -d com.apple.quarantine chromedriver
 ```

**create credentials.txt file in followig format**
```
<linkedin email_id>
<linkedin password>

```

**how to run**
```
#specify the chrome driver path in post_crawler.py and run 
python3 post_crawler.py

#specify the chrome driver path in profile_crawler.py and run 
python3 profile_crawler.py

```