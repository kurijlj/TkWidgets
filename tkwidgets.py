# -*- coding: utf-8 -*-
#==============================================================================
# TkWidgets
#
#  Copyright (C) <yyyy> <Author Name> <author@mail.com>
#
# This file is part of TkWidgets.
#
# TkWidgets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TkWidgets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TkWidgets.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================


#==============================================================================
#
# <Put documentation here>
#
# <yyyy>-<mm>-<dd> <Author Name> <author@mail.com>
#
# * <programfilename>.py: created.
#
# Nice analogous colors
# #26d3b6 #2699d3
#==============================================================================


import tkinter as tk
import tk_tools as tkt


def _isodd(n: int):
	"""
	"""

	return bool(n & 1)


def _numerical_value_in_range(val, lower, upper):
	"""
	"""

	if lower <= val and upper >= val: return True

	return False


class DialScaleWidget(tk.Frame):
	"""
	"""

	canvas = {
		'width': 200,
		'height': 200,
		'sticky': tk.W+tk.E}
	dial = {
		'startx': 12,
		'starty': 12,
		'endx': 188,
		'endy': 188,
		'width': 20,
		'style': tk.ARC,
		'startangle': 90}
	dialtext = {
		'x': 100,
		'y': 100,
		'font': '-size 14',
		'justify': tk.CENTER}
	scale = {
		'from': 0,
		'to': 100,
		'showvalue': 0,
		'borderwidth': 1,
		'sliderlength': 15,
		'width': 15,
		'orientation': tk.HORIZONTAL,
		'sticky': tk.W+tk.E}

	# Some cool colors:
	# '#1ae0a5'
	# '#1ab8e0'
	# '#1a56e0'

	def __init__(self, parent=None, initval=0, color='#1a56e0', **options):
		tk.Frame.__init__(
			self,
			parent,
			borderwidth=1,
			padx=5, pady=5,
			**options)
		self.grid()

		# Don't forget to add rounding if you implement support for
		# floating point numbers.

		# Validate initial value. Must be in range [0, 100]. If out of
		# range raise OutOfRangeError.
		if not _numerical_value_in_range(initval, 0, 100):
			raise OutOfRangeError('Value out of range.')

		#self.dialVal = round((initval/100.0)*360.0)
		#self.dialTextVal = '{0} %'.format(initval)
		self.scaleVal = tk.IntVar()
		self.color = color

		self.cvs= tk.Canvas(self,
			width=DialScaleWidget.canvas['width'],
			height=DialScaleWidget.canvas['height'])

		self.cvs.grid (
			column=0,
			columnspan=3,
			row=0,
			sticky=DialScaleWidget.canvas['sticky'])

		self.sc = tk.Scale(
			self,
			from_=DialScaleWidget.scale['from'],
			to=DialScaleWidget.scale['to'],
			showvalue=DialScaleWidget.scale['showvalue'],
			orient=DialScaleWidget.scale['orientation'],
			command=self._reDrawDial,
			borderwidth=DialScaleWidget.scale['borderwidth'],
			sliderlength=DialScaleWidget.scale['sliderlength'],
			width=DialScaleWidget.scale['width'],
			variable=self.scaleVal)
 
		self.scaleVal.set(initval)
		self._reDrawDial(None)

		self.sc.grid(
			column=0,
			columnspan=3,
			row=1,
			sticky=DialScaleWidget.scale['sticky'])

		self.lb = tk.Label (self, text='0')
		self.lb.grid(column=0, row=2, sticky=tk.W)
		self.lb = tk.Label (self, text='50')
		self.lb.grid(column=1, row=2)
		self.lb = tk.Label (self, text='100')
		self.lb.grid(column=2, row=2, sticky=tk.E)

	def _drawDial(self):
		# Handle 100% value gracefully. For full circle we must draw
		# oval.
		if 100 == self.scaleVal.get():
			self.cvs.create_oval(
				DialScaleWidget.dial['startx'],
				DialScaleWidget.dial['starty'],
				DialScaleWidget.dial['endx'],
				DialScaleWidget.dial['endy'],
				fill=self.cvs.cget('background'),
				outline=self.color,
				width=DialScaleWidget.dial['width'])

		# Not an full circle so draw arc instead.
		else:
			self.cvs.create_arc(
				DialScaleWidget.dial['startx'],
				DialScaleWidget.dial['starty'],
				DialScaleWidget.dial['endx'],
				DialScaleWidget.dial['endy'],
				extent=self.dialVal,
				fill=self.cvs.cget('background'),
				outline=self.color,
				start=DialScaleWidget.dial['startangle'],
				width=DialScaleWidget.dial['width'],
				style=DialScaleWidget.dial['style'])

		self.cvs.create_text (
			DialScaleWidget.dialtext['x'],
			DialScaleWidget.dialtext['y'],
			justify=DialScaleWidget.dialtext['justify'],
			font=DialScaleWidget.dialtext['font'],
			text=self.dialTextVal)

	def _reDrawDial(self, val):
		# First clean the canvas.
		for obj in self.cvs.find_all():
			self.cvs.delete(obj)

		self.dialVal = round((self.scaleVal.get()/100.0)*360.0)
		self.dialTextVal = '{0} %'.format(self.scaleVal.get())

		self._drawDial()


class DataDisplayGrid(tkt.Grid):
	"""
	A table-like display widget
	"""
	def __init__(self, parent, num_of_columns: int, headers: list=None, **options):
		"""
		Initialization of the label grid object
	
		:param parent: the tk parent element of this frame
		:param num_of_columns: the number of columns contained of the grid
		:param headers: a list containing the names of the column headers
		"""
		super().__init__(parent, num_of_columns, headers, **options)
	
	def add_row(self, data: list):
		"""
		Add a row of data to the current widget
	
		:param data: a row of data
		:return: None
		"""
		# validation
		if self.headers:
			if len(self.headers) != len(data):
				raise ValueError
	
		offset = 0 if not self.headers else 1
		row = list()
		for i, element in enumerate(data):

			if not _isodd(len(self.rows)):
				label = tk.Label(self, text=str(element), bg='#26d3b6', relief=tk.GROOVE, padx=self.padding, pady=self.padding)
			else:
				label = tk.Label(self, text=str(element), relief=tk.GROOVE, padx=self.padding, pady=self.padding)

			label.grid(row=len(self.rows) + offset, column=i, sticky='E,W')
			row.append(label)
	
		self.rows.append(row)


class GUIApp(tk.Tk):
	"""
	"""

	def __init__(self, initval):
		tk.Tk.__init__(self)
		#self.mainWidget = DialScaleWidget(self, initval=initval)
		self.mainWidget = DataDisplayGrid(self, 3, ['Data1', 'Data2', 'Data3'])
		self.mainWidget.add_row([1, 2, 3])
		self.mainWidget.add_row([4, 5, 6])
		self.mainWidget.add_row([7, 8, 9])
