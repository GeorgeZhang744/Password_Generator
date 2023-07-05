from tkinter import *
from tkinter import messagebox
import pyperclip as PC

import password_generator as PG
import password_storage as PS

POSSIBLE_PASSWORD_LENGTH = [x for x in range(PG.PASSWORD_MIN_LENGTH, PG.PASSWORD_MAX_LENGTH + 1)]
NUMBER_OF_PASSWORDS_TO_SHOW_IN_ONE_PAGE = 10

# Configuring the size of displaying panel
SETTING_DESCRIPTION_WIDTH = 25
SETTING_CHECKBOX_WIDTH = 15

new_pwd = ""

password_generator = PG.PasswordGenerator(PG.PASSWORD_MIN_LENGTH)
password_database_controller = PS.Password_Database_Controller()

root = Tk()
root.title("Password Generator")
root.resizable(0,0)

setting_choices = Frame(root).grid(row=0, column=0)
setting_selections = Frame(root).grid(row=0, column=1)
password_displaying_section = Frame(root).grid(row=1, column=0)

# Password generator setting labels:
password_length_label = Label(setting_choices, text="Password length: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=0, column=0, padx=(5, 0), pady=5)
include_numbers_label = Label(setting_choices, text="Include numbers: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=1, column=0, padx=(5, 0), pady=5)
include_lowercases_label = Label(setting_choices, text="Include lowercases: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=2, column=0, padx=(5, 0), pady=5)
include_uppercases_label = Label(setting_choices, text="Include uppercases: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=3, column=0, padx=(5, 0), pady=5)
include_symbols_label = Label(setting_choices, text="Include symbols: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=4, column=0, padx=(5, 0), pady=5)
exclude_similar_characters_label = Label(setting_choices, text="Exclude similar characters: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=5, column=0, padx=(5, 0), pady=5)
exclude_ambiguous_characters_label = Label(setting_choices, text="Exclude ambiguous characters: ", width=SETTING_DESCRIPTION_WIDTH, anchor=W, justify=LEFT).grid(row=6, column=0, padx=(5, 0), pady=5)

# Password length selection:
password_length = IntVar()
password_length.set(POSSIBLE_PASSWORD_LENGTH[0])
password_length_dropdown = OptionMenu(setting_selections, password_length,  *POSSIBLE_PASSWORD_LENGTH)
password_length_dropdown.config(width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT)
password_length_dropdown.grid(row=0, column=1, columnspan=2, pady=10)

# Password generator settings selection variables:
include_numbers = BooleanVar()
include_lowercases = BooleanVar()
include_uppercases = BooleanVar()
include_symbols = BooleanVar()
exclude_similar_characters = BooleanVar()
exclude_ambiguous_characters = BooleanVar()

# Password generator settings selection checkboxes:
include_numbers_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. 123456)", variable=include_numbers)
include_lowercases_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. abcdef)", variable=include_lowercases)
include_uppercases_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. ABCDEF)", variable=include_uppercases)
include_symbols_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. !@#$%^)", variable=include_symbols)
exclude_similar_characters_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. i, I, l, o, 0, O)", variable=exclude_similar_characters)
exclude_ambiguous_characters_checkbox = Checkbutton(setting_selections, width=SETTING_CHECKBOX_WIDTH, anchor=W, justify=LEFT, text="(e.g. [, ], (, ), {, })", variable=exclude_ambiguous_characters)

# Set up default password generator settings:
include_numbers_checkbox.select()
include_lowercases_checkbox.select()
include_uppercases_checkbox.select()
include_symbols_checkbox.select()

# Display the setting checkboxes on panel:
include_numbers_checkbox.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
include_lowercases_checkbox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
include_uppercases_checkbox.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
include_symbols_checkbox.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
exclude_similar_characters_checkbox.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
exclude_ambiguous_characters_checkbox.grid(row=6, column=1, columnspan=2, padx=5, pady=5)

# Display the generated password:
gen_pwd_label = Label(password_displaying_section, text="Your new password: ", font=('lucida', 10,'bold'), width=18, anchor=W, justify=CENTER).grid(row=8, column=0, pady=10)
gen_pwd = Entry(password_displaying_section, width=25, justify=LEFT)
gen_pwd.grid(row=8, column=1, padx=(0, 10), pady=10)


# -----------------------------------------Helper functions for user-clickable buttons on the panel-----------------------------------------

# Update the password generator settings:
def update_password_setting():
    password_generator.set_password_length(password_length.get())
    password_generator.change_setting('numbers', include_numbers.get())
    password_generator.change_setting('lowercases', include_lowercases.get())
    password_generator.change_setting('uppercases', include_uppercases.get())
    password_generator.change_setting('symbols', include_symbols.get())
    password_generator.change_filter_setting('similar_characters', exclude_similar_characters.get())
    password_generator.change_filter_setting('ambiguous_characters', exclude_ambiguous_characters.get())
    
# Generates new password based the set up setting and display it in the entry box on panel:
def display_new_password():
    global new_pwd

    # Update the password generator setting, generate new password, and store it into the passwords database
    update_password_setting()
    new_pwd = password_generator.generate_password()
    password_database_controller.insert_new_password(new_pwd)

    # Display the new password in the entry box
    gen_pwd.delete(0, END)
    gen_pwd.insert(0, new_pwd)

# Copy the given password to user's clipboard:
def copy_pwd(pwd):
    if pwd:
        PC.copy(pwd)

# Copy the password associated with the given id in the passwords database to the user's clipboard:
def copy_pwd_from_database(id):
    if id == "":
        messagebox.showerror("Error", "Please select the id of the password that you want to copy")

    if not password_database_controller.does_id_exist(id):
        password_id_selection.delete(0, END)
        messagebox.showerror("Error", "Selected id does not exist")

    copy_pwd(password_database_controller.get_password(id)[0])
    password_id_selection.delete(0, END)

# Delete the password associated with the given id from the passwords database:
def delete_pwd_from_database(id):
    global last_page
    global curr_page
    global prev_page_button
    global next_page_button

    # Check if the user select an id
    if id == "":
        messagebox.showerror("Error", "Please select the id of the password that you want to delete")

    # Check if the given id existed in the database
    if not password_database_controller.does_id_exist(id):
        password_id_selection.delete(0, END)
        messagebox.showerror("Error", "Selected id does not exist")

    # Delete the password from the database
    password_database_controller.delete_password(id)
    password_id_selection.delete(0, END)

    old_max_page = last_page
    last_page = get_max_page()

    # Reorganize the password displaying page after a password is removed 
    if old_max_page > last_page:
        if curr_page == last_page:
            prev_page_button = Button(new_window, text="<-", bd=1, state=DISABLED)
            next_page_button = Button(new_window, text="->", bd=1, state=DISABLED)
            prev_page_button.grid(row=3, column=0, pady=(5, 10))
            next_page_button.grid(row=3, column=2, pady=(5, 10))
        elif curr_page == 1:
            next_page(curr_page+1)
        elif curr_page == old_max_page:
            prev_page(curr_page-1)

    # Display the remaining passwords in the database
    current_page_passwords_label.config(text=show_nth_passwords(NUMBER_OF_PASSWORDS_TO_SHOW_IN_ONE_PAGE, curr_page))

# Delete all of the passwords in the database:
def delete_all_pwd_from_database():
    global last_page
    global curr_page
    global prev_page_button
    global next_page_button

    # Confirm with the user to delete all of the passwords
    response = messagebox.askyesno("Confirming deletion", "Are you sure you want to delete all of your passwords?")
    password_id_selection.delete(0, END)

    # Delete all of the passwords if the user confirms the deletion
    if response == 1:
        password_database_controller.delete_all_passwords()
        current_page_passwords_label.config(text="")
        last_page = 1
        curr_page = 1
        prev_page_button.config(state=DISABLED)
        next_page_button.config(state=DISABLED)
        prev_page_button.grid(row=3, column=0, pady=(5, 10))
        next_page_button.grid(row=3, column=2, pady=(5, 10))

# Calculate the maximum number of pages needed to display all of the passwords:
def get_max_page():
    table_size = password_database_controller.get_number_of_passwords()

    if table_size <= 10:
        return 1

    return table_size // 10 if table_size % 10 == 0 else table_size // 10 + 1   

# Show the passwords on nth page on the displaying panel:
def show_nth_passwords(n, curr_page):
    all_passwords = password_database_controller.get_all_previous_passwords()
    password_total_numbers = password_database_controller.get_number_of_passwords()

    start = n * (curr_page - 1)
    if password_total_numbers > start + n:
        end = start + n 
    else:
        end = password_total_numbers

    return password_database_controller.get_passwords_in_string(all_passwords[start: end])

# Helper function to reset tht the previous and next page arrows to a property state when passwords are added/deleted in database:
def reset_prev_and_next_arrows(page):
    prev_page_button = Button(new_window, text="<-", command=lambda: prev_page(page-1))
    next_page_button = Button(new_window, text="->", command=lambda: next_page(page+1))

    if curr_page == last_page:
        next_page_button.config(state=DISABLED)

    if last_page == 1:
        prev_page_button.config(state=DISABLED)

    prev_page_button.grid(row=3, column=0, pady=(5, 10))
    next_page_button.grid(row=3, column=2, pady=(5, 10))

# Navigate to previous page:
def prev_page(page):
    global curr_page

    passwords_to_be_shown = show_nth_passwords(NUMBER_OF_PASSWORDS_TO_SHOW_IN_ONE_PAGE, page)
    current_page_passwords_label.config(text=passwords_to_be_shown)

    curr_page -= 1
    current_page_label.config(text=str(curr_page))

    reset_prev_and_next_arrows(page)

# Navigate to next page:
def next_page(page):
    global curr_page

    passwords_to_be_shown = show_nth_passwords(NUMBER_OF_PASSWORDS_TO_SHOW_IN_ONE_PAGE, page)
    current_page_passwords_label.config(text=passwords_to_be_shown)

    curr_page += 1
    current_page_label.config(text=str(curr_page))

    reset_prev_and_next_arrows(page)

# Pops up a new window that allows the user to operate the passwords stored in the database:
def display_password_database():
    global new_window
    global password_id_selection
    global current_page_passwords_label
    global current_page_label
    global prev_page_button
    global next_page_button
    global curr_page
    global last_page 
    
    curr_page = 1
    last_page = get_max_page()

    new_window = Toplevel()
    new_window.title("Generated Passwords")
    new_window.resizable(0,0)

    # -----------------------------------Previous passwords displaying section-----------------------------------

    # A frame that is used to show the previous generated passwords in the database
    password_frame = LabelFrame(new_window, text="Generated passwords", pady=10)
    password_frame.grid(row=2, column=0, columnspan=3, padx=20)

    password_id_label = Label(new_window, text='Select id:')
    password_id_label.grid(row=0, column=0, pady=10)

    # A entry box for users to enter the id of the password that they want to do operations on
    password_id_selection = Entry(new_window, width=20, justify=CENTER)
    password_id_selection.grid(row=0, column=1, columnspan=2, pady=10)

    # Display the passwords on current page that is shown to the user
    passwords_on_current_page = show_nth_passwords(NUMBER_OF_PASSWORDS_TO_SHOW_IN_ONE_PAGE, curr_page)
    current_page_passwords_label = Label(password_frame, width=30, text=passwords_on_current_page, justify=LEFT, anchor=W)
    current_page_passwords_label.grid(row=0, column=0, columnspan=3)

    # --------------------------------Previous passwords displaying section ended--------------------------------



    # -----------------------------------------Buttons on the new window-----------------------------------------

    # A button that copies the password with the id selected by the user
    password_copy_button = Button(new_window, text="Copy", width=7, justify=CENTER, command=lambda: copy_pwd_from_database(password_id_selection.get()))
    password_copy_button.grid(row=1, column=0, padx=(5, 0), pady=(0, 10))

    # A button that deletes the password with the id selected by the user
    password_delete_button = Button(new_window, text="Delete", width=7, justify=CENTER, command=lambda: delete_pwd_from_database(password_id_selection.get()))
    password_delete_button.grid(row=1, column=1, pady=(0, 10))

    # A button that deletes all of the passwords stored in the database
    password_delete_all_button = Button(new_window, text="Delete all", width=7, justify=CENTER, command=delete_all_pwd_from_database)
    password_delete_all_button.grid(row=1, column=2, padx=(0, 5), pady=(0, 10))

    # -------------------------------------------Buttons section ended-------------------------------------------



    # ------------------------------------------Page navigation section------------------------------------------

    # A label that displays the current page the user is on 
    current_page_label = Label(new_window, text=str(curr_page))
    current_page_label.grid(row=3, column=1, pady=(5, 10))

    # A button that navigates to the previous page 
    prev_page_button = Button(new_window, text="<-", bd=1, state=DISABLED)
    prev_page_button.grid(row=3, column=0, pady=(5, 10))

    # A button that navigates to the next page
    next_page_button = Button(new_window, text="->", bd=1, command=lambda: next_page(2))
    next_page_button.grid(row=3, column=2, pady=(5, 10))

    # Disable the next page button if there is only one page total
    if curr_page == last_page:
        next_page_button.config(state=DISABLED)

    # ---------------------------------------Page navigation section ended---------------------------------------

# ----------------------------------------------------------Helper functions ended----------------------------------------------------------



# ----------------------------------------------------------Buttons on the panel----------------------------------------------------------

# A button that generates the password based on setup settings:
gen_pwd_button = Button(root, text="Generate Password", command=display_new_password).grid(row=7, column=0, pady=(15, 0))

# A button that copies the password that is just generated:
copy_pwd_button = Button(root, text="Copy", width=5, command=lambda: copy_pwd(new_pwd)).grid(row=8, column=2, padx=10, pady=10)

# A button that opens up the password database operating panel:
password_database_control_panel_button = Button(root, text="Previous passwords", command=display_password_database).grid(row=7, column=1, columnspan=2, pady=(15, 0))

# ----------------------------------------------------------Buttons section ended----------------------------------------------------------


root.mainloop()