from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import messagebox
import os
import csv

class Student:
    def __init__(self):
        self.data = dict()
        self.temp = dict()
        self.filename = 'studentlist.csv'

        if not os.path.exists(self.filename):
            with open(self.filename, mode='w') as csv_file:
                fieldnames = ["ID Number", "Name", "Course", "Year", "Gender"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        else:
            with open(self.filename, newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["ID Number"]] = {'Name': row["Name"], 'Course': row["Course"],
                                                   'Year': row["Year"], 'Gender': row["Gender"]}
            self.temp = self.data.copy()

    def data_to_csv(self):
        datalist = []
        with open(self.filename, "w", newline='') as u:
            fieldnames = ["ID Number", "Name", "Course", "Year", "Gender"]
            writer = csv.DictWriter(u, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for id_no, stud_details in self.data.items():
                temp = {"ID Number": id_no}
                for key, value in stud_details.items():
                    temp[key] = value
                datalist.append(temp)
            writer.writerows(datalist)

    def display_student_table(self, display_table):
        display_table.delete(*display_table.get_children())
        with open(self.filename, "r", encoding="utf-8") as StudData:
            stud_data = csv.DictReader(StudData)

            for stud in stud_data:
                display_table.insert('', 0, values=(stud['ID Number'], stud['Name'], stud['Course'], stud['Year'],
                                                    stud['Gender']))\


    def id_checker(self, id_num):
        if len(id_num) != 9:
            messagebox.showerror("Error", "Invalid ID Number")
        elif id_num[4] != '-' or not id_num.replace("-", "").isdigit():
            messagebox.showerror("Error", "Invalid ID Number")
        else:
            return True
        return False

class SearchStudentFrame:
    def __init__(self, frame):
        self.search_frame = frame

        self.studclass = Student()
        self.data = self.studclass.data
        self.filename = self.studclass.filename

        # Search
        self.search_bar_entry = Entry(self.search_frame, highlightthickness=2, highlightbackground="#A5678E",
                                      font=("Tw Cen MT", 18))
        self.srch_btn_img = PhotoImage(file=r"search_button_img.png")
        self.srch_result_msg = Label(self.search_frame, text="", bg="#E9B7D4", fg="#C0B9DB", font=("Comic Sans MS", 12))
        self.search_result_frame = Frame(self.search_frame, bg="#E9B7D4", highlightbackground="#A5678E", highlightthickness=2,)
        scrll_x = Scrollbar(self.search_result_frame, orient=HORIZONTAL)
        self.results_table = ttk.Treeview(self.search_result_frame, xscrollcommand=scrll_x.set,
                                          columns=("name", "course", "year", "gender"))

        scrll_x.pack(side=BOTTOM, fill=X)
        scrll_x.config(command=self.results_table.xview)
        self.results_table.heading("name", text="Name")
        self.results_table.heading("course", text="Course")
        self.results_table.heading("year", text="Year")
        self.results_table.heading("gender", text="Gender")
        self.results_table['show'] = 'headings'
        self.results_table.column("name", width=140)
        self.results_table.column("course", width=60)
        self.results_table.column("year", width=60)
        self.results_table.column("gender", width=50)

        self.srchrslts_label = Label(self.search_frame, text="  Search Result", anchor='w', bg="#C0B9DB", fg="#343535",highlightbackground="#A5678E", highlightthickness=1,
                                     font=("Tw Cen MT", 18))

        self.search_frame.place(x=140, y=160, width=300, height=415,)
        id_no_label = Label(self.search_frame, text="Search with ID Number", bg="#C0B9DB", fg="#343535", highlightbackground="#A5678E", highlightthickness=2, font=("Comic Sans MS", 16))
        id_no_label.place(x=30, y=25, width=250, height=40)
        self.search_bar_entry.place(x=30, y=80, width=250, height=40)
        search_button = Button(self.search_frame, command=self.search_student,
                               image=self.srch_btn_img, bg="#C0B9DB", fg="#C0B9DB", font=("Tw Cen MT", 20))
        search_button.place(x=240, y=80, width=40, height=40)

        self.cover = Frame(self.search_frame, bg="#E9B7D4")

        
        self.search_bar_entry.delete(0, END)

    def search_student(self):
        if self.studclass.id_checker(self.search_bar_entry.get()):
            self.srch_result_msg.place(x=30, y=125, height=20, width=150)
            self.cover.place_forget()

            if self.search_bar_entry.get() in self.data:
                stud = list(self.data[self.search_bar_entry.get()].values())
                self.results_table.delete(*self.results_table.get_children())
                self.srch_result_msg.config(text="1 record found", fg="#343535")
                self.srchrslts_label.place(x=10, y=150, width=280, height=35)
                self.search_result_frame.place(x=10, y=180, width=280, height=200)
                self.results_table.insert('', 'end', values=[stud[0], stud[1], stud[2], stud[3]])
                self.results_table.pack(fill=BOTH, expand=1)
                return
            else:
                self.srchrslts_label.place_forget()
                self.search_result_frame.place_forget()
                self.srch_result_msg.config(text="No records found", fg="#343535")
                return
        return

class AddStudentFrame:
    def __init__(me, frame, table):
        me.add_frame = frame
        me.display_table = table

        me.studclass = Student()
        me.data = me.studclass.data
        me.filename = me.studclass.filename

        me.id_no = StringVar()
        me.name = StringVar()
        me.course = StringVar()
        me.year = StringVar()
        me.gender = StringVar()

        me.add_name_entry = Entry(me.add_frame, textvariable=me.name, highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 20))

        me.add_id_entry = Entry(me.add_frame, textvariable=me.id_no, highlightthickness=2,
                                  highlightbackground="#C0B9DB", font=("Tw Cen MT", 20))
        me.add_year_combo = ttk.Combobox(me.add_frame, textvariable=me.year, font=("Tw Cen MT", 20),
                                           values=[
                                               "1st Year",
                                               "2nd Year",
                                               "3rd Year",
                                               "4th Year",
                                               "5th Year"])
        me.add_course_entry = Entry(me.add_frame, textvariable=me.course, highlightthickness=2,
                                      highlightbackground="#C0B9DB", font=("Tw Cen MT", 18))
        me.add_gender_combo = ttk.Combobox(me.add_frame, textvariable=me.gender, font=("Tw Cen MT", 20),
                                             values=["Male", "Female", "Other"])

        # add_student_interface
        me.add_frame.place(x=140, y=160, width=300, height=415)

        # attributes of the add student feature
        name_label = Label(me.add_frame, text="Name:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        name_label.place(x=20, y=50, width=90, height=40)
        me.add_name_entry.place(x=110, y=50, width=180, height=40)
        id_no_label = Label(me.add_frame, text="ID No.:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        id_no_label.place(x=20, y=120, width=90, height=40)
        name_format = Label(me.add_frame, text="Last Name, First Name, M.I", font=("Comic Sans MS", 10), fg="#343535",
                            bg="lightblue")
        name_format.place(x=115, y=91, height=20)
        me.add_id_entry.place(x=110, y=120, width=180, height=40)
        year_label = Label(me.add_frame, text="Year:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        year_label.place(x=20, y=170, width=90, height=40)
        me.add_year_combo.place(x=110, y=170, width=180, height=40)
        course_label = Label(me.add_frame, text="Course:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        course_label.place(x=20, y=220, width=90, height=40)
        me.add_course_entry.place(x=110, y=220, width=180, height=40)
        gender_label = Label(me.add_frame, text="Gender:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        gender_label.place(x=20, y=270, width=90, height=40)
        me.add_gender_combo.place(x=110, y=270, width=180, height=40)

        # buttons on add student
        add_info_button = Button(me.add_frame, command=me.add_student, text="Add", bg="#C0B9DB", fg="#343535",
                                 font=("Tw Cen MT", 20))
        add_info_button.place(x=30, y=340, width=90, height=30)
        clear_info_button = Button(me.add_frame, command=me.clear_data, text="Clear", bg="#C0B9DB", fg="#343535",
                                   font=("Tw Cen MT", 20))
        clear_info_button.place(x=180, y=340, width=90, height=30)

    def clear_data(me):
        me.add_id_entry.delete(0, END)
        me.add_name_entry.delete(0, END)
        me.add_course_entry.delete(0, END)
        me.add_year_combo.delete(0, END)
        me.add_gender_combo.delete(0, END)

    def add_student(me):
        msg = messagebox.askquestion('Add Student', 'Are you sure you want to add the student?')
        if msg == "yes":
            if me.name.get() == "" or me.id_no.get() == "" or me.year == "" or me.course.get() == "" \
                    or me.gender.get() == "":
                messagebox.showerror("Error", "Please fill out all fields")
            elif me.studclass.id_checker(me.id_no.get()):
                if me.id_no.get() in me.data:
                    overwrite = messagebox.askquestion('Overwrite Student', 'ID Number already in database, do you '
                                                                            'wish to overwrite the student information?'
                                                       )
                    if overwrite == "no":
                        return

                me.data[me.id_no.get()] = {'Name': me.name.get().upper(),
                                               'Course': me.course.get().upper(),
                                               'Year': me.year.get(), 'Gender': me.gender.get()}
                me.studclass.data_to_csv()
                messagebox.showinfo("Success!", "Student added to database!")
                me.studclass.display_student_table(me.display_table)
                me.clear_data()
            return
        else:
            return

class DeleteStudentFrame:
    def __init__(self, frame, table):
        self.delete_frame = frame
        self.display_table = table

        self.stud_class = Student()
        self.data = self.stud_class.data

        self.id_no = StringVar()
        self.name = StringVar()
        self.course = StringVar()
        self.year = StringVar()
        self.gender = StringVar()
        self.rows = []
        self.select = False

        # Delete Frame
        self.del_stud_name = Label(self.delete_frame, fg="black", bg="white",highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 16), anchor='w')
        self.del_stud_id = Label(self.delete_frame, fg="black", bg="white",highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 16), anchor='w')
        self.del_stud_year = Label(self.delete_frame, fg="black", bg="white",highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 16), anchor='w')
        self.del_stud_course = Label(self.delete_frame, fg="black", bg="white",highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 16),
                                     anchor='w')
        self.del_stud_gender = Label(self.delete_frame, fg="black", bg="white",highlightthickness=2,
                                    highlightbackground="#C0B9DB", font=("Tw Cen MT", 16),
                                     anchor='w')

        self.delete_frame.place(x=140, y=160, width=300, height=415)
        choose_lbl = Label(self.delete_frame, text="Select Student to Delete", anchor='w', fg="#343535", bg="lightblue",
                           font=("Comic Sans MS", 14))
        choose_lbl.place(x=40, y=30, width=220, height=30)
        choose_stud_btn = Button(self.delete_frame, command=self.select_stud,
                                 text="Select", bg="#C0B9DB", fg="#343535", font=("Tw Cen MT", 20))
        choose_stud_btn.place(x=30, y=350, width=90, height=30)

        name_label = Label(self.delete_frame, text="Name:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        name_label.place(x=20, y=80, width=90, height=40)
        id_no_label = Label(self.delete_frame, text="ID No.:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        id_no_label.place(x=20, y=130, width=90, height=40)
        year_label = Label(self.delete_frame, text="Year:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        year_label.place(x=20, y=180, width=90, height=40)
        course_label = Label(self.delete_frame, text="Course:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        course_label.place(x=20, y=230, width=90, height=40)
        gender_label = Label(self.delete_frame, text="Gender:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        gender_label.place(x=20, y=280, width=90, height=40)

        delete_button = Button(self.delete_frame, command=self.delete_student, text="Delete", bg="#C0B9DB", fg="#343535",
                               font=("Tw Cen MT", 20))
        delete_button.place(x=180, y=350, width=90, height=30)

        self.del_stud_name.place(x=110, y=80, width=180, height=40)
        self.del_stud_id.place(x=110, y=130, width=180, height=40)
        self.del_stud_year.place(x=110, y=180, width=180, height=40)
        self.del_stud_course.place(x=110, y=230, width=180, height=40)
        self.del_stud_gender.place(x=110, y=280, width=180, height=40)

    def clear_data(self):
        self.del_stud_name.config(text="")
        self.del_stud_id.config(text="")
        self.del_stud_course.config(text="")
        self.del_stud_year.config(text="")
        self.del_stud_gender.config(text="")

    def delete_student(self):
        if not self.select:
            messagebox.showerror("Error", "Select a student first")
            return
        else:
            msg = messagebox.askquestion('Delete Student', 'Are you sure you want to delete the student?')
            if msg == "yes":
                self.data.pop(self.rows[0], None)
                self.stud_class.data_to_csv()
                messagebox.showinfo("Success!", "Student has been deleted!")
                self.stud_class.display_student_table(self.display_table)
                self.clear_data()

                return
            else:
                return

    def select_stud(self):
        cursor_row = self.display_table.focus()
        contents = self.display_table.item(cursor_row)
        rows = contents['values']

        if rows == "":
            messagebox.showerror("Error", "Select a student first")
            self.select = False
            return
        else:
            self.del_stud_name.config(text=rows[1])
            self.del_stud_id.config(text=rows[0])
            self.del_stud_year.config(text=rows[3])
            self.del_stud_course.config(text=rows[2])
            self.del_stud_gender.config(text=rows[4])
            self.rows = rows
            self.select = True
            return

class EditStudentFrame:
    def __init__(self, frame, table):
        self.edit_frame = frame
        self.display_table = table

        self.stud_class = Student()
        self.data = self.stud_class.data
        self.filename = self.stud_class.filename

        self.id_no = StringVar()
        self.name = StringVar()
        self.course = StringVar()
        self.year = StringVar()
        self.gender = StringVar()
        self.rows = []
        self.select = False

        # Edit
        self.edit_name_entry = Entry(self.edit_frame, textvariable=self.name, highlightthickness=2,
                                     highlightbackground="#C0B9DB", font=("Tw Cen MT", 20))
        self.edit_id_entry = Entry(self.edit_frame, textvariable=self.id_no, highlightthickness=2,
                                   highlightbackground="#C0B9DB", font=("Tw Cen MT", 20))
        self.edit_year_combo = ttk.Combobox(self.edit_frame, textvariable=self.year, font=("Tw Cen MT", 20),
                                            values=[
                                                "First Year",
                                                "Second Year",
                                                "Third Year",
                                                "Fourth Year",
                                                "Fifth Year"])
        self.edit_course_entry = Entry(self.edit_frame, textvariable=self.course, font=("Tw Cen MT", 18),
                                       highlightthickness=2, highlightbackground="#C0B9DB")
        self.edit_gender_combo = ttk.Combobox(self.edit_frame, textvariable=self.gender, font=("Tw Cen MT", 20),
                                              values=["Male", "Female", "Other"])

        self.edit_frame.place(x=140, y=160, width=300, height=415)

        # GUI for selecting student to be updated
        choose_label = Label(self.edit_frame, text="Select Student to Edit", anchor='w', fg="#343535", bg="lightblue",
                             font=("Comic Sans MS", 14))
        choose_label.place(x=40, y=30, width=220, height=30)
        choose_stud_btn = Button(self.edit_frame, command=self.select_stud,
                                 text="Select", bg="#C0B9DB", fg="#343535", font=("Tw Cen MT", 20))
        choose_stud_btn.place(x=20, y=360, width=90, height=30)

        # attributes on edit student feature
        name_format = Label(self.edit_frame, text="Last Name, First Name, M.I", font=("Comic Sans MS", 10), fg="#343535",
                            bg="lightblue")
        name_format.place(x=115, y=121, height=20)
        name_label = Label(self.edit_frame, text="Name:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        name_label.place(x=20, y=80, width=90, height=40)
        self.edit_name_entry.place(x=110, y=80, width=180, height=40)
        id_no_label = Label(self.edit_frame, text="ID No.:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        id_no_label.place(x=20, y=150, width=90, height=40)
        self.edit_id_entry.place(x=110, y=150, width=180, height=40)
        year_label = Label(self.edit_frame, text="Year:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        year_label.place(x=20, y=200, width=90, height=40)
        self.edit_year_combo.place(x=110, y=200, width=180, height=40,)
        course_label = Label(self.edit_frame, text="Course:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        course_label.place(x=20, y=250, width=90, height=40)
        self.edit_course_entry.place(x=110, y=250, width=180, height=40)
        gender_label = Label(self.edit_frame, text="Gender:", font=("Tw Cen MT", 20), bg="#C0B9DB", fg="#343535")
        gender_label.place(x=20, y=300, width=90, height=40)
        self.edit_gender_combo.place(x=110, y=300, width=180, height=40)

        # buttons for add student feature
        update_info_button = Button(self.edit_frame, command=self.update_student, text="Update", bg="#C0B9DB",
                                    fg="#343535", font=("Tw Cen MT", 20))
        update_info_button.place(x=110, y=360, width=90, height=30)
        clear_info_button = Button(self.edit_frame, command=self.clear_data, text="Clear", bg="#C0B9DB", fg="#343535",
                                   font=("Tw Cen MT", 20))
        clear_info_button.place(x=200, y=360, width=90, height=30)

    def clear_data(self):
        self.edit_id_entry.delete(0, END)
        self.edit_name_entry.delete(0, END)
        self.edit_year_combo.delete(0, END)
        self.edit_course_entry.delete(0, END)
        self.edit_gender_combo.delete(0, END)

    def update_student(self):
        if not self.select:
            messagebox.showerror("Error", "Select a student first")
            return
        else:
            msg = messagebox.askquestion("Update Student", "Are you sure you want to update the student's information?")
            if msg == "yes":
                if self.name.get() == "" or self.id_no.get() == "" or self.year == "" or self.course.get() == "" \
                        or self.gender.get() == "":
                    messagebox.showerror("Error", "Please fill out all fields")

                elif self.stud_class.id_checker(self.id_no.get()):
                    if self.id_no.get() in self.data and self.id_no.get() != self.rows[0]:
                        overwrite = messagebox.askquestion('Overwrite Student',
                                                           'ID Number already in database, do you '
                                                           'wish to overwrite the student information?'
                                                           )
                        if overwrite == "no":
                            return

                    if self.rows[0] in self.data:
                        self.data[self.rows[0]] = {'Name': self.name.get().upper(),
                                                   'Course': self.course.get().upper(),
                                                   'Year': self.year.get(), 'Gender': self.gender.get()}
                        self.data[self.id_no.get()] = self.data.pop(self.rows[0])
                        self.stud_class.data_to_csv()
                        messagebox.showinfo("Success!", "Student information has been updated!")
                        self.stud_class.display_student_table(self.display_table)
                        self.clear_data()
                return
            else:
                return

    def select_stud(self):
        cursor_row = self.display_table.focus()
        contents = self.display_table.item(cursor_row)
        rows = contents['values']
        self.clear_data()

        if rows == "":
            messagebox.showerror("Error", "Select a student first")
            self.select = False
            return
        else:
            self.edit_name_entry.insert(0, rows[1])
            self.edit_id_entry.insert(0, rows[0])
            self.edit_year_combo.insert(0, rows[3])
            self.edit_course_entry.insert(0, rows[2])
            self.edit_gender_combo.insert(0, rows[4])
            self.rows = rows
            self.select = True
            return

class StudentGUI:
    def __init__(self, frame):
        self.frame = frame
        self.frame.geometry("1155x650")

        self.studclass = Student()

        

        # background frames
        
        bg1_frame = Frame(self.frame, bg="#797EF6")
        bg1_frame.place(x=7.5, y=7.5, width=1140, height=635)
        
  

        #  Layout for left frame
        self.left_frame = Frame(bg1_frame, bd=2, bg="#797EF6")
        self.left_frame.place(x=50, y=95, width=300, height=700)
        self.sis_label = Label(bg1_frame, text="STUDENT INFORMATION SYSTEM", bg="#797EF6", fg="#1AA7EC")
        self.home_img = PhotoImage(file="home_button_img.png")
        self.home_button = Button(bg1_frame, command=self.homepage, image=self.home_img, bg="#797EF6",)

        self.bg_box = Label(self.left_frame, bg="#797EF6", highlightbackground="#797EF6", highlightthickness=2)
        self.bg_box.place(x=50, y=50, width=400, height=390)
        

        self.add_frame = Frame( bg="#99FADC", highlightbackground="#A5678E", highlightthickness=2)
        self.edit_frame = Frame( bg="#99FADC",highlightbackground="#A5678E", highlightthickness=2)
        self.delete_frame = Frame( bg="#99FADC",highlightbackground="#A5678E", highlightthickness=2)
        self.search_frame = Frame( bg="#99FADC",highlightbackground="#A5678E", highlightthickness=2)

        self.head_bldsgn_img = PhotoImage(file=r"label_design.png")
        self.heading_label = Label( bg="#E9B7D4", fg="#343535", anchor='sw',highlightbackground="#705F93",highlightthickness=2, font=("Tw Cen MT", 24, BOLD))
        self.heading_lbldsgn = Label(self.left_frame, image=self.head_bldsgn_img, bg="#A5678E",
                                     fg="#99FADC",highlightbackground="#7FACD6",highlightthickness=2, anchor='sw', font=("Tw Cen MT", 24))

        # Navigation buttons
        self.add_button_img = PhotoImage(file=r"addstudent.png").subsample(6, 6)
        self.edit_button_img = PhotoImage(file=r"editstudent.png").subsample(6, 6)
        self.delete_button_img = PhotoImage(file=r"deletestudent.png").subsample(6, 6)
        self.search_button_img = PhotoImage(file=r"searchstudent.png").subsample(6, 6)
        self.add_stud_button = Button( image=self.add_button_img, bg="#797EF6",
                                      command=self.add_student_gui)
        self.edit_stud_button = Button( image=self.edit_button_img, bg="#797EF6",
                                       command=self.edit_student_gui)
        self.delete_stud_button = Button( image=self.delete_button_img, bg="#797EF6",
                                         command=self.delete_student_gui)
        self.search_stud_button = Button( image=self.search_button_img, bg="#797EF6",
                                         command=self.search_student_gui)
         
        # right_frame
        self.right_frame = Frame(bg1_frame, bg="#797EF6")
        self.right_frame.place(x=350, y=140, width=1000, height=550)
        self.display_label = Label( bg="#7FACD6", fg="#99FADC", anchor='w', font=("Tw Cen MT", 24),)
        self.display_lbldsgn = Label( image=self.head_bldsgn_img, bg="#7FACD6", fg="#99FADC",
                                     anchor='sw')
        self.about_frame = Frame( bg="#99FADC", highlightbackground="#7FACD6",
                                 highlightthickness=2)
        self.display_table_frame = Frame( bg="#99FADC", highlightbackground="#7FACD6",
                                         highlightthickness=2)

        self.about_bg = Label(self.about_frame, bg="#7FACD6", borderwidth=0)
        about = "this project is a simple student information system \nthat lets the user \n\n\u2713 add new students" \
                "\n\u2713 edit a student, \n\u2713 delete a student, and \n\u2713 search a student by id number. \n\n" 
        self.about = Text(self.about_frame, bg="#99FADC", fg="#33539E", highlightcolor="#99FADC",
                          highlightthickness=0, font=("Comic Sans MS", 13), relief=FLAT)
        self.about.insert(INSERT, about)
        self.about.config(state=DISABLED)
        self.author = Label(self.about_frame, fg="#33539E", bg="#99FADC", font=("Comic Sans MS", 12),
                            text="\u00A9 Jhon Ralfh Venecer Tercio", anchor='w')

        # Display data frame
        scroll_x = Scrollbar(self.display_table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.display_table_frame, orient=VERTICAL)
        self.display_table = ttk.Treeview(self.display_table_frame, xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set,  columns=("id_no", "name", "course", "year",
                                                                                 "gender"))
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.display_table.xview)
        scroll_y.config(command=self.display_table.yview)
        self.display_table.heading("id_no", text="ID Number")
        self.display_table.heading("name", text="Name")
        self.display_table.heading("course", text="Course")
        self.display_table.heading("year", text="Year")
        self.display_table.heading("gender", text="Gender")
        self.display_table['show'] = 'headings'
        self.display_table.column("id_no", width=80)
        self.display_table.column("name", width=230)
        self.display_table.column("course", width=150)
        self.display_table.column("year", width=80)
        self.display_table.column("gender", width=75)

        self.homepage()

    # Code for homepage
    def homepage(self):
        self.home_button.place_forget()
        self.display_table_frame.place_forget()
        
        self.heading_label.place_forget()
        self.heading_lbldsgn.place_configure()
        
        self.hide_frames()

        self.sis_label.config(font=("Tw Cen MT", 50), fg="#99FADC", borderwidth=2)
        self.sis_label.pack(anchor=CENTER, pady=20)
        

        self.add_stud_button.place(x=200, y=110, )
        self.edit_stud_button.place(x=400, y=110, )
        self.delete_stud_button.place(x=600, y=110, )
        self.search_stud_button.place(x=800, y=110, )

        self.about_frame.place(x=150, y=250, width=850, height=370)
        self.display_label.place(x=150, y=210, width=850, height=40)
        self.display_label.config(text="WHAT IS THIS?", font=("Tw Cen MT", 20, BOLD),fg= "#343535" )
        self.display_lbldsgn.place(x=900, y=210, width=100, height=40)
        self.about.place(x=40, y=25, width=550, height=280)
        self.author.place(x=30, y=320, width=250, height=40)
        self.display_table.pack_forget()

    # Display attributes common to different frames
    def display_attributes(self):
        self.sis_label.config(font=("Tw Cen MT", 30), fg="#99FADC")
        self.sis_label.place(x=80, y=10, height=50)

        self.home_button.place(x=23, y=90, width=88, height=88)

        self.about_frame.place_forget()

        self.display_table_frame.place(x=450, y=120, width=650, height=455)
        self.display_label.config(text="  STUDENTS' LIST")
        self.display_lbldsgn.place(x=1000, y=80, width=100, height=40)
        self.display_label.place(x=450, y=80, width=650, height=40)
        self.display_table.pack(fill=BOTH, expand=1)

        self.heading_label.place(x=140, y=120, width=300)
        self.heading_lbldsgn.place(x=310, y=100, width=100, height=40)

        self.studclass.display_student_table(self.display_table)

    # buttons
        self.add_stud_button.place(x=30, y=190)
        self.edit_stud_button.place(x=30, y=290, )
        self.delete_stud_button.place(x=30, y=390)
        self.search_stud_button.place(x=30, y=490)

    # Hide frames whenever using another
    def hide_frames(self):
        self.add_frame.place_forget()
        self.edit_frame.place_forget()
        self.delete_frame.place_forget()
        self.search_frame.place_forget()

    def add_student_gui(self):
        self.heading_label.config(text="   ADD ")
        self.hide_frames()
        self.display_attributes()
        AddStudentFrame(self.add_frame, self.display_table)

    def edit_student_gui(self):
        # edit_student_interface
        self.heading_label.config(text="   EDIT ")
        self.hide_frames()
        self.display_attributes()
        EditStudentFrame(self.edit_frame, self.display_table)

    def search_student_gui(self):
        self.heading_label.config(text="   SEARCH")
        self.hide_frames()
        self.display_attributes()
        SearchStudentFrame(self.search_frame)

    def delete_student_gui(self):
        self.heading_label.config(text="    DELETE ")
        self.hide_frames()
        self.display_attributes()
        DeleteStudentFrame(self.delete_frame, self.display_table)


root = Tk()
ob = StudentGUI(root)
root.mainloop()
