from flask import Flask
from flask import request
 
#you should have previously installed flask_mysqldb
#pip install flask_mysqldb
from flask_mysqldb import MySQL
from sshtunnel import SSHTunnelForwarder
 
app = Flask(__name__ )
    
    #creates instance db of class mysql.connector
    #connects to the database with the credentials given in the document through a SSH Tunnel
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'votes'
mysql = MySQL(app)
 


 
#this function is called to generate the home page of your website
@app.route('/')
def index():
    #htmlCode is some text
    htmlCode = "Hello EVERY ONE =)"
    htmlCode += "<br>"
    htmlCode += "<a href='/'>Homepage</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/list'>List</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/add'>Add</a>"
    htmlCode += "<br>"
	#this text is returned
    return htmlCode
 
@app.route('/list')
def list():
	
    
	#you must create a Cursor object
	#it will let you execute the needed query
    cur = mysql.connection.cursor()
 
	#you must complete the below SQL select query 
    cur.execute("SELECT * FROM campus ;")
    mysql.connection.commit()
    
    htmlCode = "Menu"
    htmlCode += "<br>"
    htmlCode += "<a href='/'>Homepage</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/list'>List</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/add'>Add</a>"
    htmlCode += "<br>"
    
    htmlCode += "<ol>"
	
	#print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
           	
        htmlCode += "<li>"
        htmlCode += str(row[1])
        htmlCode += "</li>"
	
    htmlCode += "</ol>"
    cur.close()
    return htmlCode

#we use this route twice: first method to display a form
@app.route('/add')
def add():

    
    htmlCode = "Menu"
    htmlCode += "<br>"
    htmlCode += "<a href='/'>Homepage</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/list'>List</a>"
    htmlCode += "<br>"
    htmlCode += "<a href='/add'>Add</a>"
    htmlCode += "<br>"
    
    htmlCode += "<ol>"
	
    
	#you must create a Cursor object
	#it will let you execute the needed query
    cur = mysql.connection.cursor()
 
	#you must complete the below SQL select query 
    cur.execute("SELECT * FROM campus;")
    mysql.connection.commit()
        

#start a form to let user enter data
    htmlCode += "<br>"
    htmlCode += "Enter yor email Address for authentification"
    htmlCode += "<br>"
    htmlCode += "<form action='addsave' method='GET''>"
	#start a form to let user enter data
	#action is the route/page called when the form is submitted
	#method indicates how the information is submitted to the other page (GET means through the URL)
	#observe the URL in your browser after submit, it will look like
	#http://127.0.0.1:5000/addsave?student=name%40icam.fr&choice=1
	#the first parameter starts with ?
	#then we have parameter1=value1
	#the second (or any subsequent parameter) starts with &
	#then we have parameter2=value2
    htmlCode += "<label>Email Address:</label>"
    htmlCode += "<br>"
	#we a have an input field of type email for the student identifier (required)
    htmlCode += "<input type='email' name='student' required>"
    htmlCode += "<br>"
    	
    htmlCode += "<label>Which Group Won Group A or Group B:</label>"
    htmlCode += "<br>"
	#we use a drop down list to select a campus
    htmlCode += "<select name='choice'>"
	
	#print the first cell (or column) of all rows (or records)
    for row in cur.fetchall():
    		#for each campus, we create an <option value=id>name</option>   	
        htmlCode += "<option value=" + str(row[0]) +">"
        htmlCode += str(row[1])
        htmlCode += "</option>"
	
	#we close the select tag
    htmlCode += "</select>"
    	
	#at the end of the form, we display a button to save the record
    htmlCode += "<br>"
    htmlCode += "<input type='submit' value='Save'>"
	#close form
    htmlCode += "</form>" 
    
    cur.execute("SELECT COUNT(Campus_idCampus) FROM `mobilitywish` WHERE Campus_idCampus = 3;")
    for row in cur.fetchall():
    		#for each campus, we create an <option value=id>name</option>
        htmlCode += "<br>"
        htmlCode += "Number of people that Chosed group 1 equals" 
        htmlCode += "</br>"
        htmlCode += "<br>"  	
        htmlCode += str(row[0])
        htmlCode += "</br>"
    
    cur.execute("SELECT COUNT(Campus_idCampus) FROM `mobilitywish` WHERE Campus_idCampus = 1;")
    for row in cur.fetchall():
    		#for each campus, we create an <option value=id>name</option>
        htmlCode += "<br>"
        htmlCode += "Number of people that Chosed group 2 equals" 
        htmlCode += "</br>"
        htmlCode += "<br>"  	
        htmlCode += str(row[0])
        htmlCode += "</br>"
        
    
    cur.close()
    return htmlCode 

@app.route('/addsave',  methods=['GET'])
def addsave():
	htmlCode = "Menu"
	htmlCode += "<br>"
	htmlCode += "<a href='/'>Homepage</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/list'>List</a>"
	htmlCode += "<br>"
	htmlCode += "<a href='/add'>Add</a>"
	htmlCode += "<br>"
 
    #you must create a Cursor object
	#it will let you execute the needed query
	cur = mysql.connection.cursor()
	
	#MobilityWish is the table
	#Campus_idCampus and studentMail are the fields in the table
	#SQL syntax is INSERT INTO table(field1, field2) VALUES('value1', 'value2')  
	sql = "INSERT INTO MobilityWish(studentMail, Campus_idCampus) VALUES (%s, %s)"
	#request.values['choice'] and request.values['student'] are input from the form by user
	val = (request.values['student'], request.values['choice'])
	#we execute an insert query
	cur.execute(sql, val)
    
 
	#commit = save changes in database
	mysql.connection.commit() 
 
 
	 #display the number of records added
	htmlCode += str(cur.rowcount) + " record inserted." 
 
	#display the values you are about to insert
	#request.values['choice'] and request.values['student'] are the values from the form inputs
	htmlCode +="<P>Student is: "+ request.values['student'] + "<br>";
	htmlCode +="Choice is: " + request.values['choice'] + "</P>";
    
    

	return htmlCode
  	
 
#make sure these 2 main lines remain at the end of the code
if __name__ == '__main__':
	app.run()

