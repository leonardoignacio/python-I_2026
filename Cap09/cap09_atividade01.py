import pyautogui as gui

opcao = gui.confirm('Escolha uma opção: ', buttons =['Excel', 'Word', 'Chrome'])
gui.hotkey('win', 'r')
gui.sleep(1)
exe=opcao
if exe=='Word':
    exe="C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"
gui.typewrite(exe)
gui.press('Enter')
gui.sleep(2)
gui.click(x=400, y=183)
gui.sleep(10)
gui.typewrite(f' {opcao} foi aberto automáticamante')

#print(gui.position())