from provider import Provider
from client import Client
from rbac import RBAC
from datetime import datetime

rbac=RBAC()
provider1=Provider(provider_id=101,name="Dr. Rahul",specialization="cardiologist")
client1=Client(client_id=201,name="Pratiksha",age=22,contact="7330333636")
provider1.update_availability(
    datetime(2026, 11, 9, 9, 0),
    datetime(2026, 11, 9, 17, 0)
)
provider1.update_availability(
    datetime(2026, 11, 16, 9, 0),
    datetime(2026, 11, 16, 17, 0)
)

provider1.update_availability(
    datetime(2026, 11, 23, 9, 0),
    datetime(2026, 11, 23, 17, 0)
)
# Book an individual appointment
appointment_start = datetime(2026, 11, 9, 10, 0)
appointment_end = datetime(2026, 11, 9, 10, 30)

result = client1.book_appointment(
    provider1,
    appointment_start,
    appointment_end,
    rbac
)

print(result)
print(client1.view_appointments())
recurring_result = client1.book_recurring_appointment(
    provider=provider1,
    start_time=datetime(2026, 11, 9, 11, 0),
    end_time=datetime(2026, 11, 9, 11, 30),
    frequency="WEEKLY",
    count=3,
    rbac=rbac
)

print(recurring_result)
print("\nAll Patient Appointments:")
for appointment in client1.view_appointments():
    print(appointment)

conflict_result = client1.book_appointment(
    provider1,
    datetime(2026, 11, 9, 11, 15),
    datetime(2026, 11, 9, 11, 45),
    rbac
)

print("Conflict Test:", conflict_result)
permission_result = rbac.check_permission(
    client1.client_id,
    "patient",
    "manage_users"
)

print("Permission Test:", permission_result)


