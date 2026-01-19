#!/usr/bin/env python

import sys

from PySide6.QtWidgets import QMessageBox, QApplication


def catch_error(f):
    import functools
    @functools.wraps(f)
    def catch_unhandled_exceptions(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            sys.stderr.flush()
            dialog = QMessageBox()
            dialog.setWindowTitle('MiasMod')
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText(
                QApplication.translate('Errors', 'Unhandled Exception', None))
            dialog.setInformativeText('%s: %s' % (e.__class__.__name__, str(e)))
            dialog.setDetailedText(traceback.format_exc())
            dialog.exec_()
            return

    return catch_unhandled_exceptions


def cmp(a, b):
    return (a > b) - (a < b)

# vi:noexpandtab:sw=8:ts=8
