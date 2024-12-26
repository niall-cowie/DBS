from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from .models import Person
from .models import Course
from .models import Tee_Time
from .models import Tee_Time_Group_Member
from django.template import Template, Context
from django.middleware.csrf import get_token
from django.http import HttpRequest

from .utils import set_isolation_level



from django.db import connection

def update_course_par(request):
    if request.method == 'POST':
        # Get course ID and new par from the form
        course_id = request.POST.get('course_id')
        new_par = request.POST.get('new_par')

        # Update the course par using a prepared statement
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    UPDATE Course
                    SET course_par = %s
                    WHERE course_id = %s
                """, [new_par, course_id])
            except Exception as e:
                return HttpResponse(f"Error occurred: {str(e)}", status=500)

        return HttpResponse("Course par updated successfully.")
    else:
        # If it's not a POST request, return an empty form
        return HttpResponse('''
            <form method="post">
                <label for="course_id">Course ID:</label>
                <input type="text" id="course_id" name="course_id"><br><br>
                <label for="new_par">New Par:</label>
                <input type="number" id="new_par" name="new_par"><br><br>
                <button type="submit">Update Course Par</button>
            </form>
        ''')
    
def is_golfer_in_database(first_name, last_name, age):
    
    with connection.cursor() as cursor:

        # Define the SQL query with placeholders for parameters
        sql = "SELECT COUNT(*) FROM Person WHERE first_name = %s AND last_name = %s AND age = %s"
        
        # Execute the prepared statement with parameters
        cursor.execute(sql, [first_name, last_name, age])
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if the golfer is in the database
        if result[0] > 0:
            return True  # Golfer is in the database
        else:
            return False  # Golfer is not in the database

def is_course_in_database(course_name, course_par):
    
    with connection.cursor() as cursor:
        # Define the SQL query with placeholders for parameters

        sql = "SELECT COUNT(*) FROM project_course WHERE course_name = %s AND course_par = %s"
        
        # Execute the prepared statement with parameters
        cursor.execute(sql, [course_name, course_par])
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if the course is in the database
        if result[0] > 0:
            return True  # Course is in the database
        else:
            return False  # Course is not in the database


# Create your views here.
def find_courses(request):
    # Logic for finding courses
    return redirect('/cs/find-courses/')  

def find_players(request):
    # Logic for finding players
    return redirect('/cs/find-players/')  

def show_player_directory(request):
    # Logic for showing player directory
    return redirect('/cs/player-directory/') 

def reserved_tee_times(request):
    # Logic for reserved tee times
    return redirect('/cs/tee-times/')  

def add_golfer(reqeust):
    return redirect('/cs/add_g/')

def add_course(reqeust):
    return redirect('/cs/add_c/')

def remove_golfer(request):
    return redirect('/cs/remove_g/')

def create_tee_time(request):
    return redirect('/cs/create_tee/')
def update_par(request):
    return redirect('/cs/par/')

def say_Hello(request):
    if request.method == 'POST':
        option = request.POST.get('options')
        if option == 'find_courses':
            return find_courses(request)
        elif option == 'find_players':
            return find_players(request)
        elif option == 'show_player_directory':
            return show_player_directory(request)
        elif option == 'reserved_tee_times':
            return reserved_tee_times(request)
        elif option == 'create_tee_time':
            return create_tee_time(request)
        elif option == 'add_golfer':
            return add_golfer(request)
        elif option == 'add_course':
            return add_course(request)
        elif option == 'remove golfer':
            return remove_golfer(request)
        elif option == 'update_course_par':
            return  update_par(request)
        else:
            return HttpResponse('Invalid option selected')
    else:
        # Define dropdown options
        dropdown_options = [
            ('find_courses', 'Find Courses'),
            ('find_players', 'Find Players'),
            ('show_player_directory', 'Show Player Directory'),
            ('reserved_tee_times', 'Reserved Tee Times'),
            ('add_golfer', 'Add a Golfer to the Registry'),
            ('add_course', 'Add a Course to the Registry'),
            ('remove golfer', 'Remove a Golfer from the Registry'),
            ('create_tee_time', 'Schedule a Tee Time'),
            ('update_course_par', 'Update Course Par'),
        ]

        # Generate HTML for the dropdown list
        dropdown_html = '<select name="options">'
        for option_key, option_label in dropdown_options:
            dropdown_html += f'<option value="{option_key}">{option_label}</option>'
        dropdown_html += '</select>'
        submit_button_html = '<input type="submit" value="Submit">'

        # Concatenate HTML for the form
        form_html = f'<form action="" method="post">{dropdown_html} {submit_button_html}</form>'
        print("HERE")

        # Return HTML response
        return HttpResponse(form_html)


def course_list(request):
    print("HERE2")


    
    unique_pars = Course.objects.values_list('course_par', flat=True).distinct()

    if request.method == 'GET' and 'par' in request.GET:
        par = request.GET['par']
        if par:
            courses = Course.objects.filter(course_par=par)
        else:
            courses = Course.objects.all()
    else:
        courses = Course.objects.all()

    # Get the CSRF token
    csrf_token = get_token(request)

    # Construct the HTML response directly in the view function
    html_template = """
    <html>
    <body>
        <form method='GET'>
            <label for='par'>Select Par:</label>
            <select id='par' name='par'>
            {% for par in unique_pars %}
                <option value='{{ par }}'>{{ par }}</option>
            {% endfor %}
            </select>
            <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
            <button type='submit'>Filter</button>
        </form>

        <h2>Filtered Courses</h2>
        <table border='1'>
            <tr><th>Course ID</th><th>Course Name</th><th>Par</th></tr>
            {% for course in courses %}
                <tr><td>{{ course.course_id }}</td><td>{{ course.course_name }}</td><td>{{ course.course_par }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    # Render the template with the provided context
    html_response = Template(html_template).render(Context({'unique_pars': unique_pars, 'courses': courses, 'csrf_token': csrf_token}))

    # Return the HTML response
    return HttpResponse(html_response)

def player_list_age(request):

    
    if request.method == 'POST':
        min_age = request.POST.get('min_age')
        max_age = request.POST.get('max_age')
        if min_age and max_age:
            players = Person.objects.filter(age__range=(min_age, max_age))
        else:
            players = Person.objects.all()
    else:
        players = Person.objects.all()
    
    # Construct the HTML response directly in the view function
    html_response = "<html><body>"
    html_response += "<h1>Players in Age Range</h1>"
    html_response += "<form method='post'>"
    html_response += "<label for='min_age'>Minimum Age:</label>"
    html_response += "<input type='number' id='min_age' name='min_age'>"
    html_response += "<label for='max_age'>Maximum Age:</label>"
    html_response += "<input type='number' id='max_age' name='max_age'>"
    html_response += "<button type='submit'>Filter</button>"
    html_response += "</form>"
    html_response += "<table border='1'>"
    html_response += "<tr><th>First Name</th><th>Last Name</th><th>Age</th></tr>"
    for player in players:
        html_response += f"<tr><td>{player.first_name}</td><td>{player.last_name}</td><td>{player.age}</td></tr>"
    html_response += "</table>"
    html_response += "</body></html>"

    # Return the HTML response
    return HttpResponse(html_response)


def player_direct(request):

    
    players = Person.objects.all()

    # Construct a dictionary to store the number of rounds played by each player
    player_rounds = {}
    for player in players:
        rounds_played = Tee_Time_Group_Member.objects.filter(participant=player).count()
        player_rounds[player] = rounds_played

    # Construct the HTML response
    html_response = "<html><body>"
    html_response += "<h1>Player Directory</h1>"
    html_response += "<table border='1'>"
    html_response += "<tr><th>Player</th><th>Rounds Played</th></tr>"
    for player, rounds_played in player_rounds.items():
        html_response += f"<tr><td>{player.first_name} {player.last_name}</td><td>{rounds_played}</td></tr>"
    html_response += "</table>"
    html_response += "</body></html>"

    # Return the HTML response
    return HttpResponse(html_response)

def tee_time_directory(request):  

         
    tee_times = Tee_Time.objects.all()

    # Construct the HTML response
    html_response = "<html><body>"
    html_response += "<h1>Tee Time Directory</h1>"
    
    for tee_time in tee_times:
        html_response += f"<h2>Date Time: {tee_time.tee_date_time}</h2>"
        html_response += f"<p>Course: {tee_time.course_id.course_name}</p>"
        html_response += "<p>Participants:</p>"
        participants = Tee_Time_Group_Member.objects.filter(tee_time=tee_time)
        if participants.exists():
            html_response += "<ul>"
            for participant in participants:
                html_response += f"<li>{participant.participant.first_name} {participant.participant.last_name}</li>"
            html_response += "</ul>"
        else:
            html_response += "<p>No participants</p>"
    
    html_response += "</body></html>"

    # Return the HTML response
    return HttpResponse(html_response)


def is_golfer_in_database(first_name, last_name, age):
        
    
    with connection.cursor() as cursor:

        # Define the SQL query with placeholders for parameters
        sql = "SELECT COUNT(*) FROM project_person WHERE first_name = %s AND last_name = %s AND age = %s"
        
        # Execute the prepared statement with parameters
        cursor.execute(sql, [first_name, last_name, age])
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if the golfer is in the database
        if result[0] > 0:
            return True  # Golfer is in the database
        else:
            return False  # Golfer is not in the database

def add_person(request):

    
    if request.method == 'POST':
        # Get user input from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')

        # Check if the person already exists in the table
        if is_golfer_in_database(first_name, last_name, age):
            return HttpResponse('Person already exists in the table!')
        else:
            # If the person doesn't exist, add them to the table
            person = Person(first_name=first_name, last_name=last_name, age=age)
            person.save()
            return HttpResponse('Person added successfully!')
    else:
        # Return the HTML form for user input
        return HttpResponse('''
            <form method="post">
                <label for="first_name">First Name:</label>
                <input type="text" id="first_name" name="first_name"><br><br>
                <label for="last_name">Last Name:</label>
                <input type="text" id="last_name" name="last_name"><br><br>
                <label for="age">Age:</label>
                <input type="number" id="age" name="age"><br><br>
                <button type="submit">Add Person</button>
            </form>
        ''')


def add_golf_course(request):

    
    if request.method == 'POST':
        # Get user input from the form
        course_name = request.POST.get('course_name')
        course_par = request.POST.get('course_par')

        # Check if the course already exists in the table
        if is_course_in_database(course_name, course_par):
            return HttpResponse('Course already exists in the table!')
        else:
            # If the course doesn't exist, add it to the table
            course = Course(course_name=course_name, course_par=course_par)
            course.save()
            return HttpResponse('Course added successfully!')
    else:
        # Return the HTML form for user input
        return HttpResponse('''
            <form method="post">
                <label for="course_name">Course Name:</label>
                <input type="text" id="course_name" name="course_name"><br><br>
                <label for="course_par">Course Par:</label>
                <input type="number" id="course_par" name="course_par"><br><br>
                <button type="submit">Add Course</button>
            </form>
        ''')
    

def remove_course(request):

    if request.method == 'POST':
        # Get the selected course's ID from the form
        course_id = request.POST.get('course_id')

        try:
            # Retrieve the course from the database
            course = Course.objects.get(course_id=course_id)

            # Remove the course from the database
            course.delete()

            # Return a success message
            return HttpResponse("Course removed successfully.")
        except Course.DoesNotExist:
            # Return an error message if the course doesn't exist
            return HttpResponse("Course does not exist in the database.")
    else:
        # Retrieve the list of courses from the database
        courses = Course.objects.all()

        # Construct the HTML response with the list of courses and removal options
        html_response = """
        <h1>List of Courses</h1>
        <form method="post">
            <label for="course_select">Select Course to Remove:</label>
            <select id="course_select" name="course_id">
        """

        for course in courses:
            html_response += f"<option value='{course.course_id}'>{course.course_name}</option>"

        html_response += """
            </select><br><br>
            <button type="submit">Remove Course</button>
        </form>
        """

        return HttpResponse(html_response)
    

def delete_golf_player(request):

    
    if request.method == 'POST':
        # Get the golfer's information from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')

        # Check if the golfer exists in the database
        if is_golfer_in_database(first_name, last_name, age):
            # Remove the golfer from the related tables
            remove_golfer_from_tables(first_name, last_name, age)
            return HttpResponse("Golfer removed successfully.")
        else:
            return HttpResponse("Golfer does not exist in the database.")
    else:
        # Render the template with the form
        return HttpResponse('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Remove Golfer</title>
        </head>
        <body>
            <h1>Remove Golfer</h1>
            <form method="post">
                <label for="first_name">First Name:</label><br>
                <input type="text" id="first_name" name="first_name"><br>
                <label for="last_name">Last Name:</label><br>
                <input type="text" id="last_name" name="last_name"><br>
                <label for="age">Age:</label><br>
                <input type="text" id="age" name="age"><br><br>
                <input type="submit" value="Remove Golfer">
            </form>
        </body>
        </html>
        ''')

def is_golfer_in_database(first_name, last_name, age):
    
    with connection.cursor() as cursor:
        # Define the SQL query with placeholders for parameters
        sql = "SELECT COUNT(*) FROM project_person WHERE first_name = %s AND last_name = %s AND age = %s"
        
        # Execute the prepared statement with parameters
        cursor.execute(sql, [first_name, last_name, age])
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if the golfer is in the database
        if result[0] > 0:
            return True  # Golfer is in the database
        else:
            return False  # Golfer is not in the database

def remove_golfer_from_tables(first_name, last_name, age):


    # Delete the golfer from the Person table
    
    Person.objects.filter(first_name=first_name, last_name=last_name, age=age).delete()

    # Remove the golfer from the Tee_Time_Group_Member table and decrease the group size of affected tee times
    Tee_Time_Group_Member.objects.filter(participant__first_name=first_name, 
                                         participant__last_name=last_name, 
                                         participant__age=age).delete()

    # Update group size for affected tee times
    affected_tee_times = Tee_Time_Group_Member.objects.filter(participant__first_name=first_name, 
                                                              participant__last_name=last_name, 
                                                              participant__age=age)
    for tee_time_group_member in affected_tee_times:
        tee_time = tee_time_group_member.tee_time
        tee_time.group_size -= 1
        tee_time.save()
        if tee_time.group_size == 0:
            tee_time.delete()


def create_tee_time_web(request):

    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        tee_date_time = request.POST.get('tee_date_time')
        golfer_ids = request.POST.getlist('golfers')

        # Create the tee time
        tee_time = Tee_Time.objects.create(course_id_id=course_id, tee_date_time=tee_date_time, group_size=len(golfer_ids))

        # Add golfers to the tee time
        for golfer_id in golfer_ids:
            golfer = Person.objects.get(pk=golfer_id)
            Tee_Time_Group_Member.objects.create(tee_time=tee_time, participant=golfer)

        return HttpResponse("Tee Time created successfully.")
    else:
        courses = Course.objects.all()
        golfers = Person.objects.all()
        
        # Render HTML form
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Create Tee Time</title>
        </head>
        <body>
            <h1>Create Tee Time</h1>
            <form method="post">
                <label for="course_id">Select Course:</label><br>
                <select id="course_id" name="course_id">
        '''
        
        # Add options for courses
        for course in courses:
            html += f'<option value="{course.course_id}">{course.course_name}</option>'
        
        html += '''
                </select><br><br>
                <label for="golfers">Select Golfers:</label><br>
        '''
        
        # Add checkboxes for golfers
        for golfer in golfers:
            html += f'''
            <input type="checkbox" id="golfer_{golfer.member_id}" name="golfers" value="{golfer.member_id}">
            <label for="golfer_{golfer.member_id}">{golfer.first_name} {golfer.last_name}</label><br>
            '''
        
        html += '''
                <br>
                <label for="tee_date_time">Tee Date Time:</label><br>
                <input type="datetime-local" id="tee_date_time" name="tee_date_time"><br><br>
                <button type="submit">Create Tee Time</button>
            </form>
        </body>
        </html>
        '''
        
        return HttpResponse(html)
    
def update_course_par_web(request):
    
    if request.method == 'POST':
        # Get selected course ID and new par from the form
        course_id = request.POST.get('course_id')
        new_par = request.POST.get('new_par')

        # Update the course par using a prepared statement
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    UPDATE project_course
                    SET course_par = %s
                    WHERE course_id = %s
                """, [new_par, course_id])
            except Exception as e:
                return HttpResponse(f"Error occurred: {str(e)}", status=500)

        return HttpResponse("Course par updated successfully.")
    else:
        # Retrieve all courses from the database
        courses = Course.objects.all()
        
        # Render HTML form with dropdown menu for course selection
        html = '''
            <form method="post">
                <label for="course_id">Select Course:</label><br>
                <select id="course_id" name="course_id">
        '''
        
        # Add options for courses
        for course in courses:
            html += f'<option value="{course.course_id}">{course.course_name}</option>'
        
        html += '''
                </select><br><br>
                <label for="new_par">New Par:</label>
                <input type="number" id="new_par" name="new_par"><br><br>
                <button type="submit">Update Course Par</button>
            </form>
        '''
        
        return HttpResponse(html)
