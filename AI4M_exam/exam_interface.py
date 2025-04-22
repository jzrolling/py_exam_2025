import pickle as pk, numpy as np, pandas as pd, os, glob
import json, time, threading, asyncio, inspect
from pathlib import Path
from IPython.display import display, clear_output
import ipywidgets as widgets
import time
import threading

class ExamApp:

    def __init__(self,
                 time_limit=20,
                 qdict_file = '202504_exam_json.pk'):

        self.login = login_interface()
        self.qdict_file = qdict_file
        self.qdict = pk.load(open(self.qdict_file,'rb'))
        self.time_limit=time_limit #unit minutes
        self.timer = CountdownTimer(total_time=self.time_limit*60)
        self.finished=False
        self.wait=True
        self.info_tracker = {}
        self.current_question = 0
        self.out_file = self.qdict_file.replace('json','output')
        
        
        if 'permuted_id' in self.qdict:
            self.login._freeze()
            self.finished=True
        elif os.path.isfile(self.out_file):
            self.finished=True
        if not self.finished:
            self.permuted_id = np.random.permutation(np.arange(1,26))
            self.qdict['permuted_id'] = self.permuted_id
            self.qboxes = []
            for i in range(25):
                qid = self.qdict['permuted_id'][i]
                qstring = self.qdict[qid]['qpic']
                qtype = self.qdict[qid]['qtype']
                qopt = self.qdict[qid]['ans']
                qbox = qa_widget(qstring,qid,qopt,qtype)
                self.qboxes.append(qbox)
            
            self.forward_button = widgets.Button(description='下一道',style={'button_color':'lightgreen'})
            self.backward_button = widgets.Button(description='上一道',style={'button_color':'lightgrey'})
            self.early_bird_button = widgets.Button(description='我做完了，现在提交',disabled=False,
                                             style={'button_color':'lightgrey'},
                                             layout=widgets.Layout(width='auto',height='30px'))
            
            self.early_bird_warning = widgets.Textarea(value='倒计时结束后 \n 自动保存答题结果',
                                                       style={'font_size':'25px'},
                                                       layout=widgets.Layout(width='auto',height='70px'))
            self.early_bird = widgets.VBox([self.early_bird_warning,self.early_bird_button])
            
            self.button_panel = widgets.HBox([self.backward_button,self.forward_button])
            self.Qlayout = widgets.VBox([self.qboxes[self.current_question],self.button_panel],
                                        layout=widgets.Layout(width='80%'))
            
            self.layout = widgets.VBox([self.login.layout])
            display(self.layout)
            
            self.login.record_label.observe(self.update_login_interface,names='value')
            self.forward_button.on_click(self.click_forward)
            self.backward_button.on_click(self.click_backward)
            self.early_bird_button.on_click(self.early_bird_click)
            self.timer.run_stop.observe(self.timer_stop,names='value')
            
    def submit(self):
        for i in range(25):
            qid = self.qdict['permuted_id'][i]
            qstring = self.qdict[qid]['qpic']
            qtype = self.qdict[qid]['qtype']
            qopt = self.qdict[qid]['ans']
            q = self.qboxes[i]
            if qtype in ['MCQ-Single','BFQ']:
                ans = q.children[1].value
            else:
                ans = [x.value for x in q.children[1].children[1:]]
            self.info_tracker[qid] = ans
        pk.dump(self.info_tracker, open(self.out_file,'wb'))
        pk.dump(self.qdict,open(self.qdict_file,'wb'))
        self.finished = True
        self.forward_button.disabled=True
        self.backward_button.disabled=True
        clear_output()

    def timer_stop(self,change):
        self.finished=True
        self.early_bird_warning.value = '答题结束，辛苦了！'
        self.early_bird_warning.disabled=True
        self.early_bird_button.disabled=True
        self.submit()
        
    def update_login_interface(self,change):
        self.info_tracker['email'] = self.login.email1.value
        self.info_tracker['name'] = self.login.namebox.value
        self.info_tracker['lab'] = self.login.labbox.value
        self.timer.start()
        self.login.layout.children = [widgets.HBox([self.timer.time_display,
                                                    self.early_bird])]
        self.login.layout.layout = widgets.Layout()
        self.layout.children = [self.login.layout,self.Qlayout]
    
    def click_forward(self,b):
        if self.current_question<=23:
            self.current_question+=1
        else:
            self.current_question=0
        self.Qlayout.children = [self.qboxes[self.current_question],self.button_panel]
        
    def click_backward(self,b):
        if self.current_question>=1:
            self.current_question-=1
        else:
            self.current_question=24
        self.Qlayout.children = [self.qboxes[self.current_question],self.button_panel]

    def early_bird_click(self,b):
        if not self.finished and not self.wait:
            self.finished=True
            self.early_bird_warning.value = '答题结束，辛苦了！'
            self.early_bird_warning.disabled=True
            self.early_bird_button.disabled=True
            self.timer.pause()
            self.submit()
    
        if not self.finished and self.wait:
            self.early_bird_warning.value = '提交后不可撤回! \n 如果确认提交请再次点击提交按钮'
            self.early_bird_warning.style.text_color='red'
            self.early_bird_button.style.button_color='salmon'
            self.wait=False


class login_interface:

    def __init__(self):

        self.namebox = widgets.Text(description='姓名:',layout=widgets.Layout(width='95%')) 
        self.labbox = widgets.Text(description='实验室:',layout=widgets.Layout(width='95%')) 
        self.email1 = widgets.Text(description='邮箱:',layout=widgets.Layout(width='80%'))
        self.email1_button = widgets.Button(description="确认",layout=widgets.Layout(width='20%'))
        self.email2 = widgets.Text(description='邮箱确认:',layout=widgets.Layout(width='80%'),disabled=True)
        self.email2_button = widgets.Button(description="确认",layout=widgets.Layout(width='20%'),disabled=True)
        self.warning_box = widgets.Textarea(value='请输入姓名, 实验室, \n 以及个人邮箱地址并确认',
                                         style={'font_size':'25px'},layout=widgets.Layout(width='99%',height='125px'))
        self.reset_button = widgets.Button(description='重置',disabled=True,
                                            layout=widgets.Layout(width='50%',height='10%'))
        self.confirm_button = widgets.Button(description='继续',disabled=True,
                                             layout=widgets.Layout(width='50%',max_height='auto'))
        self.layout = widgets.VBox([self.namebox,self.labbox,
                                    widgets.HBox([self.email1,self.email1_button]),
                                    widgets.HBox([self.email2,self.email2_button]),
                                    self.warning_box,
                                    widgets.HBox([self.reset_button,self.confirm_button])],
                                    layout=widgets.Layout(border='2px solid gray',
                                                          width='50%')) 
        self.email1_button.on_click(self.record_first_email)
        self.email2_button.on_click(self.record_second_email)
        self.reset_button.on_click(self.reset)
        self.confirm_button.on_click(self.start)
        self.started=False
        self.record_label = widgets.Label(value='')
        self.wait = True
        self.reset('')
        
    def record_first_email(self,b):
        if '@' in self.email1.value:
            self.email1_button.disabled=True
            self.email2_button.disabled=False
            self.email2_button.style.button_color='lightgreen'
            self.email1.disabled=True
            self.email2.disabled=False
            self.warning_box.value='请再次输入邮箱地址并确认'
        else:
            self.warning_box.value='邮箱地址无效，请再次输入'

    def record_second_email(self,b):
        if '@' in self.email1.value and '@' in self.email2.value:
            if self.email1.value == self.email2.value:
                self.email2_button.disabled=True
                self.email2.disabled=True
                self.confirm_button.disabled=False
                self.confirm_button.style.button_color='orange'
                self.reset_button.disabled=False
                self.namebox.disabled=True
                self.labbox.disabled=True
                self.warning_box.value='即将开始答题，共计25道题，限时15分钟完成 \n 仅有一次机会! \n 确认开始请点击"继续"按钮'
            else:
                self.email1_button.disabled=True
                self.email2_button.disabled=False
                self.email1.disabled=True
                self.email2.disabled=False
        else:
            self.warning_box.value='邮箱地址无效，请再次输入'

    def reset(self,b):
        if not self.started:
            self.namebox.disabled=False
            self.labbox.disabled=False
            self.email1_button.disabled=False
            self.email1_button.style.button_color='lightgreen'
            self.email1.disabled=False
            self.warning_box.value = '请输入邮箱地址并确认'
            self.email2_button.disabled=True
            self.email2_button.style.button_color='lightgrey'
            self.email2.disabled=True
            self.confirm_button.disabled=True
            self.reset_button.disabled=True
            self.reset_button.style.button_color='lightgrey'
            self.confirm_button.style.button_color='lightgrey'
            self.started=False
            self.wait=True

    def _freeze(self):
        self.namebox.disabled=True
        self.labbox.disabled=True
        self.email1_button.disabled=True
        self.email1_button.style.button_color='lightgrey'
        self.email1.disabled=True
        self.warning_box.style.text_color='red'
        self.warning_box.value = '已有答题记录！'
        self.email2_button.disabled=True
        self.email2_button.style.button_color='lightgrey'
        self.email2.disabled=True
        self.confirm_button.disabled=True
        self.reset_button.disabled=True
        self.reset_button.style.button_color='lightgrey'
        self.confirm_button.style.button_color='lightgrey'
        self.started=False
        self.wait=True

    def start(self,b):
        if not self.started and not self.wait:
            self.started=True
            self.reset_button.disabled=True
            self.confirm_button.disabled=True
            self.record_label.value="let's do it!"
            
        if not self.started and self.wait:
            self.warning_box.value = '请注意仅有一次答题机会! \n 如果确认开始请再次点击"继续"按钮'
            self.warning_box.style.text_color='red'
            self.confirm_button.style.button_color='salmon'
            self.wait=False

def qa_widget(img_bytes, 
              qid, 
              choices,
              qtype='MCQ_Single'):
    fmt = 'png'
    stem = widgets.Image(value=img_bytes, 
                         format=fmt,
                         layout=widgets.Layout(width="80%",border='2px solid gray'))
    apanel = widgets.Label('-')
    if qtype=='MCQ-Single':
        apanel = widgets.RadioButtons(description='请选择一个正确答案:',
                                      index = len(choices),
                                      options=list(choices)+[''],
                                      layout=widgets.Layout(width="auto"))
    elif qtype=='MCQ-Multi':
        checkboxes = [widgets.Label('请选择一个或多个正确答案:')]
        for x in choices:
            checkboxes.append(widgets.Checkbox(description=x,value=False))
        apanel = widgets.VBox(checkboxes,layout=widgets.Layout(width="auto"))
    elif qtype=='BFQ':
        apanel = widgets.Text(description='请输入答案:',
                              layout=widgets.Layout(width="auto"))
    

    # --- combine and return -------------------------------------------------
    box = widgets.VBox([stem, apanel],
                       layout=widgets.Layout(align_items="flex-start",
                                             width="95%",
                                             border='2px solid gray',
                                             padding='10px',margin='10px'))
    return box


class CountdownTimer:
    def __init__(self, total_time=60):
        # 初始化组件
        self.total_time = total_time
        self.remaining_time = total_time
        self.is_running = False
        self.run_stop = widgets.Label('')
        
        # 创建可视化组件
        self.time_display = widgets.Label("⌛",
                                          style={'font_size':'60px'},
                                          layout=widgets.Layout(height='100px',padding='20px'))
        
        # 组装界面
        
    def update_display(self):
        """更新时间显示和进度条"""
        mins, secs = divmod(self.remaining_time, 60)
        if self.remaining_time < 60:
            color = 'red'
        else:
            color = 'black'
        self.time_display.style.text_color = color
        time_str = f"⌛{mins:02d}:{secs:02d}"
        self.time_display.value = time_str
        
    def start(self):
        """开始倒计时"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run_timer)
            self.thread.start()

    def pause(self):
        """暂停/恢复倒计时"""
        if self.is_running:
            self.is_running = False
        
    def run_timer(self):
        """计时器核心逻辑"""
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_display()
            
        if self.remaining_time <= 0:
            self.time_display.value = "⏰时间到！交卷啦！"
            self.is_running = False
            self.run_stop.value = 'Finished'
