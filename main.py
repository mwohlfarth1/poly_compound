from typing import Tuple, List
import sys # for running this app strangely. see G

# drawin shit
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QPushButton, QMessageBox, QLineEdit)
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import QLine, Qt

# math and shit
import numpy as np
from numpy import NaN, ndarray
import matplotlib.pyplot as plt
from numpy.lib.polynomial import poly
import scipy as sp
import pandas as pd 

# copying the clipboard
import pyperclip as clipboard

# to suppress the RankWarning
import warnings

# for time
from datetime import datetime, timedelta

# python shits the bed if we put this as a class variable, so merry christmas global scope.
# i ass-ume this is a problem because I'm stupid, but who knows
points: List[Tuple] = []

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#- 

class Driver(QWidget):

    def __init__(self):
        super().__init__()

        # constrain some things
        self.window_width = 1600
        self.window_height = 900

        self.version = 0.1

        # and on the 7th day...
        self.create_window()
        self.create_labels()
        self.create_donation_button()
        self.create_help_button()
        self.create_input_boxes()

        # only track mouse coordinates when it's pressed down
        # NOTE: this is explicit when the implicit matches it already
        self.setMouseTracking(False)

        # summon a dead man to paint for us
        self.picasso = QPainter()

        # to hold the amt of time that we have after each rebase
        self.time_amts_after_rebases: List = []

        # so that we don't infinitely loop through things
        self.last_points_len = len(points)
        
        # show the window or sumn
        self.show()


# defining and creating windows and labels -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    def create_window(self):
        '''Create the window with a label'''

        # define the window
        self.setGeometry(300, 100, self.window_width, self.window_height)
        self.setWindowTitle(f'Poly Compound v{self.version}')


    def create_labels(self):
        '''Make some 'o dem labels.'''

        # define a label for the mouse position in regular format
        self.mouse_loc_label = QLabel(self)
        self.mouse_loc_label.resize(200, 40)
        self.mouse_loc_label.move(5, 100)

        # define a label for the mouse position in cartesian
        self.mouse_loc_cart_label = QLabel(self)
        self.mouse_loc_cart_label.resize(200, 40)
        self.mouse_loc_cart_label.move(5, 200)

        # define a label for me printing things
        self.my_printer = QLabel(self)
        self.my_printer.resize(500, 200)
        self.my_printer.move(5, 120)

        if hasattr(self, 'qt_sucks_big_dick'):
            self.my_printer.setText('Fuck QT')
            self.my_printer.setFont(QFont('Arial', 100))

        # define a label for printing the polynomial
        self.polynomial_label = QLabel(self)
        self.polynomial_label.resize(1000, 40)
        self.polynomial_label.move(200, self.window_height - 45)

        # define another printer
        self.my_printer2 = QLabel(self)
        self.my_printer2.resize(200, 40)
        self.my_printer2.move(10, 270)

        # define a label for putting the final TIME amount
        # TODO: change the name from box to label
        self.final_time_amt_box = QLabel(self)
        self.final_time_amt_box.resize(200, 40)
        self.final_time_amt_box.move(5, 50)

        # define a label for putting the final TIME value
        self.final_time_value_box = QLabel(self)
        self.final_time_value_box.resize(200, 40)
        self.final_time_value_box.move(5, 75)

        # define labels for explaining the inputs
        self.start_apy_label = QLabel(self)
        self.start_apy_label.resize(50, 25)
        self.start_apy_label.move(5, 10)
        self.start_apy_label.setText('Start APY:')

        self.start_time_label = QLabel(self)
        self.start_time_label.resize(55, 25)
        self.start_time_label.move(5, self.window_height - 35)
        self.start_time_label.setText('Start Time:')

        self.end_time_label = QLabel(self)
        self.end_time_label.resize(50, 25)
        self.end_time_label.move(self.window_width - 160, 10)
        self.end_time_label.setText('End Time:')

        self.end_apy_label = QLabel(self)
        self.end_apy_label.resize(50, 25)
        self.end_apy_label.move(self.window_width - 160, self.window_height - 35)
        self.end_apy_label.setText('End APY:')

        self.start_time_princ_label = QLabel(self)
        self.start_time_princ_label.resize(100, 25)
        self.start_time_princ_label.move(int(self.window_width / 2 - 45), 10)
        self.start_time_princ_label.setText('Start $MEMO:')

        self.end_time_price_label = QLabel(self)
        self.end_time_price_label.resize(100, 25)
        self.end_time_price_label.move(int(self.window_width / 2 + 165), 10)
        self.end_time_price_label.setText('End $TIME Price:')


    def create_donation_button(self):
        '''You know what this does.'''

        # define a button for people to say when they're done drawing points
        self.donation_button = QPushButton('Buy me a beer', self)
        self.donation_button.move(500, 10)
        self.donation_button.clicked.connect(self.on_donation_button_clicked)
        self.donation_button.show()


    def create_help_button(self):
        self.help_button = QPushButton('HELP!!!', self)
        self.help_button.move(600, 10)
        self.help_button.clicked.connect(self.on_help_button_clicked)
        self.help_button.show()


    def create_input_boxes(self):
        '''Creates the input boxes for time start, time end, apy start, apy 
        end.'''

        # top left
        self.start_apy_box = QLineEdit(self)
        self.start_apy_box.setGeometry(60, 10, 100, 25)
        self.start_apy_box.setText('69696')

        # bottom right
        self.end_apy_box = QLineEdit(self)
        self.end_apy_box.setGeometry(self.window_width - 110, self.window_height - 35, 100, 25)
        self.end_apy_box.setText('0')

        # bottom left
        self.start_time_box = QLineEdit(self)
        self.start_time_box.setGeometry(60, self.window_height - 35, 100, 25)
        self.start_time_box.setText('now')

        # top right
        self.end_time_box = QLineEdit(self)
        self.end_time_box.setGeometry(self.window_width - 110, 10, 100, 25)
        thirty_days_out = datetime.now() + timedelta(days=30)
        thirty_days_out_str = thirty_days_out.strftime('%m/%d/%Y %H:%M')
        self.end_time_box.setText(thirty_days_out_str)

        # create a box to enter the initial principle TIME
        self.init_princ_time_box = QLineEdit(self)
        self.init_princ_time_box.setGeometry(int(self.window_width / 2 + 25), 10, 100, 25)
        self.init_princ_time_box.setText('1.0')

        # create a box to enter the price of TIME at end_time
        self.end_time_price_box = QLineEdit(self)
        self.end_time_price_box.setGeometry(int(self.window_width / 2 + 250), 10, 100, 25)
        self.end_time_price_box.setText('2000.00')


# shit that gets run when things happen #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    def mouseMoveEvent(self, event):
        '''Called when the mouse is moved while clicked'''
        x_loc = event.x()
        y_loc = event.y()

        # record the current position but convert to cartesian before
        cartesian_point = self.to_bl_origin(x_loc, y_loc)
        points.append(cartesian_point)

        # print the mouse location
        #self.mouse_loc_label.setText(f'Mouse coords: ( {event.x()} , {event.y()} )')
        #self.mouse_loc_cart_label.setText(f'Mouse coords: ( {cartesian_point[0]} , {cartesian_point[1]} )')

        # trigger the paintEvent() since pyqt5 is a bitch and says we shouldn't
        # directly call paintEvent(). let me shoot myself you fucker!
        self.update()


    def on_donation_button_clicked(self):
        '''Runs when the Done button is clicked'''

        donation_box = QMessageBox(self)
        message = """I made this for free. If you feel like buying me a beer, here\'s an address you can send AVAX/TIME/MEMO to: \n\n0xF85CB785F3Aa1eaEF8901E687f54E680F7c082DE"""
        donation_box.about(self, 'Donate', message)

    
    def on_help_button_clicked(self):
        help_box = QMessageBox(self)
        # TODO: fix this so that I can actually collapse the function in vscode
        message = \
        """INPUTS:
        Start date/time: Enter the start date/time in the bottom left box
            Format: MM/DD/YYYY HH:MM
            Default: now

        End date/time: Enter the end date/time in the top right box
            Format: MM/DD/YYYY HH:MM
            Default: 30 days out from the start date/time

        Start APY: Enter the start APY in the top left box
            Default: 69696

        End APY: Enter the end APY in the bottom right box
            Default: 0

        Initial MEMO amount: Enter the initial MEMO amount in the box in the top middle
            Default: 1.0

        End $TIME Price: Enter the price of TIME/MEMO at the end time
            Default: 2000.00

USAGE:
        Click and drag to add points to the screen. Those points are used to generate a polynomial which best fits the points. That polynomial is used to calculate the apy and rebase rate for each of the rebases.

        The program will apply each of the rebase rates to your initial TIME amount and display that.

        To copy the current polynomial to your clipboard for pasting into other things: ctrl-c
        To remove all points that you've drawn: ctrl-z

COMMON PROBLEMS:
        "The program crashed." - Make sure you've got something in each of the input boxes and make sure that each of the inputs is properly formatted. If it still crashes, read the code and try to figure it out, or contact the developer. Please include a screenshot/copy of what the error message was.

        "The Final TIME Amt box says 'nan'" - this is because, for at least one of the rebase times, your polynomial does not have a value at that "x" value. Add some more points so that your polynomial (the black line) touches both the left and right sides of the screen. You can get away with not doing this, but this will definitely fix your problem.

        "My terminal outputs warnings" - you can ignore any RankWarnings or RuntimeWarnings (and probably any other warnings) you see. They don't really matter.

        "I have too much money and don't know what to do with it" - I know how stressful this can be. Don't worry. I can take it off your hands. Feel free to make a donation.
            """

        help_box.about(self, 'Help', message)


    def keyPressEvent(self, event):
        '''If Ctrl-C is pressed, copy the formatted polynomial to the 
        clipboard.
        '''
        global points # TODO: why do i need to use this here but not in other
                      # functions?

        # copy to clipboard if ctrl-c pressed
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            clipboard.copy(self.format_poly(self.calc_cart_polynomial(points)))

            self.my_printer2.setText('Polynomial copied to clipboard')

        # clear the points if ctrl-z pressed
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            points = []

            self.update()
            self.my_printer2.setText('Points cleared')


# shit that draws stuff #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    def paintEvent(self, event):
        '''The paintEvent function which is run whenever something happens.

        Not really sure what the something is.

        EDIT: one of the somethings is when we call update on the widget
        '''

        if len(points) > self.last_points_len: # only redraw if we have new points
            self.last_points_len = len(points)

            # begin (not sure you have to do this)
            self.picasso.begin(self)

            # call our function to draw the points and the polynonial
            self.drawPoints(self.picasso)
            self.draw_calculated_polynomial(self.picasso)
            self.draw_rebase_points(self.picasso)

            # stop drawing (this may trigger the program to dump the buffer to screen)
            self.picasso.end()

        # if we have points, we can calculate a real polynomial and get rebase
        # rates and stuff. DO do (haha) this every time because the user may
        # have entered a new value for one of the input boxes
        if len(points) > 0:
            # get the cartesian polynomial
            cart_poly = self.calc_cart_polynomial(points)

            # print the cartesian polynomial to the screen
            self.polynomial_label.setText('Polynomial: ' + 
                self.format_poly(cart_poly)
            )

            # calculate the rebases for the rebase rate over time
            self.rebase_rates = self.calc_rebase_rates(cart_poly)
            #print(self.rebase_rates)

            # only try to calculate this if we didn't get an error response
            # from the calc_rebase_rates function
            if self.rebase_rates is not None:
                final_time_amt = self.calc_time_amts_after_rebases()

                # display the final time amt
                self.final_time_amt_box.setText(f'Final $TIME: {final_time_amt:.6f}')

                # grab the final time price and print value
                final_price = float(self.end_time_price_box.text())
                self.final_time_value_box.setText(f'Final $TIME Value: ${(final_price * final_time_amt):.2f}')

                #print(self.time_amts_after_rebases)


    def drawPoints(self, picasso):
        '''Actually draw the point buffer to the screen.'''

        # create a pen writing red and a width of 10
        pen = QPen(Qt.red)
        pen.setWidth(10)

        # tell picasso which pen to use
        picasso.setPen(pen)

        if False:
            # draw a diagonal line to see if we can (we can)
            for i in range(1000):
                if i % 10 == 0:
                    x = y = i
                    picasso.drawPoint(x, y)

        # draw the points in the point buffer
        for point in points: 
            x, y = self.to_tl_origin(point[0], point[1]) # convert to original 
            picasso.drawPoint(x, y)
        

    def draw_calculated_polynomial(self, picasso):
        '''Calculates the polynomial based on the points we have and draws
        that polynomial'''

        # calculate a polynomial if we have enough data
        if len(points) > 10:
            # calculate the polynomial
            self.poly = self.calc_cart_polynomial(points)

            # set this pen to black and make it smaller
            pen2 = QPen(Qt.black)
            pen2.setWidth(5)
            picasso.setPen(pen2)

            # draw the polynomial if we've calculated it        
            for x in range(self.window_width):
                raw_y = int(np.polyval(self.poly, x)) 

                # don't try to draw infinite values
                if raw_y > 10000:
                    y = 10000 
                elif raw_y < -10000:
                    y = -10000
                else:
                    y = raw_y

                # need to convert to the pyqt5 coordinate system before we print
                original_csys_point = self.to_tl_origin(x, y)
                picasso.drawPoint(original_csys_point[0], original_csys_point[1])


    def draw_rebase_points(self, picasso):
        '''Draw the points that the rebases occur at'''
        # calculate a polynomial if we have enough data
        if hasattr(self, 'rebase_points'):
            # set this pen to blue and make it smaller
            pen = QPen(Qt.blue)
            pen.setWidth(5)
            picasso.setPen(pen)

            # draw the polynomial if we've calculated it        
            for x, y in self.rebase_points:
                if x > 10000:
                    x = 10000 
                elif x < -10000:
                    x = -10000

                if y > 10000:
                    y = 10000
                elif y < -10000:
                    y = -10000

                #print(f'rebase point: ({x}, {y})')
                # need to convert to original coordinate system
                orig_csys_pt = self.to_tl_origin(x, y)
                picasso.drawPoint(int(orig_csys_pt[0]), int(orig_csys_pt[1]))


# calculations related things #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#- 
    # TODO: remove this function
    def calc_graph_polynomial(self, points: List[Tuple], degree: int = 7) -> ndarray:
        '''Given the x's and y's of the points and the degree polynomial
        requested, return an ndarray of the coefficients for a polynomial
        which will visually fit the list of points drawn.

        @param points: a list of the points, where each point is a tuple.
        @param y: a list of the y points
        @param degree: the degree polynomial that we want to generate.
                       defaults to 7 because 7 would allow for the final 
                       inflection to match the initial inflection (it do go 
                       down now so it do go down then) and 7 is a good numba

                        # NOTE: proof of the above:
        '''

        # split the tuples into independent lists
        x = [x for x,y in points]
        y = [y for x,y in points]

        return np.polyfit(x, y, degree)

    
    def calc_cart_polynomial(self, points: List[Tuple], degree: int = 7) -> ndarray:
        '''Given the x's and y's of the points in the polynomial requested,
        return an ndarray of the coefficients. 

        @param points: the cartesian points
        NOTE: arguments are same as for calc_graph_polynomial. 
        '''

        x = [x for x,y in points]
        y = [y for x,y in points]

        return np.polyfit(x, y, degree)


    def calc_apy_at_point(self, polynomial: ndarray, x: float) -> float:
        '''Given the polynomial and the inputs in the boxes, calculates what
        the apy is at that point.

        @param polynomial: the polynomial (scaled to window size) for the
                           apy curve
        @param x: the x value of the point we want to evaluate

        @returns: the y value at the x, scaled to the apy in top left
                  minus the apy in the bottom right
        '''


        # scale the y to the start apy minus the end apy
        start_apy = float(self.start_apy_box.text())
        end_apy = float(self.end_apy_box.text())

        # get the raw value between 0 and window height
        raw_y = np.polyval(polynomial, x)

        # scale that raw value first to 0-1 and then to the apy delta
        zero_to_1 = raw_y / self.window_height 
        apy_at_point = zero_to_1 * (start_apy - end_apy)

        return apy_at_point

    
    # TODO: make the calculation correct?
    def calc_rebase_rate_for_apy(self, apy: float):
        '''Calculate the rebase rate for a particular apy.
        '''
        # so, the apy to apr formula is:
        # apy = (1 + rebase_rate) ^ (periods)
        # that means that the rebase rate is equal to:
        # rebase_rate = (apy ** (1 / periods)) - 1

        # NOTE: wonderland docs say that equation is: 
        # APY = (1 + rebase_rate)**1095
        # this isn't really true. if you take the rebase_rate of 0.62% for example,
        # (1 + 0.0062)**1095 is 869.606392807, which is definitely 86960% APY, but
        # not what we're looking for. therefore, you can't just
        # take the period'th root of the apy percentage and subtract 1.
        # you have to divide the apy by 100 first so we're dealing
        # with all decimals and not percentages and decimals

        periods = 365 * 3 # every 8 hours
        rebase_rate = ((apy / 100) ** (1 / periods)) - 1

        #print(f'apy -> rebase_rate: {apy} -> {rebase_rate} ')

        return rebase_rate 


    def calc_rebase_rates(self, polynomial: ndarray) -> List[float]:
        '''Calculate the rebase rate for each rebase in the curve.
        
        @polynomial: the polynomial representing the apy over time
        '''

        should_return_none = False

        # get start time as a datetime object
        start_time_text = self.start_time_box.text()
        if start_time_text == 'now' or start_time_text == '': # default to now
            start_time = datetime.now()

            # set background to white since this is a valid thing to have here
            self.start_time_box.setStyleSheet('QLineEdit { background: rgb(255, 255, 255); }')
        else:
            try:
                start_time = datetime.strptime(start_time_text, '%m/%d/%Y %H:%M')

                # if we didn't throw a ValueError, we should continue on and not
                # return None because of this line
                self.start_time_box.setStyleSheet('QLineEdit { background: rgb(255, 255, 255); }')
                should_return_none = False
            except ValueError as ve:
                # invalid text. set box to red and make sure we return None after
                # setting the other one
                self.start_time_box.setStyleSheet('QLineEdit { background: rgb(255, 0, 0); }')
                should_return_none = True

        # get end time as a datetime object
        end_time_text = self.end_time_box.text()
        if end_time_text == '': # default to 30 days out
            end_time = datetime.now()
            end_time = end_time + timedelta(days=30)
        else:
            try:
                end_time = datetime.strptime(end_time_text, '%m/%d/%Y %H:%M')

                # if we were successful and the previous line didn't throw a ValueError,
                # make the box white again
                self.end_time_box.setStyleSheet('QLineEdit { background: rgb(255, 255, 255); }')
            except ValueError as ve:
                # we will get ValueError if the text doesn't match the 
                # format we need. turn the box red and return and wait
                # for the next loop
                self.end_time_box.setStyleSheet('QLineEdit { background: rgb(255, 0, 0); }')
                return None

        # return None for the first one now if we need to. delayed this until now
        # so that we made sure to check the second box before returning None for 
        # the first
        if should_return_none:
            return None

        # find the delta between these two dates and times 
        delta = end_time - start_time

        # get the datetimes for each of the rebases in the time period
        rebase_datetimes = self.get_rebase_datetimes(start_time, end_time)

        # translate these rebase dates to x values
        rebase_deltas: List = [d - start_time for d in rebase_datetimes] # how far we've gone for each rebase
        rebase_delta_percents: List = [d / delta for d in rebase_deltas]
        rebase_xs = [percent * self.window_width for percent in rebase_delta_percents]

        # now, get the x, y pairs for these points so we can print them and see where they fall
        self.rebase_points = [(x, self.calc_apy_at_point(polynomial, x)) for x in rebase_xs]

        # now that we have rebase times as x values, we can just evaluate the rebase 
        # rate for each of the x values and then we'll know what rebase rates we
        # need to apply to the principle

        rebase_apys = [self.calc_apy_at_point(polynomial, x) for x in rebase_xs]

        rebase_rates = [self.calc_rebase_rate_for_apy(apy) for apy in rebase_apys]

        return rebase_rates


    def get_rebase_datetimes(self, start_time: datetime, end_time: datetime) -> List[datetime]:
        '''Given the start time of the time frame and end time of the time frame,
        returns a list of datetime objects: one for each rebase in the time frame.'''

        # find the first rebase date/time
        # TODO: make this different for different time zones
        if start_time.hour <= 7:
            first_rebase = start_time.replace(hour=7, minute=0, second=0, microsecond=0)
        elif start_time.hour <= 15:
            first_rebase = start_time.replace(hour=15, minute=0, second=0, microsecond=0)
        elif start_time.hour <= 23:
            first_rebase = start_time.replace(hour=23, minute=0, second=0, microsecond=0)
        else:
            # we are after 2300 hours, so bump to 0700 next day
            first_rebase = start_time.replace(hour=7, minute=0, second=0, day = start_time.day + 1, microsecond=0)

        # find every other rebase date/time
        rebase_dates: List[datetime] = []
        current_rebase_date = first_rebase
        while current_rebase_date < end_time:
            # record this date
            rebase_dates.append(current_rebase_date)

            # move to next date
            current_rebase_date = current_rebase_date + timedelta(hours=8)
        
        return rebase_dates


    def calc_time_amts_after_rebases(self) -> float:
        '''Take the initial principle of TIME and multiply it by all of the
        rebase rates through the time period in question.

        @return: returns the final time amt after all rebases applied
        '''

        # first, we need to clear the list from last time so we calculate
        # a new list
        self.time_amts_after_rebases = []

        current_time_amt = float(self.init_princ_time_box.text())
        for rebase_rate in self.rebase_rates:
            current_time_amt *= (1 + rebase_rate)
            self.time_amts_after_rebases.append(current_time_amt)

        return current_time_amt


# formatting/converting things #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#- 
    def format_poly(self, poly: ndarray) -> str:
        '''Return the polynomial formatted into ax^e + bx^e-1 + ...'''

        formatted_poly: str = ''
        for i, coeff in enumerate(poly):
            # poly is ordered biggest exponent to smallest so we need to flip it
            deg = len(poly) - i - 1 

            # add this coeff and deg pair
            formatted_poly += '{:.6e}'.format(coeff) + 'x^' + str(deg)

            if deg != 0:
                formatted_poly += ' + '

        return formatted_poly


    def to_bl_origin(self, x, y):
        '''Convert from top left origin to bottom left origin'''

        new_x = x
        new_y = self.window_height - y

        return (new_x, new_y)


    def to_tl_origin(self, x, y):
        '''Convert from bottom left origin to top left origin'''

        new_x = x   
        new_y = self.window_height - y

        return (new_x, new_y)


def main():
    app = QApplication(sys.argv)
    exe = Driver()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # wtf does this do? spawn a new thread and run this program in the 
    # thread and then kill the current thread? why would you do that? 
    # i don't get paid enough to know that i guess...
    main()