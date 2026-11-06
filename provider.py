from datetime import datetime

class Provider:
    """Represents a doctor or healthcare provider in the hospital appointment system.

    The Provider class is responsible for managing doctor information,
    maintaining the doctor's available working hours, checking whether
    an appointment can be scheduled, and reserving appointment slots.

    Each provider has:
        - A unique provider ID.
        - A name.
        - A medical specialization.
        - A list of available time slots.
        - A list of already booked appointments.

    Availability and booked appointments are maintained separately.
    This allows multiple appointments to be scheduled within the
    doctor's available working hours while preventing overlapping bookings.

    Attributes:
        provider_id (int): Unique identification number of the doctor.
        name (str): Full name of the doctor.
        specialization (str): Medical specialization of the doctor.
        availability (list): Stores the doctor's available time slots.
        booked_appointments (list): Stores appointments already reserved."""
    def __init__(self,provider_id:int,name:str,specialization:str):
        self.provider_id=provider_id
        self.name=name
        self.specialization=specialization
        self.availability=[]
        self.booked_appointments = []

    def update_availability(self,start_time:datetime,end_time:datetime):
        if start_time >= end_time:
            return "Invalid availability period"
        slot={
            "start_time":start_time,
            "end_time":end_time,
        }
        self.availability.append(slot)
        return"Availability added successfully"
    def check_availability(self,start_time:datetime,end_time:datetime):
        if start_time>=end_time:
            return False
        available=False
        for slot in self.availability:
            if slot["start_time"]<=start_time and end_time<=slot["end_time"]:
                available=True
                break
        if not available:
            return False
        for appointment in self.booked_appointments:
            if start_time< appointment["end_time"] and end_time >appointment["start_time"]:
                return False
        return True
    def book_slot(self,start_time:datetime,end_time:datetime)->bool:
        if not self.check_availability(start_time,end_time):
            return False
        appointment={
             "start_time":start_time,
             "end_time":end_time
              }
        self.booked_appointments.append(appointment)
        return True
    def get_provider_details(self)->dict:
        return{
            "provider_id":self.provider_id,
            "name":self.name,
            "specialization":self.specialization,
            "availability":self.availability
         }

