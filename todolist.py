import tkinter as tk
from tkinter import messagebox, ttk

#to_do_list

to_do_list=[]

#Function to add new task
def add_task():
    task=input("enter a task:")
    to_do_list.append ({"Task":task,"Status":"pending"})
    print("New Task Added Successfully!")


#function view all task
def view_task():
    print("Your To DO list:")
    if len(to_do_list)==0:
        print("no pending task")
    else:
        for index, task in enumerate(to_do_list,1):
            print(f"{index}:{task}")


#function to remove
def remove_task():
    if len(to_do_list)==0:
        print("list is empty!")
    else:
        try:
            search_index=int(input("enter the task that you want to remove "))-1
            if 0 <= search_index < len(to_do_list):
                removed_task = to_do_list.pop(search_index)
                print(f"task removed :{removed_task['Task']}")
            else:
                print("Invalid Task No.")
        except ValueError:
                print("PLEASE ENTER A VALID TASK NO")

#functon to mark a task done
def mark_done():
    if len(to_do_list)==0:
        print("list is empty")
    else:
        try:
            search_index=int(input("enter the task no. you want to remove"))-1
            if 0 <= search_index < len(to_do_list):
                to_do_list[search_index]['Status']='done'
            else:
                print("invalid task no.")
        except ValueError:
            print("enter a valid task no")

                



#fucn to display a menu
def menu():
    while(True):
        print("*** Main Menu")
        print("1.Add a New Task")
        print("2.View all Tasks")
        print("3.Remove a Task")
        print("4.Task Completed")
        print("5.Exit")

        choice=input("Enter your Choice:")
        if choice =="1":
            add_task()
        elif choice=="2":
            view_task()
        elif choice=="3":
            remove_task ()
        elif choice=="4":
            mark_done()
        elif choice=="5":
            print("Exitting the Application...")
            exit()
        else:
            print("Invalid Choice Try Again!")


menu()
add_task()
view_task()
remove_task()
mark_done()




