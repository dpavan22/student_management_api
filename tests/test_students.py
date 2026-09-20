
def test_create_student_unauthorized(client):
    dummy_student = {
        'full_name' : "Test Student",
        'email' : 'teststudent@gmail.com',
        'age' : 20,
        'department' : 'Science',
        'roll_number' : "SCI123"
    
    }
    
    response = client.post("/students/" , json=dummy_student)
    assert response.status_code == 401

def test_create_student_authorized(client):
    login_response = client.post("/auth/register", json={'email': 'dummystudent@gmail.com',
                                                      'password' : 'dummy34535'})
    login_response = client.post('/auth/login', 
                                 data={'username' : 'dummystudent@gmail.com',
                                       'password' : 'dummy34535'})
    
    token = login_response.json()['access_token']
    
    dummy_student = { 
        'full_name' : "Authorized Student",
        'email': 'authstudent@gmail.com',
        'age': 22,
        'department' : 'Arts',
        'roll_number' : "ART24234"
        }
    response = client.post("/students/", json=dummy_student,
                           headers = {"Authorization" : f"Bearer {token}"})
    
    assert response.status_code == 201
    assert response.json()['full_name'] == "Authorized Student"
    

def test_get_all_students(client):
    response = client.get('/students/?skip=0&limit=5')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    