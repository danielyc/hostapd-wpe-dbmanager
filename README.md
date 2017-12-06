# hostapd-wpe-dbmanager

This is a Hostapd-wpe Database manager.
I couldn't find anything like it so that is why i've made this.
I've made this in about an hour so it is qick and dirty.
Don't hasitate to create issues if you encounter any.

# Usage

Checks for db.csv at start-up and creates one if none found.
Checks if there is a hostapd-wpe.log file and reads if so.

Menu contains 6 options:

1. import cracked passwords to the database
- enter the filename of a file with john or hashcat output.
2. search user
- if user found it checks if there is a known password and if so it displays the password
3. export users with uncracked passwords
- enter filename to export to
- chose john or hashcat output
4. delete a user from the database
- enter a username
- if a user is found, it will display the username and password and ask for a confirmation

19. delete database
- asks for confirmation to delete database
99. exit the programm
