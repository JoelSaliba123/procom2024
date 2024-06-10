import PySimpleGUI as sg
import numpy as np
from tabulate import tabulate

class Calculator:
    input1_num = np.array([])
    input2_num = np.array([])
    results    = np.array([])
    n_rows     = int
    n_rows1    = int
    n_col1     = int
    n_col      = int
    values     = []
    operator  = str
    operator_iter = False
    iterations = int
    window     = None

    def __init__(self):
        layout = [
            [sg.Checkbox('Vector/Matrix', key='vector_matrix', enable_events=True,disabled=False),
             sg.Checkbox('Scalar', key='scalar', enable_events=True, disabled=False),
             sg.Checkbox('Iterative', enable_events=True,key='iter',disabled=True),
             sg.Input(key='iter_num',size=(5, 1), enable_events=True,disabled=True)],
             [sg.Text('Rows 1:'), sg.InputText(size=(5, 1), key='rows', disabled=True),
             sg.Text('Columns 1:'), sg.InputText(size=(5, 1), key='columns', disabled=True),
             sg.Text('Rows 1:'), sg.InputText(size=(5, 1), key='rows1', disabled=True),
             sg.Text('Columns 1:'), sg.InputText(size=(5, 1), key='columns1', disabled=True),
             sg.Button('Fix',key='fix',disabled=True), 
             sg.Button('Clean row/col',key='clean',disabled=True)],
            [sg.Text('Enter your input:'), sg.InputText(key='input1',disabled=True, enable_events=True, visible=True)],
            [sg.Text('Enter your input:'), sg.InputText(key='input2',disabled=True,enable_events=True, visible=True)],
            [sg.Radio('Add[+]',group_id='operacion',enable_events=True,key='+',disabled=True),
             sg.Radio('Substract[-]', group_id='operacion',enable_events=True,key='-',disabled=True),
             sg.Radio('Product[x]', group_id='operacion',enable_events=True,key='*',disabled=True),
             sg.Radio('Division[/]', group_id='operacion',enable_events=True,key='/',disabled=True),
             sg.Radio('Dot Product[.]', group_id='operacion',enable_events=True,key='dot',disabled=True)],
             [sg.Button('Run',key='run_button',disabled=True),
             sg.Button('Cancel'),
             sg.Button('Clean all',key='clean_all',disabled=True)],
            [sg.Text('\nInput 1:', size=(25, 2), key='output_message'),
            sg.Text('\nInput 2:', size=(25, 2), key='output_message'),
            sg.Text('\nOutput:', size=(25, 2), key='output_message')],

            [sg.Multiline('', size=(25, 10), key='input1_tab',disabled=True),
             sg.Multiline('', size=(25, 10), key='input2_tab',disabled=True),
             sg.Multiline('', size=(25, 10), key='output',disabled=True)]
        ]
        self.window = sg.Window('Calculator', layout)

    ###############################33
    ## RUN
    #############################3
    def run(self):
        while True:
            self.event, self.values = self.window.read()

            if self.event == sg.WIN_CLOSED or self.event == 'Cancel':  # if user closes window or clicks cancel
                break

            self.window['scalar'].update(disabled=self.values['vector_matrix'])
            self.window['vector_matrix'].update(disabled=self.values['scalar'])

            
            if (not(self.values['scalar']) and not(self.values['vector_matrix'])):
                self.non_selected_mode()
            elif (self.values['scalar']): 
                self.scalar_mode()
            elif (self.values['vector_matrix']):
                self.matrix_mode()

            ###################################
            # EVENT HANDLER
            ###################################

            if (self.event == 'clean'):
                for x in ['input1','input2']:
                    self.window[x].update(value='', disabled=True)
                self.window['fix'].update(disabled=False)
            
            if (self.event == 'clean_all'):
                self.non_selected_mode()

            if (self.event == 'scalar'):
                if (self.values['scalar']):
                    self.window['input1'].update(value=self.init_texbox(1,1),disabled=False)
                    self.window['input2'].update(value=self.init_texbox(1,1),disabled=False)

            if (self.event == 'fix'):
                self.fix_pushed()
            
            if (self.event == '+'):
                self.operator = '+'

            if (self.event == '-'):
                self.operator = '-'

            if (self.event == '/'):
                self.operator = '/'

            if (self.event == '*'):
                self.operator = '*'
            
            if (self.event == 'dot'):
                self.operator = 'dot'

            if (self.event == 'run_button'):
                self.operate()
            
            if (self.event == 'iter'):
                if self.values['iter']:
                    self.operator_iter = self.values['iter']
                else:
                    self.clean_iters()

            if (self.operator_iter):
                self.iterations = self.values['iter_num']

        self.window.close()

    def init_texbox(self, row, columns):
        if (row+columns>2):
            str1 = '['
            str1 = str1 + ' , '*columns 
            str1 = str1 [0:-3]+ '] , '
            str1 = str1*row
            str1 = '[' + str1[0:-2] + ']' 
        else:
            str1 = '[]'
        return (str1)
    
    def non_selected_mode(self):
        for x in ['rows','columns','input1',
                  'input2','input1_tab','input2_tab',
                  'output','iter_num',
                  'rows1','columns1','+','-','*','/','dot']:
            self.window[x].update(value='',disabled=True)

        for x in ['+','-','*','/','dot','iter','run_button']:
            self.window[x].update(disabled=True)

        self.window['vector_matrix'].update(value=False,disabled=False)
        self.window['scalar'].update(value=False,disabled=False)
        self.window['fix'].update(disabled=True)
        self.window['clean'].update(disabled=True)
        self.window['clean_all'].update(disabled=True)
    
    def scalar_mode(self):

        for x in ['+','-','*','/','iter','run_button']:
            self.window[x].update(disabled=False)
        self.n_rows = 1
        self.n_col = 1
        self.n_rows1 = 1
        self.n_col1 = 1
        self.window['dot'].update(disabled=True)
        self.window['input1'].update(disabled=False)
        self.window['input2'].update(disabled=False)
        self.window['fix'].update(disabled=True)
        self.window['clean'].update(disabled=True)
        self.window['clean_all'].update(disabled=False)
        
        if (self.values['iter']):
            self.window['input2'].update(value='',disabled=True)
            self.window['dot'].update(disabled=True)
            self.window['iter_num'].update(disabled=False)
            self.window['/'].update(disabled=True)

        for x in ['rows','columns','rows1','columns1']:
            self.window[x].update(value='1', disabled=True)

    def matrix_mode(self):
        for x in ['iter_num','iter']:
            self.window[x].update(disabled=True)
        
        self.window['fix'].update(disabled=False)
        self.window['clean'].update(disabled=False)
        self.window['clean_all'].update(disabled=False)

        for x in ['rows','columns','rows1','columns1']:
            self.window[x].update(value=self.values[x], disabled=False)

    def fix_pushed(self):
        for x in ['+','-','*','/','dot','run_button']:
            self.window[x].update(disabled=False)

        self.n_rows = int(self.values['rows'])
        self.n_col  = int(self.values['columns'])
        self.n_rows1 = int(self.values['rows1'])
        self.n_col1  = int(self.values['columns1'])

        for x in ['rows','columns','rows1','columns1']:
            self.window[x].update(value=self.values[x], disabled=True)

        self.window['fix'].update(disabled=True)
        self.window['input1'].update(value=self.init_texbox(self.n_rows,self.n_col),disabled=False)
        self.window['input2'].update(value=self.init_texbox(self.n_rows1,self.n_col1),disabled=False)


    def show_matrix(self, data, output_layer):
        input =  tabulate(data.tolist(), tablefmt='grid') 
        self.window[output_layer].update(input)
    
    def clean_iters(self):
        self.window['input2'].update(value=self.init_texbox(self.n_rows1,self.n_col1),disabled=False)
        self.window['iter_num'].update(value='', disabled=True)
        self.operator_iter = False

    def operate(self):
        try:
            if self.operator in ['+','-','/']:
                if not(self.n_col == self.n_col1 and
                    self.n_rows == self.n_rows1):
                    raise Exception('Wrong matrix dimension')
                
            if self.operator in ['*']:
                if not(self.n_col == self.n_rows1):
                    raise Exception('Wrong matrix dimension')
                
        except Exception as e:
            sg.popup_error(e)
            return 0
        
        # Check if the inpt numbers are floats
        try:
            self.input1_num = np.array(eval(self.values['input1']))  
            size_input1 = np.shape(self.input1_num)
            if sum(size_input1)==1:
                size_input1 = [1,1]

            if not(self.operator_iter):
                self.input2_num = np.array(eval(self.values['input2']))
                size_input2 = np.shape(self.input2_num)
                if sum(size_input2)==1:
                    size_input2= [1,1]
        except Exception as e:
            sg.popup_error(e)
            return 0
        
        ## check if the matrix dimmension are equal to fixed ones
        try:
            if (size_input1[0]!=self.n_rows or size_input1[1]!=self.n_col):
                raise Exception('Wrong matrix dimention')

            if (not(self.operator_iter) and
                (size_input2[0]!=self.n_rows1 
                or size_input2[1]!=self.n_col1)):
                raise Exception('Wrong matrix dimention')

        except Exception as e:
            sg.popup_error(e)
            return 0
        
        ## Check if the value of iterations is an integer
        try:
            if self.operator_iter:
                self.iterations=eval(self.iterations)
        except Exception as e:
            sg.popup_error('Number of iterationsmust be an integer')
            return 0
        
        try:
            if (self.operator== '+'):
                if  self.operator_iter:
                    self.result = self.input1_num        
                    for i in range(self.iterations-1):
                        self.result = self.result + self.input1_num        
                else:
                    self.result = self.input1_num+self.input2_num
            elif (self.operator== '-'):
                if  self.operator_iter:
                    self.result = self.input1_num        
                    for i in range(self.iterations-1):
                        self.result = self.result - self.input1_num        
                else:
                    self.result = self.input1_num-self.input2_num
            elif (self.operator== '*'):
                if  self.operator_iter:
                    self.result = self.input1_num        
                    for i in range(self.iterations-1):
                        self.result = (self.result*self.input1_num)        
                else:
                    if (sum(size_input1)+sum(size_input2)==4):
                        self.result = (self.input1_num*self.input2_num)
                    else:   
                        self.result = np.matmul(self.input1_num,self.input2_num)

            elif (self.operator== '/'):
                self.result = self.input1_num/self.input2_num
            elif (self.operator== 'dot'):
                if 1 in np.shape(self.input1_num) and 1 in np.shape(self.input2_num):
                    self.result = [np.dot(self.input1_num.ravel(),
                                                  self.input2_num.ravel())]
                else:
                    self.result = np.dot(self.input1_num,self.input2_num)

        except Exception as e:
            sg.popup_error(e)
            return 0
            
        self.print_result()
    
            

    def print_result(self):
        if (len(self.input1_num)>1):
            input1 = tabulate(self.input1_num.tolist(), tablefmt='grid')
        else:
            input1 = self.input1_num
        
        if (len(self.input2_num)>1):
            input2 = tabulate(self.input2_num.tolist(), tablefmt='grid')
        else:
            input2 = self.input2_num

        if (len(self.result)>1):
            result = tabulate(self.result.tolist(), tablefmt='grid')
        else:
            result = self.result

        self.window['input1_tab'].update(input1)
        if not(self.operator_iter): 
            self.window['input2_tab'].update(input2)
        self.window['output'].update(result)


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
