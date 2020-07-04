# Backend

# please follow the calls as given below
# user registration:
#
  url : http://127.0.0.1:8000/api/users/
  method: post
  body: username, email,password, confirm_password
  Ex:
    {
    username:vishnuq
    email: example@example.com
    password:vishnu
    confirm_password:vishnu
    }
    
  response:
    {
    "id": 7,
    "username": "vishnuq",
    "email": "example@example.com",
    "date_joined": "2020-03-14T05:35:34.003323Z",
    "token": "0729d3936ab452080f43c082da08e735c1"
    }


# user login:

  url: http://127.0.0.1:8000/api/users/login/
  method: post
  headers: Content-Type:application/json
  body:
  {
  "username":"admin",
  "password":"admin"
  }
  
  response:
  {
    "username": "admin",
    "name": "Vishnuvardhan Nayakam",
    "project_id": "devops",
    "project": "devops",
    "premissions": {
        "viewer": false,
        "editor": false,
        "admin": false,
        "Manager": true
    },
    "Token": {
        "auth_token": "d33cad432193c4f4380999a85a75bd8f95785855",
        "created": "2020-03-03T17:08:47.890544Z"
      }
    }
  
  # signout
  
  
  url: http://127.0.0.1:8000/api/tokens/current/ or http://127.0.0.1:8000/api/tokens/$AUTH_TOKEN/
  method: delete
  headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
  
  responce:
  No respone, if status 2** means successful
  
  
    
 
 
 # Register users can have information which need to be utilised in shift and personal view so every registered user should have their own info it can be added by their own after logging else admin can add (but admin can add from only administration tool as of now)
 
 
 url: http://127.0.0.1:8000/api/users/user_info/ <br>
 method: post;
 <br>
 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 <br>
 body:
 
 {
	"designation":"ASE",
	"fullname": "Some Name",
	"project": "hr",
	"gender": "male",
	"permissions":"V"
}
<br>
if permissions field not given in body it will default gives permission 'V'
<br>

responce:

[
    {
        "user": {
            "id": 3,
            "username": "vishnuvardhan",
            "email": ""
        },
        "full_name": "v",
        "designation": "Software Engineer Trainee",
        "project_id": null,
        "project": "devops",
        "doj": "2020-03-03T16:49:10.201220Z",
        "gender": "male",
        "permissions": "M",
        "mobile_number": 8688272707,
        "total_exp": 10,
        "project_exp": 2,
        "img": "http://127.0.0.1:8000/media/empid/vishnuvardhan.jpg"
    }
]

<br>
#Note: Please use keyword based post request in order to get the robust results. default permission would be 'V' -> viewer, for managers it would be 'M' and for admins it would be "A"



# Retrive the user information after logging it is restricted to only authenticated user( for user profile info)

 url: http://127.0.0.1:8000/api/users/user_info/ <br>
 method: get;
 
 <br>
 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 
 <br>

responce:

[
    {
        "user": {
            "id": 3,
            "username": "vishnuvardhan",
            "email": ""
        },
        "full_name": "v",
        "designation": "Software Engineer Trainee",
        "project_id": null,
        "project": "devops",
        "doj": "2020-03-03T16:49:10.201220Z",
        "gender": "male",
        "permissions": "M",
        "mobile_number": 8688272707,
        "total_exp": 10,
        "project_exp": 2,
        "img": "http://127.0.0.1:8000/media/empid/vishnuvardhan.jpg"
    }
]





# UserInfo and Shift Info of 7 days from today

url: http://127.0.0.1:8000/api/users/user_info_shift_info/
<br>
method: get
<br>

 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 
<br>

responce:
<br>
{
    "user_info": {
        "user": {
            "id": 3,
            "username": "vishnuvardhan",
            "email": ""
        },
        "full_name": "v",
        "designation": "Software Engineer Trainee",
        "project_id": null,
        "project": "devops",
        "doj": "2020-03-03T16:49:10.201220Z",
        "gender": "male",
        "permissions": "M",
        "mobile_number": 8688272707,
        "total_exp": 10,
        "project_exp": 2,
        "img": "/media/empid/vishnuvardhan.jpg"
    },
    "shifts": [
        {
            "Date": "2020-06-18",
            "MorningShift": false,
            "AfternoonShift": false,
            "NightShift": false,
            "GeneralShift": true,
            "Leave": false
        },
        {
            "Date": "2020-06-18",
            "MorningShift": true,
            "AfternoonShift": false,
            "NightShift": false,
            "GeneralShift": false,
            "Leave": false
        }
    ]
}

<br>


# Persons info of shifts for particular date of mentioned dept.

url : http://127.0.0.1:8000/api/users/shift_details/<project_id>/dd/mm/yyyy
	
<br>
method: get
<br>

 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 
<br>
responce:
<br>

{
    "projectName": "devops",
    "date": "2020-06-08",
    "shifts": {
        "MorningShift": [
            "admin"
        ],
        "AfternoonShift": [],
        "NightShift": [],
        "GeneralShift": [],
        "Leave": []
    }
}
<br>


# Shift of a user on particular date

url : http://127.0.0.1:8000/api/users/<user_id>/dd/mm/yyyy

<br>
method: get
<br>

 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 
<br>
responce:
<br>

{
    "currentShift": "MorningShift"
}

<br>

# No of persons in a particular shift of mentioned dept

url : http://127.0.0.1:8000/api/users/<project_id>/<shift_name>/dd/mm/yyyy

<br>
method: get
<br>

 headers: { Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09 }
 
<br>
responce:
<br>

{
    "persons": [
        "admin"
    ]
}

<br>


#last1
