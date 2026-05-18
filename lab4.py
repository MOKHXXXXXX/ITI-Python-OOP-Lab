import json
import re

MOODS = ("happy", "tired", "lazy")


class Person:
    def __init__(self, name, money, mood, healthRate):
        self.name = name
        self.money = money
        self.mood = mood
        self.healthRate = healthRate  

    @property
    def healthRate(self):
        return self._healthRate

    @healthRate.setter
    def healthRate(self, value):
        if 0 <= value <= 100:
            self._healthRate = value
        else:
            raise ValueError("Health rate must be between 0 and 100.")

    def sleep(self, hours):
        if hours == 7:
            self.mood = MOODS[0]  
        elif hours < 7:
            self.mood = MOODS[1]  
        else:
            self.mood = MOODS[2]  

    def eat(self, meals):
        if meals == 3:
            self.healthRate = 100
        elif meals == 2:
            self.healthRate = 75
        elif meals == 1:
            self.healthRate = 50

    def buy(self, items):
        self.money -= 10 * items  

class Car:
    def __init__(self, name, fuelRate, velocity):
        self.name = name
        self.fuelRate = fuelRate 
        self.velocity = velocity 

    @property
    def fuelRate(self):
        return self._fuelRate

    @fuelRate.setter
    def fuelRate(self, value):
        if 0 <= value <= 100:
            self._fuelRate = value
        else:
            self._fuelRate = max(0, min(value, 100))  

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if 0 <= value <= 200:
            self._velocity = value
        else:
            raise ValueError("Velocity must be between 0 and 200.")

    def run(self, velocity, distance):
        self.velocity = velocity
        fuel_needed = distance * 1.0  
        
        if self.fuelRate >= fuel_needed:
            self.fuelRate -= fuel_needed
            self.stop(remain_distance=0)
        else:
            covered_distance = self.fuelRate
            remain_distance = distance - covered_distance
            self.fuelRate = 0
            self.stop(remain_distance=remain_distance)

    def stop(self, remain_distance=0):
        self.velocity = 0
        if remain_distance == 0:
            print(f"You have arrived at your destination successfully with {self.name}!") 
        else:
            print(f"Out of fuel! The car has stopped. Remaining distance to arrive: {remain_distance} km.") 


class Employee(Person):  
    def __init__(self, name, money, mood, healthRate, emp_id, car, email, salary, distanceToWork):
        super().__init__(name, money, mood, healthRate)
        self.id = emp_id
        self.car = car  
        self.email = email  
        self.salary = salary  
        self.distanceToWork = distanceToWork

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value >= 1000:
            self._salary = value
        else:
            raise ValueError("Salary must be 1000 or more.")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            self._email = value
        else:
            raise ValueError("Invalid email address!")

    def work(self, hours):
        if hours == 8:
            self.mood = MOODS[0]  
        elif hours > 8:
            self.mood = MOODS[1]  
        else:
            self.mood = MOODS[2]  

    def drive(self, distance, velocity):
        if self.car:
            self.car.run(velocity, distance)
        else:
            print("This employee does not have a car to drive.")

    def refuel(self, gasAmount=100):
        if self.car:
            self.car.fuelRate += gasAmount
        else:
            print("No car available to refuel.")

    def send_mail(self, to, subject, msg, receiver_name):
        email_content = f"From: {self.email}\nTo: {to}\n\nHi, {receiver_name}\n{msg}\nthanks\n{subject}"
        with open("email_composer.txt", "w", encoding="utf-8") as f:
            f.write(email_content)
        print("Email file generated successfully as 'email_composer.txt'.")


class Office:
    employeesNum = 0 

    def __init__(self, name, employees=None):
        self.name = name
        self.employees = employees if employees is not None else []
        Office.employeesNum += len(self.employees)

    @classmethod
    def change_emps_num(cls, num):
        cls.employeesNum = num

    def get_all_employees(self):
        return self.employees

    def get_employee(self, empId):
        for emp in self.employees:
            if emp.id == empId:
                return emp
        return None

    def hire(self, employee):
        self.employees.append(employee)
        Office.employeesNum += 1
        print(f"Employee {employee.name} has been hired successfully.")

    def fire(self, empId):
        emp = self.get_employee(empId)
        if emp:
            self.employees.remove(emp)
            Office.employeesNum -= 1
            print(f"Employee with ID {empId} has been fired.")
        else:
            print("Employee not found.")

    def deduct(self, empId, deduction):
        emp = self.get_employee(empId)
        if emp:
            emp.salary -= deduction

    def reward(self, empId, reward_amount):
        emp = self.get_employee(empId)
        if emp:
            emp.salary += reward_amount

    @staticmethod
    def calculate_lateness(targetHour, moveHour, distance, velocity):
        arrival_time = moveHour + (distance / velocity)
        return arrival_time > targetHour

    def check_lateness(self, empId, moveHour):
        emp = self.get_employee(empId) 
        if emp:
            trip_velocity = emp.car.velocity if (emp.car and emp.car.velocity > 0) else 40
            
            is_late = Office.calculate_lateness(9, moveHour, emp.distanceToWork, trip_velocity) 
            if is_late:
                self.deduct(empId, 10) 
                print(f"Employee {emp.name} is late! 10 L.E deducted from salary.") 
            else:
                self.reward(empId, 10) 
                print(f"Employee {emp.name} arrived on time! 10 L.E rewarded to salary.") 



if __name__ == "__main__":
    samys_car = Car(name="Fiat 128", fuelRate=60, velocity=0)

    samy = Employee(
        name="Samy",
        money=500,
        mood="happy",
        healthRate=100,
        emp_id=1,
        car=samys_car,
        email="samy@iti.gov.eg",
        salary=5000,
        distanceToWork=20
    )

    iti_office = Office(name="ITI Smart Village Office")
    iti_office.hire(samy)

    print("\n--- Samy's Trip to Work ---")
    samy.drive(distance=samy.distanceToWork, velocity=40)
    iti_office.check_lateness(empId=samy.id, moveHour=8.5)

    office_data = {
        "office_name": iti_office.name,
        "total_employees_count": Office.employeesNum,
        "employees": [
            {
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "salary": emp.salary,
                "mood": emp.mood,
                "health_rate": emp.healthRate,
                "money": emp.money,
                "car": {
                    "name": emp.car.name,
                    "fuel_rate": emp.car.fuelRate,
                    "velocity": emp.car.velocity
                } if emp.car else None
            } for emp in iti_office.get_all_employees()
        ]
    }

    with open("iti_office_data.json", "w", encoding="utf-8") as json_file:
        json.dump(office_data, json_file, indent=4, ensure_ascii=False)
        
    print("\n[All office data saved successfully to 'iti_office_data.json']")