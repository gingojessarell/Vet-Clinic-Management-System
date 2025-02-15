from datetime import datetime
from tabulate import tabulate

class VetClinic:
    def __init__(self):
        self.patients = []
        self.appointments = {}
        self.patient_id_counter = 1

    def add_patient(self, pet_name, species, owner):
        """Method to add a new patient record."""
        # Check if the patient is already in the list
        for patient in self.patients:
            if patient['pet_name'] == pet_name:
                print(f"Invalid! Patient record for {pet_name} already in the list.")
                return
        # Add the patient if not found in the list
        patient = {
            'id': self.patient_id_counter,
            'pet_name': pet_name, 
            'species': species, 
            'owner': owner
        }
        self.patients.append(patient)
        print(f"Patient {pet_name} added successfully with ID {self.patient_id_counter}.")
        self.patient_id_counter += 1  # Increment the ID counter for the next patient

    def list_patients(self):
        """Method to list all patient records in a table format."""
        if not self.patients:
            print("No patients available.")
            return
        
        table_data = [(patient['id'], patient['pet_name'], patient['species'], patient['owner']) for patient in self.patients]
        headers = ["ID", "Pet Name", "Species", "Owner"]
        print(tabulate(table_data, headers, tablefmt="grid"))

    def book_appointment(self, patient_id, appointment_date, appointment_time):
        """Method to book an appointment for a pet."""
        # Find the patient by ID
        patient = next((p for p in self.patients if p['id'] == patient_id), None)
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        
        pet_name = patient['pet_name']
        species = patient['species']
        owner = patient['owner']
        
        if pet_name not in self.appointments:
            appointment = f"{appointment_date} {appointment_time}"
            self.appointments[pet_name] = {'species': species, 'owner': owner, 'appointment': appointment}
            print(f"Appointment booked for {pet_name} ({species}) owned by {owner} on {appointment}.")
        else:
            print(f"{pet_name} already has an appointment.")

    def list_appointments(self):
        """Method to list all booked appointments."""
        if not self.appointments:
            print("No appointments available.")
            return
        
        table_data = [(pet_name, details['species'], details['owner'], details['appointment']) 
                      for pet_name, details in self.appointments.items()]
        headers = ["Pet Name", "Species", "Owner", "Appointment"]
        print(tabulate(table_data, headers, tablefmt="grid"))

    def update_patient_info(self, pet_name, new_name=None, new_species=None, new_owner=None):
        """Method to update a patient's information."""
        for patient in self.patients:
            if patient['pet_name'] == pet_name:
                # Update patient info
                if new_name:
                    old_name = patient['pet_name']
                    patient['pet_name'] = new_name
                    # Update appointment if the pet name changes
                    if old_name in self.appointments:
                        self.appointments[new_name] = self.appointments.pop(old_name)
                if new_species:
                    patient['species'] = new_species
                    # Update appointment species
                    if patient['pet_name'] in self.appointments:
                        self.appointments[patient['pet_name']]['species'] = new_species
                if new_owner:
                    patient['owner'] = new_owner
                    # Update appointment owner
                    if patient['pet_name'] in self.appointments:
                        self.appointments[patient['pet_name']]['owner'] = new_owner
                print(f"Patient information updated for {pet_name}.")
                return
        print(f"Patient {pet_name} not found.")

    def generate_report(self):
        """Generate a report of all patients and their appointments in a table format."""
        if not self.patients:
            print("No patients to generate a report.")
            return

        table_data = []
        for patient in self.patients:
            appointment = self.appointments.get(patient['pet_name'], "No appointment")
            # Correct the format here to include the appointment details correctly
            appointment_info = appointment['appointment'] if appointment != "No appointment" else "No appointment"
            table_data.append((patient['id'], patient['pet_name'], patient['species'], patient['owner'], appointment_info))
        
        headers = ["ID", "Pet Name", "Species", "Owner", "Appointment"]
        print(tabulate(table_data, headers, tablefmt="grid"))

    def cancel_appointment(self, pet_name):
        """Cancel an existing appointment."""
        if pet_name in self.appointments:
            del self.appointments[pet_name]
            print(f"Appointment for {pet_name} canceled.")
        else:
            print(f"No appointment found for {pet_name}.")

# Error handling function for date input (YYYY-MM-DD)
def get_valid_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

# Error handling function for time input (HH:MM AM/PM)
def get_valid_time_input(prompt):
    while True:
        time_str = input(prompt)
        try:
            time = datetime.strptime(time_str, "%I:%M %p")  # 12-hour format with AM/PM
            return time.strftime("%I:%M %p")
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM AM/PM format.")

# Error handling function for other inputs
def get_valid_input(prompt, input_type=str):
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

# Function to validate pet's species
def get_valid_species_input():
    while True:
        species = input("Enter pet's species (dog or cat): ").lower()
        if species in ['dog', 'cat']:
            return species
        else:
            print("Invalid species. Please enter 'dog' or 'cat'.")

# Main program to interact with VetClinic
def main():
    clinic = VetClinic()
    
    while True:
        print("\nWelcome to Vet Clinic Management System")
        print()
        print("1. Add Patient Record")
        print("2. List Patients")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Update Patient Info")
        print("6. Cancel Appointment")
        print("7. Generate Report")
        print("8. Exit")
        print()
        
        choice = get_valid_input("Select an option: ", int)
        
        # Perform the action based on the user's choice
        if choice == 1:
            pet_name = input("Enter pet's name: ")
            species = get_valid_species_input()
            owner = input("Enter owner's name: ")
            clinic.add_patient(pet_name, species, owner)
        elif choice == 2:                   #elif allows to check multiple expressions for truth value and execute a block of code
            clinic.list_patients()
        elif choice == 3:
            clinic.list_patients()
            patient_id = get_valid_input("Enter patient ID to book an appointment: ", int)
            appointment_date = get_valid_date_input("Enter appointment date (YYYY-MM-DD): ")
            appointment_time = get_valid_time_input("Enter appointment time (HH:MM AM/PM): ")
            clinic.book_appointment(patient_id, appointment_date, appointment_time)
        elif choice == 4:
            clinic.list_appointments()
        elif choice == 5:
            pet_name = input("Enter pet's name: ")
            new_name = input("Enter new name (leave empty for no change): ")
            new_species = input("Enter new species (leave empty for no change): ")
            new_owner = input("Enter new owner's name (leave empty for no change): ")
            clinic.update_patient_info(pet_name, new_name, new_species, new_owner)
        elif choice == 6:
            pet_name = input("Enter pet's name to cancel appointment: ")
            clinic.cancel_appointment(pet_name)
        elif choice == 7:
            clinic.generate_report()
        elif choice == 8:
            print("Exiting the Vet Clinic Management System.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()