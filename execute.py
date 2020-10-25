import PySimpleGUI as sg

sg.theme('Dark Blue 3')
layout = [
    [sg.Text('検索する出品者のセラーIDとページ数を入力してください')],
    [sg.Text('出品者ID', size=(15, 1)), sg.InputText('')],
    [sg.Text('ページ数', size=(15, 1)), sg.InputText('')],
    [sg.Checkbox('非表示モード', default=False)],
    [sg.Submit(button_text='Go')]
]
window = sg.Window('ASIN Picker for Storefront', layout)

while True:
    INVALID_INPUT_MESSAGE = '出品者IDが不正です'
    CHROME_LAUNCHING = 'Google chromeを起動しています。'
    CROLLER_FAILED = '検索に失敗しました。\n出品者IDを確認してください'
    CROLLER_FINISHED = '検索が完了しました。'

    event, values = window.read()

    if event is None:
        break

    if event == 'Go':
        if values[0] == 'A1VC38T7YXB528':
            # marketplaceIDは弾く
            sg.popup(INVALID_INPUT_MESSAGE, title='error')
        elif len(values[0]) < 11 or len(values[0]) > 14:
            sg.popup(INVALID_INPUT_MESSAGE, title='error')
        elif str(values[0]).isalnum() == False:
            sg.popup(INVALID_INPUT_MESSAGE, title='error')
        else:
            sg.popup(CHROME_LAUNCHING, title='ASIN Picker For Storefront', auto_close=True)
            try:
                import scraper
                if values[1] is not None:
                    loop_count = int(values[1])
                else: 
                    loop_count = 10
                scraper.execute(sellerid=values[0], loop=int(loop_count), headless=values[2])
            except:
                scraper.remove_file(filekey=values[0])
                sg.popup(CROLLER_FAILED)


            sg.popup(CROLLER_FINISHED)
            window.close()

window.close()