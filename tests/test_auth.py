
def test_register_user(client):
  response = client.post('/auth/register', json={'email': 'dummy23423@gmail.com', 'password': 'yourpassword4323'})
  assert response.status_code == 201
  assert response.json()['email'] == 'dummy@gmail.com'
  
  

def test_login_user(client):
    response = client.post('/auth/login', json={'username': 'dummy@gmail.com', 
                                                "password": 'yourpassword'})
    
    response = client.post('/auth/login', data={'username' : 'dummy@gmail.com',
                                                'password' : 'yourpassword'})
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    

    
    