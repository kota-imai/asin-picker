import PySimpleGUI as sg
import iniclient

sg.theme('Dark Blue 3')

config = iniclient.Config()
layout = [
    [sg.Text('Google chromeのバージョンを入力して下さい')],
    [sg.Text('version', size=(15, 1)), sg.InputText(config.get_version())],
    [sg.Submit(button_text='Save')]
]

window = sg.Window('設定', layout)
while True:
    event, values = window.read()

    if event is None:
        print('exit')
        break

    if event == 'Save':
        config.set_version(values[0])
        sg.popup('設定を保存しました。')
        window.close()

window.close()