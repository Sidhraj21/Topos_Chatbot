import sys

if sys.version_info[0] < 3:
    # for Python2
    import Tkinter as tk
    import tkMessageBox as messagebox
    from Tkinter import *
else:
    # for Python3
    import tkinter as tk
    from tkinter import *

import query
from query import Query
import edison
from edison import *


class Chatbot:
    def __init__(self, window_title):
        logging_file = None
        self._is_empty = True

        # create chat log
        self._logging_file = logging_file

        if logging_file is None:
            self._log = None
        else:
            try:
                self._log = open(logging_file, "r")
            except:
                self._log = None

                # create window
        self.window = tk.Tk()
        self.window.title(window_title)
        # self.window.geometry("870x400")

        # create chatbox frame
        self.interior = tk.Frame(self.window, class_="Chatbox")
        self.interior.pack(expand=True, fill=tk.BOTH)

        # create msg frame
        self.msg_frame = tk.Frame(self.interior, padx=10, bg="#FFF6E5", class_="Top")
        self.msg_frame.pack(expand=True, fill=tk.BOTH)

        self._textarea = tk.Text(self.msg_frame, state=tk.DISABLED)

        # create scroll bar for the msg_frame
        self.scroll_bar = tk.Scrollbar(
            self.msg_frame, takefocus=0, command=self._textarea.yview
        )
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self._textarea.pack(side=tk.RIGHT, expand=YES, fill=tk.BOTH)
        self._textarea["yscrollcommand"] = self.scroll_bar.set

        # Create Chatbox Entry Frame
        self.entry_frame = Frame(self.window, class_="Chatbox_Entry")
        self.entry_frame.pack(fill=tk.X, anchor=tk.N)

        # create dropdown list for query option
        self.query_option = tk.StringVar(self.entry_frame)
        self.query_option.set("KB")
        w = OptionMenu(self.entry_frame, self.query_option, "KB", "Feeds")
        w.pack()

        # create msg_txtbox for users to input their queries
        self.user_msg = tk.StringVar()
        self.msg_txtbox = tk.Entry(
            self.entry_frame,
            textvariable=self.user_msg,
            width=100,
            font=("Helvetica", 16),
        )
        self.msg_txtbox.bind("<Return>", self.send)  # shortcut
        self.msg_txtbox.pack(side=tk.LEFT, anchor=tk.SE, fill=tk.X)

        self.window.mainloop()

    def send(self, event=None):
        # Get the msg input from the user and return the answer depends on the query option
        relative_position_of_scrollbar = self.scroll_bar.get()[1]
        msg = self.user_msg.get()

        # display the user msg
        self.display_user_text(msg)

        # get query option from user
        # -KB: query from the KB
        # -Feeds: feed text to Edison and get return
        if self.query_option.get() == "KB":
            query = Query()
            j = query.match_question(msg)
            print("matched q: %s real q: %s" % (query.get_question(j), msg))
            ans = query.get_query(j)
        else:
            ans = edison.get_response_kibana(msg)

            # display the bot msg
        self.display_bot_text(ans)
        self.msg_txtbox.delete("0", tk.END)

        # move the scroll bar to bottom
        if relative_position_of_scrollbar == 1:
            self._textarea.yview_moveto(1)

    def _filter_text(self, text):
        return "".join(ch for ch in text if ch <= u"\uFFFF")

        # Display the bot msg

    def display_bot_text(self, text):
        self._textarea.config(state=NORMAL)

        if self._is_empty:
            self._is_empty = False
        else:
            self._textarea.insert(END, "\n")
            if self._log is not None:
                self._log.write("\n")

        text = self._filter_text("Bot: " + text)
        self._textarea.tag_config("botcolor", foreground="red")
        self._textarea.insert(END, text, "botcolor")
        self._textarea.config(state=DISABLED)

        # Display the user msg

    def display_user_text(self, text):

        self._textarea.config(state=NORMAL)

        if self._is_empty:
            self._is_empty = False
        else:
            self._textarea.insert(END, "\n")
            if self._log is not None:
                self._log.write("\n")

        text = self._filter_text("User: " + text)
        self._textarea.tag_config("usercolor", foreground="blue")
        self._textarea.insert(END, text, "usercolor")
        self._textarea.config(state=DISABLED)


if __name__ == "__main__":
    Chatbot("Lord of the Ring Bot")
