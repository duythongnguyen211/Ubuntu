import Skype4Py


if __name__ == '__main__':
    skype = Skype4Py.Skype()
    skype.Attach()
    print 'Your full name:', skype.CurrentUser.FullName
    print 'Your contacts:'
    for user in skype.Friends:
        if user.FullName == 'Thong Bui':
            skype.SendMessage(user.Handle, 'vl')
    chat = skype.Chat('Thong Bui')
