"""Small AppKit builders shared by the Settings and Welcome windows.

Hand-rolled rather than pulled from a UI framework: the whole point of this project is
that a reader can follow every line, and a layout DSL would be one more thing to trust.

House rules encoded here, so both windows stay consistent:

* Colour carries meaning or it is not used. Ordinary state is grey; red appears only
  where something is actually blocking the user and there is a button next to it to
  fix that. Nothing is green — "it works" is the boring case and should look boring.
* Explanatory text is secondary grey and small; it never competes with the control it
  explains.
* Links look like links (blue, no bezel), not like push buttons.
"""
import AppKit
from Foundation import NSMakeRect

LABEL = AppKit.NSColor.labelColor()
SECONDARY = AppKit.NSColor.secondaryLabelColor()
ALERT = AppKit.NSColor.systemRedColor()
LINK = AppKit.NSColor.linkColor()

POPOVER_PAD = 14   # inside a popover, which is tighter than a window


def label(text, x, y, w, bold=False, color=None, size=13):
    f = AppKit.NSTextField.alloc().initWithFrame_(NSMakeRect(x, y, w, 18))
    f.setStringValue_(text)
    # Single line, said out loud. An NSTextField wraps by default, and 18 points of
    # height fits exactly one line — so a label long enough to wrap loses its second
    # half with no sign that anything is missing. Truncation at least shows an ellipsis,
    # and it is what test_i18n.py measures a translation against.
    f.setUsesSingleLineMode_(True)
    f.setLineBreakMode_(AppKit.NSLineBreakByTruncatingTail)
    f.setBezeled_(False)
    f.setDrawsBackground_(False)
    f.setEditable_(False)
    f.setSelectable_(False)
    f.setFont_(AppKit.NSFont.boldSystemFontOfSize_(size) if bold
               else AppKit.NSFont.systemFontOfSize_(size))
    f.setTextColor_(color or LABEL)
    return f


def required_label(text, x, y, w, size=13):
    """A field label carrying the red asterisk that means "this one is not optional".

    One attributed string rather than a label plus a second label: two views drift
    apart by however wrong the first one's width guess was, and this one has to sit
    tight against the text to read as a marker instead of as debris.
    """
    f = label(text, x, y, w, size=size)
    marker = {AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(size),
              AppKit.NSForegroundColorAttributeName: ALERT}
    plain = {AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(size),
             AppKit.NSForegroundColorAttributeName: LABEL}
    text_attr = AppKit.NSMutableAttributedString.alloc().initWithString_attributes_(
        text, plain)
    text_attr.appendAttributedString_(
        AppKit.NSAttributedString.alloc().initWithString_attributes_(" *", marker))
    f.setAttributedStringValue_(text_attr)
    return f


def note(text, x, y, w, h, size=11):
    """Secondary explanatory text. Wraps; never the loudest thing on screen."""
    f = AppKit.NSTextField.alloc().initWithFrame_(NSMakeRect(x, y, w, h))
    f.setStringValue_(text)
    f.setBezeled_(False)
    f.setDrawsBackground_(False)
    f.setEditable_(False)
    f.setSelectable_(True)
    f.setFont_(AppKit.NSFont.systemFontOfSize_(size))
    f.setTextColor_(SECONDARY)
    f.cell().setWraps_(True)
    return f


def field(x, y, w, secure=False, placeholder="", target=None, action=None):
    """Text field. Wiring target/action makes Return commit, which people expect."""
    cls = AppKit.NSSecureTextField if secure else AppKit.NSTextField
    f = cls.alloc().initWithFrame_(NSMakeRect(x, y, w, 22))
    f.setFont_(AppKit.NSFont.systemFontOfSize_(12))
    if placeholder:
        f.setPlaceholderString_(placeholder)
    if action is not None:
        f.setTarget_(target)
        f.setAction_(action)
    return f


def button(title, x, y, w, target, action, default=False, small=True):
    b = AppKit.NSButton.alloc().initWithFrame_(NSMakeRect(x, y, w, 24 if small else 32))
    b.setTitle_(title)
    b.setBezelStyle_(AppKit.NSBezelStyleRounded)
    if small:
        b.setControlSize_(AppKit.NSControlSizeSmall)
        b.setFont_(AppKit.NSFont.systemFontOfSize_(11))
    if default:
        b.setKeyEquivalent_("\r")   # Return activates it, and macOS tints it
    b.setTarget_(target)
    b.setAction_(action)
    return b


def link(title, x, y, w, target, action):
    """A borderless blue link. A bordered push button for a URL reads as an action
    the app performs, which is not what opening a web page is."""
    b = AppKit.NSButton.alloc().initWithFrame_(NSMakeRect(x, y, w, 16))
    b.setBordered_(False)
    b.setButtonType_(AppKit.NSButtonTypeMomentaryChange)
    b.setFont_(AppKit.NSFont.systemFontOfSize_(11))
    b.setAlignment_(AppKit.NSTextAlignmentLeft)
    attrs = {
        AppKit.NSForegroundColorAttributeName: LINK,
        AppKit.NSFontAttributeName: AppKit.NSFont.systemFontOfSize_(11),
    }
    b.setAttributedTitle_(
        AppKit.NSAttributedString.alloc().initWithString_attributes_(title, attrs))
    b.setTarget_(target)
    b.setAction_(action)
    return b


def linked_note(before, link_text, url, after, x, y, w, size=11):
    """One line of secondary text with one clickable link inside it.

    Composing this out of a label plus a button never lines up: the button carries its
    own internal padding and its own baseline, so the two halves drift apart by a few
    points and by however wrong the label's width guess was. A single text field with
    an attributed string has one baseline and one text run, and the link lands exactly
    where the sentence puts it.
    """
    font = AppKit.NSFont.systemFontOfSize_(size)
    text = AppKit.NSMutableAttributedString.alloc().init()

    def run(s, attrs):
        text.appendAttributedString_(
            AppKit.NSAttributedString.alloc().initWithString_attributes_(s, attrs))

    plain = {AppKit.NSFontAttributeName: font,
             AppKit.NSForegroundColorAttributeName: SECONDARY}
    linked = {AppKit.NSFontAttributeName: font,
              AppKit.NSForegroundColorAttributeName: LINK,
              AppKit.NSLinkAttributeName: url}

    if before:
        run(before, plain)
    run(link_text, linked)
    if after:
        run(after, plain)

    f = AppKit.NSTextField.alloc().initWithFrame_(NSMakeRect(x, y, w, 16))
    f.setBezeled_(False)
    f.setDrawsBackground_(False)
    f.setEditable_(False)
    # Both are required for a link inside a text field to be clickable and to show
    # the pointing-hand cursor.
    f.setSelectable_(True)
    f.setAllowsEditingTextAttributes_(True)
    f.setAttributedStringValue_(text)
    return f


def checkbox(title, x, y, w, target, action):
    b = AppKit.NSButton.alloc().initWithFrame_(NSMakeRect(x, y, w, 20))
    b.setButtonType_(AppKit.NSButtonTypeSwitch)
    b.setTitle_(title)
    b.setFont_(AppKit.NSFont.systemFontOfSize_(12))
    b.setTarget_(target)
    b.setAction_(action)
    return b


def help_button(x, y, target, action, tag=0):
    """The round ? macOS puts next to a field it expects to have to explain.

    Deliberately the system bezel rather than a drawn glyph: people already know what
    the circle does, and it is the one control that can carry an explanation without
    spending a line of the window on it.
    """
    b = AppKit.NSButton.alloc().initWithFrame_(NSMakeRect(x, y, 21, 21))
    b.setBezelStyle_(AppKit.NSBezelStyleHelpButton)
    b.setTitle_("")
    b.setTag_(tag)
    b.setTarget_(target)
    b.setAction_(action)
    return b


def _text_height(text, width, size):
    font = AppKit.NSFont.systemFontOfSize_(size)
    rect = AppKit.NSString.stringWithString_(text).boundingRectWithSize_options_attributes_(
        (width, 10000.0), AppKit.NSStringDrawingUsesLineFragmentOrigin,
        {AppKit.NSFontAttributeName: font})
    return rect.size.height


def show_help(button, title, body, link_text="", url="", width=320):
    """Pop an explanation out of a help button. Returns the popover, which the caller
    must keep a reference to — AppKit does not retain it and it vanishes mid-animation.

    Transient behaviour: it closes on the next click anywhere, so there is no dialog to
    dismiss and nothing to get stuck behind the window.
    """
    inner = width - POPOVER_PAD * 2
    body_h = _text_height(body, inner, 11) + 4
    link_h = 18 if link_text else 0
    height = POPOVER_PAD * 2 + link_h + body_h + 22

    view = AppKit.NSView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    y = height - POPOVER_PAD - 16
    view.addSubview_(label(title, POPOVER_PAD, y, inner, bold=True, size=12))
    y -= body_h + 4
    view.addSubview_(note(body, POPOVER_PAD, y, inner, body_h))
    if link_text:
        y -= link_h
        view.addSubview_(linked_note("", link_text, url, "", POPOVER_PAD, y, inner))

    controller = AppKit.NSViewController.alloc().init()
    controller.setView_(view)
    popover = AppKit.NSPopover.alloc().init()
    popover.setContentViewController_(controller)
    popover.setContentSize_((width, height))
    popover.setBehavior_(AppKit.NSPopoverBehaviorTransient)
    popover.showRelativeToRect_ofView_preferredEdge_(
        button.bounds(), button, AppKit.NSRectEdgeMaxY)
    return popover


def popup(entries, x, y, w, target, action):
    """Pop-up menu. A None entry in `entries` becomes a separator."""
    p = AppKit.NSPopUpButton.alloc().initWithFrame_pullsDown_(
        NSMakeRect(x, y, w, 24), False)
    for entry in entries:
        if entry is None:
            p.menu().addItem_(AppKit.NSMenuItem.separatorItem())
        else:
            p.addItemWithTitle_(entry)
    p.setTarget_(target)
    p.setAction_(action)
    p.setFont_(AppKit.NSFont.systemFontOfSize_(12))
    return p


def separator(x, y, w):
    box = AppKit.NSBox.alloc().initWithFrame_(NSMakeRect(x, y, w, 1))
    box.setBoxType_(AppKit.NSBoxSeparator)
    return box


def spinner(x, y):
    s = AppKit.NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(x, y, 16, 16))
    s.setStyle_(AppKit.NSProgressIndicatorStyleSpinning)
    s.setControlSize_(AppKit.NSControlSizeSmall)
    s.setDisplayedWhenStopped_(False)
    return s


def progress_bar(x, y, w):
    p = AppKit.NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(x, y, w, 8))
    p.setStyle_(AppKit.NSProgressIndicatorStyleBar)
    p.setIndeterminate_(False)
    p.setMinValue_(0.0)
    return p


def titled_entries(choices):
    """Split a config list of (title, value) plus None separators into the two lists
    the pop-up helpers want: display entries, and the value behind each real row."""
    entries = [c[0] if c else None for c in choices]
    values = [c[1] for c in choices if c]
    return entries, values


def select_value(popup_button, choices, value):
    """Select the row backing `value`, accounting for separator rows. Does not fire
    the action — AppKit only sends that on a user click."""
    index = 0
    for entry in choices:
        if entry is None:
            index += 1
            continue
        if entry[1] == value:
            popup_button.selectItemAtIndex_(index)
            return True
        index += 1
    return False


def selected_value(popup_button, choices):
    """Inverse of select_value: the value behind the currently selected row."""
    index = popup_button.indexOfSelectedItem()
    if 0 <= index < len(choices) and choices[index] is not None:
        return choices[index][1]
    return None
