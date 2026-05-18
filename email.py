from_email = input("From: ")
to_email = input("To: ")
name = input("Name: ")
subject = input("Email Subject: ")

file = open("email.txt", "w")

file.write(f"Email Subject: {subject}\n")
file.write(f"From: {from_email}\n")
file.write(f"To: {to_email}\n\n")

file.write(f"Hi, {name}\n")
file.write("This is an email template\n")
file.write("Thanks")

file.close()

