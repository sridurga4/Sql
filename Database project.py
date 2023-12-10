import sqlite3

# Connect to the SQLite database (creating it if it doesn't exist)
conn = sqlite3.connect('employee_project.db')
cursor = conn.cursor()

# Create Employee Information table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS EmployeeInformation (
        EmployeeID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        DateOfBirth DATE,
        Gender TEXT,
        ContactNumber TEXT,
        Address TEXT,
        DepartmentID INTEGER,
        HireDate DATE,
        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
    )
''')

# Create Project Details table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProjectDetails (
        ProjectID INTEGER PRIMARY KEY,
        DepartmentID INTEGER,
        ProjectName TEXT,
        ProjectDescription TEXT,
        StartDate DATE,
        EndDate DATE,
        Status TEXT,
        EmployeeID INTEGER,
        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID),
        FOREIGN KEY (EmployeeID) REFERENCES EmployeeInformation(EmployeeID)
    )
''')

# Create Department table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Department (
        DepartmentID INTEGER PRIMARY KEY,
        DepartmentName TEXT
    )
''')

# Create Health Providers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS HealthProviders (
        HealthProviderID INTEGER PRIMARY KEY,
        ProviderName TEXT,
        ProviderType TEXT,
        ContactNumber TEXT,
        Address TEXT,
        InsuranceCoverage TEXT,
        EmployeeID INTEGER,
        FOREIGN KEY (EmployeeID) REFERENCES EmployeeInformation(EmployeeID)
    )
''')

# Create Employee_Project_Assignment table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee_Project_Assignment (
        EmployeeID INTEGER,
        ProjectID INTEGER,
        FOREIGN KEY (EmployeeID) REFERENCES EmployeeInformation(EmployeeID),
        FOREIGN KEY (ProjectID) REFERENCES ProjectDetails(ProjectID)
    )
''')

# Create Employee_HealthProvider table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee_HealthProvider (
        Employee_ID INTEGER,
        HealthProvider_ID INTEGER,
        FOREIGN KEY (Employee_ID) REFERENCES EmployeeInformation(EmployeeID),
        FOREIGN KEY (HealthProvider_ID) REFERENCES HealthProviders(HealthProviderID)
    )
''')

# Insert sample data into Department table (using different IDs)
cursor.execute('''
    INSERT INTO Department (DepartmentID, DepartmentName)
    VALUES (1, 'IT'),
           (2, 'HR');
''')

# Insert sample data into EmployeeInformation table
cursor.execute('''
    INSERT INTO EmployeeInformation (FirstName, LastName, DateOfBirth, Gender, ContactNumber, Address, DepartmentID, HireDate)
    VALUES ('John', 'Doe', '1990-05-15', 'Male', '555-1234', '123 Oak St', 1, '2023-01-15'),
           ('Jane', 'Smith', '1985-08-22', 'Female', '555-5678', '456 Maple St', 2, '2023-02-01');
''')

# Insert sample data into ProjectDetails table
cursor.execute('''
    INSERT INTO ProjectDetails (DepartmentID, ProjectName, ProjectDescription, StartDate, EndDate, Status, EmployeeID)
    VALUES (1, 'Project A', 'Description A', '2023-01-01', '2023-12-31', 'Ongoing', 1),
           (2, 'Project B', 'Description B', '2023-02-01', '2023-11-30', 'Completed', 2);
''')

# Insert sample data into HealthProviders table
cursor.execute('''
    INSERT INTO HealthProviders (ProviderName, ProviderType, ContactNumber, Address, InsuranceCoverage, EmployeeID)
    VALUES ('City Hospital', 'Hospital', '123-456-7890', '123 Main St', 'Medical, Dental', 1),
           ('Community Clinic', 'Clinic', '987-654-3210', '456 Oak St', 'Health Checkups', 2);
''')

# Insert sample data into Employee_Project_Assignment table
cursor.execute('''
    INSERT INTO Employee_Project_Assignment (EmployeeID, ProjectID)
    VALUES (1, 1),
           (2, 2);
''')

# Insert sample data into Employee_HealthProvider table
cursor.execute('''
    INSERT INTO Employee_HealthProvider (Employee_ID, HealthProvider_ID)
    VALUES (1, 1),
           (2, 2);
''')

# Query to retrieve employees along with their project assignments
cursor.execute('''
    SELECT EmployeeInformation.FirstName, EmployeeInformation.LastName, ProjectDetails.ProjectName
    FROM EmployeeInformation
    JOIN Employee_Project_Assignment ON EmployeeInformation.EmployeeID = Employee_Project_Assignment.EmployeeID
    JOIN ProjectDetails ON Employee_Project_Assignment.ProjectID = ProjectDetails.ProjectID
''')
employee_project_assignments = cursor.fetchall()

# Display the results
print("\nEmployee Project Assignments:")
for assignment in employee_project_assignments:
    print(assignment)

# Query to retrieve employees along with their health providers
cursor.execute('''
    SELECT EmployeeInformation.FirstName, EmployeeInformation.LastName, HealthProviders.ProviderName
    FROM EmployeeInformation
    JOIN Employee_HealthProvider ON EmployeeInformation.EmployeeID = Employee_HealthProvider.Employee_ID
    JOIN HealthProviders ON Employee_HealthProvider.HealthProvider_ID = HealthProviders.HealthProviderID
''')
employee_health_providers = cursor.fetchall()

# Display the results
print("\nEmployee Health Providers:")
for provider in employee_health_providers:
    print(provider)

# Commit the changes and close the connection
conn.commit()
conn.close()
