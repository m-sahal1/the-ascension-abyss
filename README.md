# Elevator-problem

The elevator system is built completely from the user perspective. There are elevator systems(Equivalent to buildings) that contains some elevators. Now some user comes in and makes a request to an elevator. The elevator automatically moves UP/DOWN as per the request of the user.The elevator's algorithm to process the requests can be optimized further. The status of an elevator like it is currently operational or not can be updated using API calls.
## Assumptions:
Number of elevators in the system will be defined by the API to intialise the elevator system
Elevator System has got only one button per floor.
So if there are a total of 5 floors, there will be 5 buttons per floor.
Note that, this doesn't not mimic real world, when you would have a total of 10 buttons for 5 floors ( one for up and one for down)
Once the elevator reaches its called point, then based on what floor is requested, it moves either up or down.
Assume the API calls which make the elevator go up/down or stop will reflect immediately. When the API to go up is called, you can assume that the elevator has already reached the above floor. 
The system has to assign the most optimal elevator to the user according to their request.
##Installation :
Make a python virtual enviornment in virtualenv venv python
refer to: ```https://www.geeksforgeeks.org/python-virtual-environment/```
Clone the repository and navigate to the directory where the manage.py file is located
```git clone https://github.com/m-sahal1/the-ascension-abyss.git
cd Elevator-problem```
Install the requirements
```pip install -r requirements.txt```
Run the development server
```python manage.py runserver```
## Usage

1. View all elevator systems
    - Endpoint: ```GET  /api/system/all```


2. Create a new elevator system
    - Endpoint: ```POST/api/system/add-new/```
        - Request body:
    ```json
    {
        "building_name": "Homeland",
        "total_floors": 2,
        "total_elevators": 6
    }
    ```
    
3. View All elevators under an elevator system
    - Endpoint: ```GET  /api/system/{system_id}/```

  ## Elevator
Elevator object model. Represents a single elevator that can move up and down. It is always a part of an entire elevator system. So elevator system is assigned as foreignkey.
### GET api/system/<int:id>/
Given an elevator system list all the elevators and their status.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
```

#### Response Example
```
200
[
  {
    "id": 0,
    "elevator_number": 0,
    "current_floor": 0,
    "operational": true,
    "door": true,
    "status": "open",
    "elevator_system": 0
  }
]

```

### GET api/system/{elevator-system-id}/elevator/{elevator-number}/view/
Get details of a specific elevator, given its elevator system id and elevator number with URL

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```

### PUT/PATCH api/system/{elevator-system-id}/elevator/{elevator-number}/update/
Update details of a specific elevator, given its elevator system and elevator number with URL It can be done together with prev view

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
elevator_number   - required integer (Elevator number)
current_floor	    - integer (Current floor)
operational	  - boolean (Is operational)
door	    - "open" or "close"
status	  - "moving_up","moving_down" or "idle"
elevator_system   - required integer (Elevator system)
```
#### Response Example
```
200

  {
    "id": 0,
    "elevator_number": 0,
    "current_floor": 0,
    "operational": true,
    "door": true,
    "status": "open",
    "elevator_system": 0
  }

```

### GET api/system/{elevator-system-id}/elevator/{elevator-number}/destination/
Fetch the next destination floor for a given elevator

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```


## Elevator Request
User request targeted to a specific elevator.

### GET api/system/{elevator-system-id}/elevator/{elevator-number}/req/view/
List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Params
```
is_active ----> False/0 ---> All the processed requests by the elevator(False is case insensitive)
is_active ----> True/1 ---> All the pending requests by the elevator(True is case insensitive)
```
#### Response Example
```
200
[
  {
    "id": 0,
    "requested_floor": 0,
    "destination_floor": 0,
    "request_time": "2019-08-24T14:15:22Z",
    "is_active": true,
    "elevator": 0
  }
]
```
### POST api/system/{elevator-system-id}/elevator/{elevator-number}/req/add-new/
Create a new request for a specific elevator, given its elevator system and elevator number with URL. The inputs of requested and destinatiom floor is sent with the form-data.

#### Path Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
requested_floor       - required integer 
destination_floor	    - required integer
```
#### Response Example
```
201
{
  "requested_floor": 0,
  "destination_floor": 0
}
```
##What was your motivation? 
The motivation behind building this project was to implement a simplified elevator model using Python and Django. The challenge provided an opportunity to develop the business logic for an elevator system that can handle elevator movements, floor requests, elevator states, and other related functionalities. By tackling this project, the aim was to improve programming skills, particularly in Python and Django, and gain a better understanding of designing and implementing an elevator system.

##Why did you build this project? 
The project was built to demonstrate proficiency in Python and Django, specifically using the Django Rest Framework. It allowed for the application of object-oriented programming principles, software design patterns, and API development. By creating the elevator system, it was possible to showcase the ability to handle complex logic and decision-making processes required for elevator movements.

##What problem does it solve? 
The project solves the problem of simulating a simplified elevator system. While ignoring real-world complexities and optimizations, it focuses on making decisions about elevator movements (up, down, or stop) based on user requests. The elevator system assigns the most optimal elevator to handle the user's request and maintains the elevator states accordingly. By implementing this project, it becomes possible to understand the core logic and functionality required for an elevator system and explore the challenges involved in designing such systems.

##What did you learn? 
Through this project, several key learnings were obtained:
Improved proficiency in Python and Django, including the use of Django Rest Framework.
Knowledge of API development using Django, including the use of ViewSets and Serializers.
Consideration of edge cases and thorough testing to ensure the system functions as expected.
Ability to communicate design decisions, API contracts, and setup instructions effectively through a well-structured README.md file.
##Note :
The code is repetitive in some cases as I have used each view only for one type of HTTP Method to provide a better understanding.
Redis caching is done for the entire site with a time limit of 5 minutes, so if you update the DB the changes in a cached device will appear 5 minutes later.
Please make sure redis is installed and running in your device. If it is running in a different port than 6379 then please go to Elevator/Settings.py and update it at line number : 158.
The elevator is running in a different thread and processes all the requests immediately. Check core/move_elevator.py and core/apps.py to know more details.
sqlite3 DB is used for portability in GitHub. 

