import tuichat


def tuiserver():
    if __name__ == 'tuichat.__main__':
        serv = tuichat.Server()
        serv.main()


def tuiclient():
    if __name__ == 'tuichat.__main__':
        client = tuichat.Client()
        client.main()
