from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import bs4
import requests
from sqlite3 import *
import matplotlib.pyplot as plt

# QOTD
qotd = "https://www.brainyquote.com/quote_of_the_day"
res = requests.get(qotd)
data = bs4.BeautifulSoup(res.text, "html.parser")
info = data.find("img", {"class":"p-qotd"})
q = info["alt"]

# LOC and TEMP
resl = requests.get("https://ipinfo.io/")
loca = resl.json()
r = loca['country']
c = loca['city']
l = c+","+r
apik = "6f648dfbfd1acc96038eb5ce7d7c9e4a"
url = f"https://api.openweathermap.org/data/2.5/weather?q={l}&appid={apik}"
res = requests.get(url).json()
kel = res['main']['temp']
cel = round((kel - 273.15),2)
#---------------------------------------------------------
# add command
def f1():
	add_win.deiconify()
	sms.withdraw()
def f2():
	view_win.deiconify()
	sms.withdraw()
	vie()
def f3():
	ud_win.deiconify()
	sms.withdraw()
def f4():
	del_win.deiconify()
	sms.withdraw()

def f12():
	sms.deiconify()
	aw_ent_rno.delete(0,END)
	aw_ent_nm.delete(0,END)
	aw_ent_mrks.delete(0,END)
	add_win.withdraw()
def f22():
	vw_st_data.delete("1.0",END)
	sms.deiconify()
	view_win.withdraw()
def f32():
	sms.deiconify()
	ud_win.withdraw()
def f42():
	sms.deiconify()
	del_win.withdraw()
def sav():
	con = None
	try:
		con = connect("sman.db")
		cursor = con.cursor()
		sql = "insert into info values('%d','%s','%d')"
		r = int(aw_ent_rno.get())
		if r<=0:
			showerror("Error","Invalid Roll No.: Enter Roll No. greater than 0")
			aw_ent_rno.delete(0,END)
			aw_ent_rno.focus()
			return
		n = aw_ent_nm.get()
		if not n.isalpha():
			showerror("Error","Invalid Name: Enter Alphabets")
			aw_ent_nm.delete(0,END)
			aw_ent_nm.focus()
			return
		elif len(n)<2:
			showerror("Error","Invalid Name: Name can't consist 1 alphabet")
			aw_ent_nm.delete(0,END)
			aw_ent_nm.focus()
			return
		m = aw_ent_mrks.get()
		if (int(m) < 0) or (int(m) >= 100):
			showerror("Error","Invalid Marks: Marks should be between 0 to 100")
			aw_ent_mrks.delete(0,END)
			aw_ent_mrks.focus()
			return
		elif not m.isdigit():
			showerror("Error","Invalid Marks: Enter digits")
			aw_ent_mrks.delete(0,END)
			aw_ent_mrks.focus()
			return
		cursor.execute(sql % (r,n,int(m)))
		c = cursor.rowcount
		if c==0:
			showerror("Error","Roll No. does not exist")
		else:	
			showinfo("Success","Records Added")
		con.commit()
		aw_ent_rno.delete(0,END)
		aw_ent_nm.delete(0,END)
		aw_ent_mrks.delete(0,END)
	except ValueError:
		showerror("Error","Please Enter Positive Number")
		aw_ent_rno.delete(0,END)
		aw_ent_nm.delete(0,END)
		aw_ent_mrks.delete(0,END)
		aw_ent_rno.focus()
		con.rollback()
	except Exception as e:
		showerror("Error",str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()

def vie():
	con = None
	try:
		con = connect("sman.db")
		cursor = con.cursor()
		sql = "select * from info;"
		cursor.execute(sql)
		rows = cursor.fetchall()
		for rows in rows:
			vw_st_data.insert(INSERT,"rno: ")
			vw_st_data.insert(INSERT,rows[0])
			vw_st_data.insert(INSERT,"\tname: ")
			vw_st_data.insert(INSERT,rows[1])
			vw_st_data.insert(INSERT,"\t\tmarks: ")
			vw_st_data.insert(INSERT,rows[2])
			vw_st_data.insert(INSERT,"\n")
		con.commit()
	except Exception as e:
		con.rollback()
		showerror("Error",e)
	finally:
		if con is not None:
			con.close()
def up():
	con = None
	try:
		con = connect("sman.db")
		cursor = con.cursor()
		sql = "update info set name = '%s', marks = '%d' where rno = '%d'"
		r = int(uw_ent_rno.get())
		if r<=0:
			showerror("Error","Invalid Roll No.: Enter Roll No. greater than 0")
			uw_ent_rno.delete(0,END)
			uw_ent_rno.focus()
			return
		n = uw_ent_nm.get()
		if not n.isalpha():
			showerror("Error","Invalid Name: Enter Alphabets")
			uw_ent_nm.delete(0,END)
			uw_ent_nm.focus()
			return
		elif len(n)<2:
			showerror("Error","Invalid Name: Name can't consist 1 alphabet")
			uw_ent_nm.delete(0,END)
			uw_ent_nm.focus()
			return
		m = uw_ent_mrks.get()
		if (int(m) < 0) or (int(m) >= 100):
			showerror("Error","Invalid Marks: Marks should be between 0 to 100")
			uw_ent_mrks.delete(0,END)
			uw_ent_mrks.focus()
			return
		elif not (m.isdigit()):
			showerror("Error","Invalid Marks: Enter digits")
			uw_ent_mrks.delete(0,END)
			uw_ent_mrks.focus()
			return
		cursor.execute(sql % (n,int(m),r))
		c = cursor.rowcount
		if c==0:
			showerror("Error","Roll No. does not exist")
		else:	
			showinfo("Success","Records Updated")
		con.commit()
		uw_ent_rno.delete(0,END)
		uw_ent_nm.delete(0,END)
		uw_ent_mrks.delete(0,END)
	except ValueError:
		showerror("Error","Please Enter Positive Number")
		uw_ent_rno.delete(0,END)
		uw_ent_nm.delete(0,END)
		uw_ent_mrks.delete(0,END)
		uw_ent_rno.focus()
		con.rollback()
	except Exception as e:
		showerror("Error",str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
def de():
	con = None
	sql = "delete from info where rno = %d"
	try:
		
		con = connect("sman.db")
		cursor = con.cursor()
		dr = int(dw_ent_rno.get())
		cursor.execute(sql % (dr))
		c = cursor.rowcount
		if c == 0:
			showerror("Error","Roll No. does not exist")
		else:	
			msg = "Roll No."+str(dr)+" deleted"
			showinfo("Success",msg)
		con.commit()
		dw_ent_rno.delete(0,END)		
		dw_ent_rno.focus()
	except ValueError:
		showerror("Error","Please Enter Positive Number!")
		dw_ent_rno.delete(0,END)
		dw_ent_rno.focus()		
		con.rollback()
	except Exception as e:
		con.rollback()
		showerror("Error",str(e))
	finally:
		if con is not None:
			con.close()
		
def cha():
	con = None
	try:
		con = connect("sman.db")
		cursor= con.cursor()
		sql = "Select * from info"
		cursor.execute(sql)
		rows = cursor.fetchall()
		con.commit()
	except Exception as e:
		con.rollback()
		showerror("Error",e)
	finally:
		if con is not None:
			con.close()
	n=[]
	m=[]
	for rows in rows:
		n.append(rows[1])
		m.append(rows[2])
	plt.bar(n,m,width = 0.5)
	plt.xlabel("Name of Student")
	plt.ylabel("Marks")
	plt.title("Batch Information!")
	plt.legend(shadow = True)
	plt.show()
#--------------------------------------------
# MAIN WINDOW
sms = Tk()
sms.title("S.M.S")
sms.geometry("500x600+0+0")
f = ("Arial", 20, "bold")
sms_but_add = Button(sms, text = "Add", bd = 2, font = f, command = f1)
sms_but_add.pack(pady = 10) 
sms_but_vw = Button(sms, text = "View", bd = 2, font = f, command = f2)
sms_but_vw.pack(pady = 5) 
sms_but_upd = Button(sms, text = "Update", bd = 2, font = f, command = f3)
sms_but_upd.pack(pady = 5) 
sms_but_del = Button(sms, text = "Delete", bd = 2, font = f, command = f4)
sms_but_del.pack(pady = 5) 
sms_but_chart = Button(sms, text = "Chart", bd = 2, font = f,command = cha)
sms_but_chart.pack(pady = 5)
f2 = ("Arial", 11, "italic")
lt = "LOCATION :"+ l +"\t\t\t\tTemp :"+str(cel)+"°C"
sms_st_lt = ScrolledText(sms,width = 57, height = 3, font = f2)
sms_st_lt.place(x = 10, y = 470)
sms_st_lt.insert(INSERT,lt)
sms_st_lt.configure(state = 'disabled')
qu = "QOTD :" + q 
sms_st_qotd = ScrolledText(sms, width = 57, height = 3, font = f2)
sms_st_qotd.place(x = 10, y = 530)
sms_st_qotd.insert(INSERT,qu)
sms_st_qotd.configure(state = 'disabled')

# ADD WINDOW
add_win = Toplevel(sms)
add_win.title("Add St.")
add_win.geometry("500x600+0+0")
aw_lbl_rno = Label(add_win, text = "enter rno:", font = f)
aw_lbl_rno.pack(pady = 5)
aw_ent_rno = Entry(add_win, bd = 4, font = f)
aw_ent_rno.pack(pady = 5)
aw_lbl_nm = Label(add_win, text = "enter name:", font = f)
aw_lbl_nm.pack(pady = 5)
aw_ent_nm = Entry(add_win, bd = 4, font = f)
aw_ent_nm.pack(pady = 5)
aw_lbl_mrks = Label(add_win, text = "enter marks:", font = f)
aw_lbl_mrks.pack(pady = 5)
aw_ent_mrks = Entry(add_win, bd = 4, font = f)
aw_ent_mrks.pack(pady = 5)
aw_but_save = Button(add_win, text = "Save", font = f, command = sav)
aw_but_save.pack(pady = 10)
aw_but_back = Button(add_win, text = "Back", font = f, command = f12)
aw_but_back.pack(pady = 10)
add_win.withdraw()

# VIEW WINDOW
view_win = Toplevel(sms)
view_win.title("View St.")
view_win.geometry("500x600+0+0")
fo = ("Arial",13,"italic")
vw_st_data = ScrolledText(view_win, width = 42, height = 15, font = fo)
vw_st_data.pack(pady = 10)
vw_but_back = Button(view_win, text = "Back", font = f, command = f22)
vw_but_back.pack(pady = 5)
view_win.withdraw()

# UPDATE WINDOW
ud_win = Toplevel(sms)
ud_win.title("Update St.")
ud_win.geometry("500x600+0+0")
uw_lbl_rno = Label(ud_win, text = "enter rno:", font = f)
uw_lbl_rno.pack(pady = 10)
uw_ent_rno = Entry(ud_win, bd = 4, font = f)
uw_ent_rno.pack(pady = 10)
uw_lbl_nm = Label(ud_win, text = "enter name:", font = f)
uw_lbl_nm.pack(pady = 10)
uw_ent_nm = Entry(ud_win, bd = 4, font = f)
uw_ent_nm.pack(pady = 10)
uw_lbl_mrks = Label(ud_win, text = "enter marks:", font = f)
uw_lbl_mrks.pack(pady = 10)
uw_ent_mrks = Entry(ud_win, bd = 4, font = f)
uw_ent_mrks.pack(pady = 10)
uw_but_save = Button(ud_win, text = "Save", bd = 4, font = f, command = up)
uw_but_save.pack(pady = 10)
uw_but_back = Button(ud_win, text = "Back", bd = 4, font = f, command = f32)
uw_but_back.pack(pady = 10)
ud_win.withdraw()

# DELETE WINDOW
del_win = Toplevel(sms)
del_win.title("Delete St.")
del_win.geometry("500x600+0+0")
dw_lbl_rno = Label(del_win, text = "enter rno:", font = f)
dw_lbl_rno.pack(pady = 10)
dw_ent_rno = Entry(del_win, bd = 4, font = f)
dw_ent_rno.pack(pady = 10)
dw_but_save = Button(del_win, text = "Save", font = f,command = de)
dw_but_save.pack(pady = 10)
dw_but_back = Button(del_win, text = "Back", font = f, command = f42)
dw_but_back.pack(pady = 10)
del_win.withdraw()

sms.mainloop()