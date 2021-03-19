Instructions for setting up the project:

1. download the zip 
2. create a new directory and place the zip into this directory
3. open terminal and navigate to the created directory
4. create a virtual environment 
        python3 -m venv env
5. enter env directory
        cd env
6. activate virtual environment
        source bin/activate
7. install flask
        pip install flask
8. deactivate virtual environment
        deactivate
9. navigate back to the original directory
        cd ..
10. navigate to the directory created from the zip
        cd <<name of directory>>
11. instal mysql client and flask-mysql
        pip install mysqlclient
        pip install flask-mysql
12. go into the app.py file and adjust the configurations to match your sql connection
13. start the server
        python app.py
