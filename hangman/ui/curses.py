"""
An (n)curses applicaton of the hangman using the basic HangmanEngine.
"""

from __future__ import division
from hangman.core.engines import HangmanEngine

import hangman.ui.curses
import urwid
import urwid.raw_display
import os


def simple_text(text):
    """ Builds a urwid text widget

    Args:
        text (str): The value for the urwid.Text widget

    Returns:
        urwid.Text: A text the value of `text` parameter.

    """
    return urwid.Text(u"{0}".format(text))


def create_edit(label, text, fn):
    w = urwid.Edit(label, text, multiline=True)
    urwid.connect_signal(w, 'change', fn)
    fn(w, text)
    w = urwid.AttrWrap(w, 'edit')
    return w


class ListChars(urwid.ListBox):

    def __init__(self):
        body = urwid.SimpleListWalker([simple_text(40*'-')])
        super(hangman.ui.curses.ListChars, self).__init__(body)

    def add_char(self, text):
        position = self.focus_position
        self.body.insert(position + 1, simple_text(text))


class HangmanUrwid:

    def __init__(self, hangman_ascii='resources/hangman_ascii_default.txt'):
        self.palette = [
            ('body', 'black', 'light gray', 'standout'),
            ('header', 'white', 'dark red', 'bold'),
            ('button normal', 'light gray', 'dark blue', 'standout'),
            ('button select', 'white', 'dark green'),
            ('button disabled', 'dark gray', 'dark blue'),
            ('edit', 'light gray', 'dark blue'),
            ('bigtext', 'white', 'black'),
            ('chars', 'light gray', 'black'),
            ('exit', 'white', 'dark cyan'), ]
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        self.ascii_segments = self.hangman_ascii_segments(
            os.path.join(__location__, hangman_ascii)
        )
        self.btw = urwid.Text("")
        self.hangman_engine = HangmanEngine('Silenus')
        self.letter_edit = urwid.Edit('Guess: ', '')
        self.sentence_found = urwid.Text(self.hangman_engine.get_text_found())
        urwid.connect_signal(self.letter_edit, 'change',
                             self.on_edit_text_change)
        self.tfw = urwid.Text('Failed chars:')
        self.bt_view = urwid.Pile([self.btw, urwid.Divider('-'),
                                   self.letter_edit, urwid.Divider('-'),
                                   self.sentence_found],
                                  focus_item=2)
        self.tstatus_w = urwid.Text(self.hangman_engine.get_status_text())
        self.tstatus_w.set_align_mode('right')
        self.current_segment = 0

    def on_edit_text_change(self, widget, text):
        if len(text):
            char = text[len(text)-1]
            if self.still_alive():
                if self.found(char):
                    self.sentence_found.set_text(
                        self.hangman_engine.get_text_found())
                else:
                    self.tfw.set_text("{0} {1} ".format(
                        self.tfw.text, char
                    ))
                    if self.still_alive():
                        self.draw_hangman_ascii_segment()
                    else:
                        self.draw_hangman_ascii_segment(last=True)

                self.tstatus_w.set_text(self.hangman_engine.get_status_text())

    def draw_hangman_ascii_segment(self, last=False):
        x = len(self.ascii_segments)
        y = self.hangman_engine.max_attempts
        z = len(self.hangman_engine.guess_misses)
        r = x/y if y > x else y/x
        g = (z-r)
        result = False
        if g > 1:
            if last:
                self.btw.set_text(self.ascii_segments[x-1])
            else:
                self.btw.set_text(self.ascii_segments[self.current_segment])
                self.current_segment += 1
                result = True

        return result

    def still_alive(self):
        result = (len(self.hangman_engine.guess_misses) <
                  self.hangman_engine.max_attempts)
        return result

    def found(self, char):
        result = self.hangman_engine.count(char)
        if not self.hangman_engine.already_tried(char):
            occurrences = self.hangman_engine.occurrences(char)
            if occurrences:
                for char_i in occurrences:
                    pass

        return result

    def hangman_ascii_segments(self, hangman_ascii_location):
        file_segments = open(hangman_ascii_location, 'r').read().split(',')
        return file_segments

    def setup_view(self):
        self.body_view = urwid.Columns([('weight', 3, self.bt_view),
                                        ('weight', 1, self.tfw)],
                                       dividechars=4)
        self.body_view = urwid.Filler(self.body_view, valign='middle')
        self.ttitle_w = urwid.Text(self.hangman_engine.__repr__())
        self.head_view = urwid.Columns([('weight', 2, self.ttitle_w),
                                        ('weight', 2, self.tstatus_w)])

        self.main_view = urwid.Frame(body=self.body_view, header=self.head_view)
        bg = urwid.AttrWrap(urwid.SolidFill(u"\u259E"), 'main shadow')
        self.main_view = urwid.Padding(self.main_view, left=4, right=4,
                                       align='center')
        return urwid.Overlay(self.main_view, bg,
                             ('fixed left', 2), ('fixed right', 3),
                             ('fixed top', 1), ('fixed bottom', 2))

    def run(self):
        self.view = self.setup_view()
        self.loop = urwid.MainLoop(self.view, self.palette)
        self.loop.run()
