# Backend

# user Registration
=================================================================================<br>
POST :<br>
  http://127.0.0.1:8000/api/users/  <br>
  -> mandotary fields<br>
  
  data  = {
      1. username(EMPID)
      2. email(optional can be update later if not available)
      3. password
      4. confirm_password
      }
    
    <br>
    returns:
        {
          "id": 1,
          "username": "emp129",
          "email": "",
          "date_joined": "2020-02-29T09:26:42.056198Z",
          "token": "cf85d0ecbedd539a0f1817e05b7ad164e09"
         } <br>
      
     
# LogIn
=============================================================================================================<br>

POST:
<br>
http://127.0.0.1:8000/api/users/login/<br>
  -> mandatory fields<br>
    <br>
        data = {
            "username":"emp129",
            "password":"*******"
          }
        }
        <br>
    -> returns:
      {
        "auth_token": "cf85d0ecbedd539a0f1817e05b7ad164e09",
        "created": "2020-02-29T09:26:42.143937Z"
      }
  
  
  -> authorization key is important for further rest calls<br>
  
  #User_Info add<br>
 ==================================================================================================================
 
 POST:
    url : http://127.0.0.1:8000/api/users/add_info/<br>
    headers : <br>
            Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09<br>
            Content-Type:application/json<br>
    data:
            {
              "designation":"ASE",
              "project": "Project1",
              "gender": "male"
            }
            
            
   returns:<br>
          {
            "user": {
                "id": 2,
                "username": "emp129",
                "email": ""
            },
            "designation": "ASE",
            "project": "Project1",
            "doj": "2020-02-29T09:44:57.250165Z",
            "gender": "male"
        }
          
  
  #User_Info <br>
 ==================================================================================================================
 
 GET:<br>
    url : http://127.0.0.1:8000/api/users/add_info/<br>
    headers : <br>
            Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09<br>
            Content-Type:application/json<br>
            <br>
    
   -> Authorization Token decides the user info returned
            <br>
    returns:<br>
          {
            "user": {
                "id": 2,
                "username": "emp129",
                "email": ""
            },
            "designation": "ASE",
            "project": "Project1",
            "doj": "2020-02-29T09:44:57.250165Z",
            "gender": "male"
        }
  
  # get token
  =======================================================================================<br>
  
    GET:
		
		<br>
    url : http://127.0.0.1:8000/api/tokens/current/
    url : http://127.0.0.1:8000/api/tokens/cf85d0ecbedda128a539a0f1817e05b7ad164e09/
    
    -> we can use any of the two urls to get the token<br>
    
    headers : 
            Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09<br>
            Content-Type:application/json<br>
            <br>
            
    returns:
      {
        "auth_token": "cf85d0ecbedd539a0f1817e05b7ad164e09",
        "created": "2020-02-29T09:26:42.143937Z"
      }
    
 #Signout User<br>
========================================================================================================

    DELETE:
    
    url : http://127.0.0.1:8000/api/tokens/current
    url : http://127.0.0.1:8000/api/tokens/cf85d0ecbedda128a539a0f1817e05b7ad164e09
    
    headers : 
            Authorization:Token cf85d0ecbedda128a539a0f1817e05b7ad164e09
            <br>
    will delete the token of the user with current logged in 
    
    
 
 
    
    
    


  
