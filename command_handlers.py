from addressbook import AddressBook
# from notebook import NoteBook
from file_sorter import file_sorter


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError as index_error:
            return index_error
        except ValueError as value_error:
            return value_error
        except KeyError as key_error:
            return key_error
        except AttributeError as attribute_error:
            return attribute_error
        except NotImplementedError:
            return 'This feature is not implemented'
    return execute


def welcome_message(*args) -> str:
    message = "Hi! How can i help you?"
    return message


def help_message(*args) -> str:
    message = """
Commands and their usage:
add: 
    record 'name'                        : adds a new record with specified name.
    phone 'name' 'phone'                 : add new phone to record.
    email 'name' 'email'                 : add email to record. Can be only one.
    birthday 'name' 'birthday'           : add birthday to record. Can be only one. Birthday format dd-mm-yyyy.
    note                                 : add note to notebook.
    tags                                 : add tag(s) to the note you'll choose from notebook.
change: 
    phone 'name' 'old phone' 'new phone' : change old phone with new one.
    email 'name' 'email'                 : change email in record. 
    birthday 'name' 'birthday'           : change birthday in record. Birthday format dd-mm-yyyy.
    note                                 : change the note text.
    note title                           : change the note title.
    tags                                 : change the tags for chosen note. 
del: 
    record 'name'                        : delete record with specified name.
    phone 'name' 'phone'                 : delete phone from record.
    email 'name' 'email'                 : NOT IMPLEMENTED
    birthday 'name' 'birthday'           : NOT IMPLEMENTED
    note                                 : delete the note from notebook completely.
    tags                                 : delete all tags from the note.

#:                                       : search by a tags (usage: # tag1 tag2...).
    """
    return message


@input_error
def add_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'record':
        addressbook.add_record(args[1])
        message = f'New record with name {args[1]} added to addressbook.'
    elif args[0] == 'phone':
        addressbook[args[1]].add_phone(args[2])
        message = f'Phone {args[2]} added to {args[1]} record.'
    elif args[0] == 'email':
        addressbook[args[1]].set_email(args[2])
        message = f'Email {args[2]} added to {args[1]} record.'
    elif args[0] == 'birthday':
        addressbook[args[1]].set_birthday(args[2])
        message = f'Birthday {args[2]} added to {args[1]} record.'
    elif args[0] == 'note':
        message = addressbook.notebook.create_note()
    elif args[0] == 'tags':

        message = addressbook.notebook.set_tags()
    else:
        message = f'add does not support {args[0]} command.'
    return message


@input_error
def change_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'phone':
        addressbook[args[1]].del_phone(args[2])
        addressbook[args[1]].add_phone(args[3])
        message = f'Phone in record {args[1]} was changed from {args[2]} to {args[3]} record.'
    elif args[0] == 'email':
        addressbook[args[1]].set_email(args[2])
        message = f'Email in record {args[1]} was changed'
    elif args[0] == 'birthday':
        addressbook[args[1]].set_birthday(args[2])
        message = f'Email in record {args[1]} was changed'
    elif args[0] == 'note' and len(args) == 1:
        message = addressbook.notebook.change_note()
    elif args[0] == 'note' and args[1] == 'title':
        message = addressbook.notebook.change_title()
    elif args[0] == 'tags':
        message = addressbook.notebook.change_tags()
    else:
        message = f'change does not support {" ".join(args)} command.'
    return message


@input_error
def del_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'record':
        addressbook.del_record(args[1])
        message = f'Record with name {args[1]} was deleted from addressbook.'
    elif args[0] == 'phone':
        addressbook[args[1]].del_phone(args[2])
        message = f'Phone {args[2]} was deleted from {args[1]} record.'
    elif args[0] == 'email':
        raise NotImplementedError
    elif args[0] == 'birthday':
        raise NotImplementedError
    elif args[0] == 'note':
        message = addressbook.notebook.del_note()
    elif args[0] == 'tags':
        message = addressbook.notebook.del_tags()
    else:
        message = f'del does not support {args[0]} command.'
    return message


@input_error
def show_handler(addressbook: AddressBook, *args) -> str:
    if len(args) < 1:
        addressbook.show_records()
        return 'All records are shown.'
    elif len(args) == 1 and args[0] == 'notes':
        mes = addressbook.notebook.show_notes()
        return mes
    return "Something went wrong."


@input_error
def search_handler(addressbook: AddressBook, *args):
    query = " ".join(args)
    results = addressbook.search(query)
    if not results:
        # res_notes = addressbook.notebook.search_note(query)
        # if res_notes:
        #     print(f"{len(res_notes)} note(s) was found.")
        #     response = "".join(str(note) for note in res_notes)
        #     return response
        # else:
        return "Nothing was found."
    # response = ""
    # for record in results:
    #     response += f"{str(record.name.value).capitalize()}: {record.phones}\n"
    return results


def find_tag(addressbook: AddressBook, *args):
    result = addressbook.notebook.find_tag(args)
    if not result:
        return "No such tag(s)"
    print(f"{len(result)} note(s) was found with {' '.join('#'+tag for tag in args)}")
    response = "".join(str(note) for note in result)
    return response


def save_data(addressbook: AddressBook, *args) -> str:
    addressbook.save_records_to_file('storage1.dat')
    return "Records have been saved."


def load_data(addressbook: AddressBook, *args) -> str:
    addressbook.read_records_from_file('storage1.dat')
    return "Records have been loaded."


@input_error
def sort_files(addressbook: AddressBook, *args) -> str:
    message = file_sorter(args[0])


def notes(addressbook: AddressBook, *args):
    raise NotImplementedError


def list_contacts_with_days_to_birthday(addressbook: AddressBook, *args):
    birthdays = addressbook.contacts_with_days_to_bday(args[0])
    if len(birthdays) == 0:
        return f"No contacts will have birthday in {args[0]} days"
    return f'The following contacts will have days in {args[0]} days: \n{birthdays}'


function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'change': change_handler,
            'del': del_handler,
            'show': show_handler,
            'search': search_handler,
            'save': save_data,
            'load': load_data,
            'sort_files': sort_files,
            'birthdays': list_contacts_with_days_to_birthday,
            '#': find_tag}
