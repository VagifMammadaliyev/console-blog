from os import system

from consoleblog.core.application import (map_, settings,
                                        lib, exceptions, session)
from consoleblog.pages.start_page import StartPage


class Engine(object):

    def start(self, start_page=StartPage()):
        system('clear')
        self.open(start_page)

    def open(self, page):
        print(settings.long_border)
        page = map_.Map.next_page(page)

        while 1:
            try:
                # show alert message (at the top of terminal's space)
                alerter = session.session.get_alerter()
                if alerter.has_message():
                    lib.print_alert(alerter.get_alert())

                next_page = page.show()
                system('clear')
                page = map_.Map.next_page(next_page)
            except exceptions.PageNotCompletedError as e:
                print(e.message)
                print('Terminating app...')
                break
                # handle it better yo!!!
            except EOFError:
                # define a way of terminating!!!
                print()
                lib.print_alert('Good bye!')
                break
            