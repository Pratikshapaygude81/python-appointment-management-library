
class Provider:
    """Handles doctor information and availability"""

    def __init__(self, provider_id, name, specialization):
        self.provider_id = provider_id
        self.name = name
        self.specialization = specialization
        self.availability = []

    def update_availability(self, day, time):
        slot = {
            "day": day,
            "time": time,
            "is_booked": False
        }
        self.availability.append(slot)

    def check_availability(self, day, time):
        for slot in self.availability:
            if slot["day"] == day and slot["time"] == time:
                if slot["is_booked"] == False:
                    return True
        return False

    def book_slot(self, day, time):
        for slot in self.availability:
            if slot["day"] == day and slot["time"] == time:
                if slot["is_booked"] == False:
                    slot["is_booked"] = True
                    return True
        return False

    def get_provider_details(self):
        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "specialization": self.specialization,
            "availability": self.availability
        }



class Client:
    """Handles client information and appointments"""

    def __init__(self, client_id, name, age, contact):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.contact = contact
        self.appointments = []

    def get_client_detail(self):
        return {
            "client_id": self.client_id,
            "client_name": self.name,
            "client_age": self.age,
            "contact_no": self.contact,
            "appointments": self.appointments
        }

    def book_appointment(self, provider, day, time, rbac):
        if not rbac.check_permission(self.client_id, "patient", "book_appointment"):
            return "Permission denied"

        if provider.book_slot(day, time):
            appointment = {
                "provider_id": provider.provider_id,
                "doctors_name": provider.name,
                "day": day,
                "time": time
            }

            self.appointments.append(appointment)
            return "Appointment booked successfully"

        return "Doctor is not available"

    def view_appointments(self):
        if not self.appointments:
            return "No appointments booked"

        return self.appointments


class RBAC:
    """Handles user roles and permissions"""

    def __init__(self):
        self.roles = {
            "doctor": [],
            "patient": []
        }

        self.permissions = {
            "doctor": ["view_appointments", "update_availability"],
            "patient": ["view_doctors", "book_appointment", "view_appointments"]
        }

    def assign_role(self, user_id, role):
        if role not in self.roles:
            return "Invalid role"

        self.roles[role].append(user_id)
        return f"{role} role assigned successfully"
    def check_permission(self, user_id, role, permission):
        if role in self.roles:
            if user_id in self.roles[role]:
                if permission in self.permissions[role]:
                    return True

        return False
# Creating doctor object
doctor1 = Provider(101, "Rahul", "Cardiologist")

# Adding doctor availability
doctor1.update_availability("Monday", "10 AM - 1 PM")
doctor1.update_availability("Tuesday", "2 PM - 5 PM")

# Creating patient objects
client1 = Client(201, "Om", 22, "879087658")
client2 = Client(202, "Sneha", 23, "9876543211")

# Creating RBAC object
rbac = RBAC()

# Assigning roles
print(rbac.assign_role(101, "doctor"))
print(rbac.assign_role(201, "patient"))
print(rbac.assign_role(202, "patient"))

print("Patient can book appointment:",
      rbac.check_permission(201, "patient", "book_appointment"))

print("Doctor can book appointment:",
      rbac.check_permission(101, "doctor", "book_appointment"))

# Checking doctor details
print("\nDoctor Details:")
print(doctor1.get_provider_details())

# Booking appointment
print("\nClient 1:")
print(client1.book_appointment(doctor1, "Monday", "10 AM - 1 PM",rbac))

# Second patient tries to book the same slot
print("\nClient 2:")
print(client2.book_appointment(doctor1, "Monday", "10 AM - 1 PM",rbac))

# Displaying appointments
print("\nClient 1 Appointments:")
print(client1.view_appointments())

print("\nClient 2 Appointments:")
print(client2.view_appointments())

# Final doctor availability
print("\nUpdated Doctor Availability:")
print(doctor1.get_provider_details())

# Testing RBAC permissions

print("\n--- RBAC Testing ---")

print(rbac.check_permission(101, "doctor", "update_availability"))
print(rbac.check_permission(201, "patient", "book_appointment"))
print(rbac.check_permission(201, "patient", "update_availability"))
print(rbac.check_permission(101, "doctor", "book_appointment"))
