import Tkinter as tk	   

class PathGraphics(tk.Frame):			  
	def __init__(self, obstacles, result, master=None):
		tk.Frame.__init__(self, master)  
		self.pack()			
		self.draw(obstacles, result)

	def draw(self, obstacles, result):
		C = tk.Canvas(self, height = 100+15*result[-1].pos[1], width = 100+15*result[-1].pos[0])
		
		for ob in obstacles:
			self.rect = C.create_polygon(10+15*ob[0][0], 10+15*ob[0][1], 10+15*ob[1][0], 10+15*ob[1][1], 10+15*ob[2][0], 10+15*ob[2][1], 10+15*ob[3][0], 10+15*ob[3][1],fill='#eee')
			C.grid(padx=10, pady=10)
			
		for i in range(0, len(result) - 1):
			self.line = C.create_line(10+15*result[i].pos[0], 10+15*result[i].pos[1], 10+15*result[i+1].pos[0], 10+15*result[i+1].pos[1], width = 2)
			C.grid(padx=10, pady=10)
   