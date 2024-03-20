import _sqlite3

##connecting to the database sqllite

connection = _sqlite3.connect("eventdatabase.db")

#create a cursor obj to insert records,create table


cursor = connection.cursor()

#create the table

table_info = """Create table Event(NAME VARCHAR(25),DESCRIPTION VARCHAR(250),SECTION VARCHAR(25))"""

#to insert into a table

cursor.execute(table_info);

##inserting some records into the events table

cursor.execute('''
INSERT INTO Event (NAME, DESCRIPTION, SECTION) VALUES
('Conference 2024', 'Annual conference for professionals in the industry.', 'Business'),
('Tech Summit', 'Gathering of leading technologists to discuss innovations.', 'Technology'),
('Art Exhibition', 'Showcasing contemporary artworks from local artists.', 'Arts'),
('Startup Pitch', 'Competition for startups to pitch their ideas to investors.', 'Entrepreneurship'),
('Music Festival', 'Three-day festival featuring live performances from top artists.', 'Entertainment'),
('Science Fair', 'Showcasing student projects and experiments.', 'Education'),
('Charity Gala', 'Fundraising event for local charities and community projects.', 'Philanthropy'),
('Fashion Show', 'Showcasing the latest trends in fashion and design.', 'Fashion'),
('Food Expo', 'Exhibition of culinary delights and gourmet products.', 'Food & Beverage'),
('Health Summit', 'Conference focused on health and wellness topics.', 'Healthcare');
''')
print("The inserted Records are")
data = cursor.execute('''Select * from Event''')

for row in data:
    print(row)

#commiting the changes into the database
    
connection.commit()
connection.close()
