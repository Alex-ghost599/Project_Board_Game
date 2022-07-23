#Liangyz
#2022/7/23  16:51

from tkinter import Tk
from tkinter.simpledialog import askinteger, askfloat, askstring
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename, askdirectory
from tkinter.messagebox import showinfo, showwarning, showerror

if __name__ == "__main__":
    #
    app = Tk()  #初始化GUI程序
    app.withdraw() #仅显示对话框，隐藏主窗口
    ##
    select_directory=askdirectory(title="请选择一个文件夹")
    ##
    app.destroy() #关闭GUI窗口，释放资源
