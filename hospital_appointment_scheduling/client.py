from datetime import datetime
from icalendar import Calendar, Event
import recurring_ical_events

class Client:
     """
    Represents a patient in the hospital appointment management system.

    The Client class manages patient information and maintains
    the patient's appointment records.

    Attributes:
        client_id (int): Unique identification number of the patient.
        name (str): Name of the patient.
        age (int): Age of the patient.
        contact (str): Contact number of the patient.
        appointments (list): Stores the patient's appointment records.
    """
     def __init__(self,client_id:int,name:str,age:int,contact:str):
          self.client_id=client_id
          self.name=name
          self.age=age
          self.contact=contact
          self.appointments=[]
     def book_appointment(self,provider,start_time,end_time,rbac):
          if not rbac.check_permission(
               self.client_id,"patient","book_appointment"
          ):
               return "permission denied"
          if not provider.book_slot(start_time,end_time):
               return "Doctor is not available for this time-slot"
          appointment={
               "provider_id":provider.provider_id,
               "provider_name":provider.name,
               "start_time":start_time,
               "end_time":end_time,
               "type":"individual"
          }
          self.appointments.append(appointment)
          return "Appointment booked successfully"
     
     def view_appointments(self) -> list:
        """
           Returns all appointments booked by the patient.

           Returns:
               list: List of the patient's appointment records.
        """
        return self.appointments
     def book_recurring_appointment(self,provider,start_time,end_time,frequency,count,rbac):
           """
           Books recurring appointments with a doctor.

           Args:
              provider: Doctor with whom the patient wants to book.
              start_time (datetime): First appointment start time.
              end_time (datetime): First appointment end time.
              frequency (str): Recurrence frequency (DAILY, WEEKLY, MONTHLY).
              count (int): Total number of appointments, including the first.
              rbac: RBAC object used to verify booking permission.
            """
           if not rbac.check_permission(self.client_id,"patient","book_appointment"):
                return "permission denied"
           if start_time>=end_time:
                return"Invalid Appointment time"
           if frequency.upper() not in ["DAILY","WEEKLY","MONTHLY"]:
                return "invalid recurrence frequency"
           if count<1:
                return "appointment must be atleast 1"

           
           calendar = Calendar()

           calendar.add("prodid", "-//Hospital Appointment System//")
           calendar.add("version", "2.0")

           event = Event()

           event.add("summary", "Hospital Appointment")
           event.add("dtstart", start_time)
           event.add("dtend", end_time)

           event.add("rrule", {
              "freq": frequency.lower(),
              "count": count
             })

           calendar.add_component(event)
           recurring_events=recurring_ical_events.of(calendar).all()
           appointments_to_book=[]

           for occurence in recurring_events:
                occurence_start=occurence["DTSTART"].dt
                occurence_end=occurence["DTEND"].dt

                appointments_to_book.append({
                     "start_time":occurence_start,
                     "end_time":occurence_end
                })
           for appointment in appointments_to_book:
                if not provider.check_availability(
                     appointment["start_time"],
                     appointment["end_time"]
                ):
                    return "recurring appointments conflict found"
           for appointment in appointments_to_book:
                if not provider.book_slot(
                    appointment["start_time"],
                    appointment["end_time"]
                ):
                     return "unable to book recurring appointment"
                appointment["provider_id"]=provider.provider_id
                appointment["provider_name"]=provider.name
                appointment["type"]="recurring"
                self.appointments.append(appointment)

           return "recurring appointments are booked successfully"

           

          
