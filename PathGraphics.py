import Tkinter as tk	   

class PathGraphics(tk.Frame):			  
	def __init__(self, obstacles, result, master=None):
		tk.Frame.__init__(self, master)  
		self.pack()			
		self.draw(obstacles, result)

	def draw(self, obstacles, result):
		C = tk.Canvas(self, height=750, width=750)
		
		for ob in obstacles:
			self.rect = C.create_polygon(15*ob[0][0], 15*ob[0][1], 15*ob[1][0], 15*ob[1][1], 15*ob[2][0], 15*ob[2][1], 15*ob[3][0], 15*ob[3][1],fill='#eee')
			C.grid(ipadx=10, ipady=10)
			
		for i in range(0, len(result) - 1):
			self.line = C.create_line(15*result[i].pos[0], 15*result[i].pos[1], 15*result[i+1].pos[0], 15*result[i+1].pos[1])
			C.grid(ipadx=10, ipady=10)

# app = PathGraphics()		
# app.master.geometry("250x150")			   
# app.master.title('Sample application')   
# app.master.maxsize(1000, 400) 
# app.mainloop()   