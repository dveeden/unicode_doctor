#!/usr/bin/python3
from unicode_doctor import DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def make_guess(self):
    good_text = builder.get_object("input_good").get_text()
    bad_text = builder.get_object("input_bad").get_text()
    output_label = builder.get_object('output_label')

    if good_text == '' and bad_text =='':
        good_text = 'Café'
        bad_text = 'CafÃ©'
    elif good_text == bad_text:
        output_label.set_text("Good and Bad can not be equal.")
        return

    output_text = ''

    for doctor in [DecodeEncodeUnicodeDoctor, ForcedAsciiUnicodeDoctor]:
        for guess in doctor.make_guess(str_good=good_text, str_bad=bad_text):
            output_text += guess.issue + "\n"

    if output_text == '':
        output_text = 'No explanation found'
    output_label.set_text(output_text)


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("unicode_doctor.ui")

    main_window = builder.get_object("main_window")
    hb = builder.get_object("header_bar")
    main_window.set_titlebar(hb)

    check_button = builder.get_object("check_button")
    check_button.connect("clicked", make_guess)

    main_window.connect("delete-event", Gtk.main_quit)
    main_window.show_all()

    Gtk.main()
