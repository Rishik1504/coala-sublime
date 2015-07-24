import sublime_plugin
from .Utils import log, COALA_KEY


class CoalaBackground(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        """
        Show errors in the status line when the carret/selection moves.
        This assumes that the output from coala are saved in COALA_OUTPUT.
        """
        output = view.settings().get(COALA_KEY + ".output", {})
        last_line = view.settings().get(COALA_KEY + ".last_line", -1)
        if output:
            # Get the currently selected line
            new_selected_line = view.rowcol(view.sel()[0].end())[0]

            if new_selected_line != last_line:  # If line has changed
                view.settings().set(COALA_KEY + ".last_line", new_selected_line)

                # Search through results, and show message (if it exists)
                found_result_flag = False
                for section_name, section_results in output["results"].items():
                    for result in section_results:
                        if new_selected_line == result["line_nr"] - 1:
                            msg = result["origin"] + ": " + result["message"]
                            view.set_status(COALA_KEY, msg)
                            found_result_flag = True

                if view.get_status(COALA_KEY) and not found_result_flag:
                    view.erase_status(COALA_KEY)
