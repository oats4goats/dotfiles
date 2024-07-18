# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile
from libqtile import widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import extension
from libqtile.widget import backlight

# from qtile_extras import widget
# from qtile_extras.widget.decorations import BorderDecoration

import colors

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # 
    # by Mitya
    # Special symbols:
    # https://github.com/qtile/qtile/blob/master/libqtile/backend/x11/xkeysyms.py 

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Run Rofi launcher"),
    # Key([mod], "e", lazy.spawn("my_menu.sh"), desc="Run Rofi launcher with my menu"),

    # by Mitya
    Key([alt], "Shift_L", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),

    Key([], 'XF86AudioMute', lazy.widget["pulsevolume"].mute()),
    Key([], 'XF86AudioRaiseVolume', lazy.widget["pulsevolume"].increase_vol()),
    Key([], 'XF86AudioLowerVolume', lazy.widget["pulsevolume"].decrease_vol()),

    # Key([], 'XF86MonBrightnessUp',  lazy.widget["backlight"].change_backlight(backlight.ChangeDirection.UP)),
    # Key([], 'XF86MonBrightnessDown', lazy.widget["backlight"].change_backlight(backlight.ChangeDirection.DOWN)),

    Key([], 'XF86MonBrightnessUp',  lazy.spawn('brillo -q -u 1000000 -A 10'), desc="Increase brightness with exp scale"),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brillo -q -u 1000000 -U 10'), desc="Decrease brightness with exp scale"),

    Key([], 'Print', lazy.spawn('maim -s | xclip -selection clipboard -t image/png', shell=True), desc="Send the screenshot to clipboard"),
    Key([alt, "control"], 'Delete', lazy.spawn('show ~/fav_menus/power_menu | run', shell=True), desc="Power menu"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# colors = colors.SolarizedDark

colors = [
    "#002b36",
    "#073642",
    "#586e75",
    "#657b83",
    "#839496",
    "#93a1a1",
    "#eee8d5",
    "#fdf6e3",
    "#b58900",
    "#cb4b16",
    "#dc322f",
    "#d33682",
    "#6c71c4",
    "#268bd2",
    "#2aa198",
    "#859900"
]

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[12],
                "border_normal": colors[1],
                "single_border_width": 0,
                }

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="CaskaydiaMono Nerd Font",
    fontsize=19,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.Prompt(foreground = colors[6]),
                widget.GroupBox(active = colors[6], inactive = colors[4], highlight_method = "", this_current_screen_border = colors[13]),
                widget.CurrentLayoutIcon(foreground = colors[4]),
                # widget.CurrentLayout(foreground = colors[4]),
                # widget.Sep(padding = 10, linewidth = 2),
                widget.WindowName(background = colors[8], foreground = colors[7]),
                # widget.Sep(padding = 10, linewidth = 2),
                widget.Backlight(foreground = colors[4], backlight_name = "intel_backlight", format = "eDP: {percent:2.0%}"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.Battery(low_background = colors[10], low_foreground = colors[6], empty_char = "X", full_char = "=", charge_char = "󱐋", discharge_char = "", not_charging_char = "!", battery = 0, foreground = colors[4], format = "{char}{percent:2.1%}", fmt = "BAT0: {}"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.CPU(foreground = colors[4], format = "CPU: {load_percent}%"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.Memory(foreground = colors[4], measure_mem='G', format = "{MemFree:.1f}{mm}", fmt = "RAM: {}"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.DF(foreground = colors[4], partiotion = "/", visible_on_warn = False, format = "{uf}{m}", fmt = "SSD: {}"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.KeyboardLayout(foreground = colors[6], configured_keyboards = ['us', 'ru']),
                widget.Sep(padding = 10, linewidth = 2),
                widget.PulseVolume(
                    foreground = colors[4], 
                    fmt = "Vol: {}",
                    mute_command = "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle",
                    volume_down_command = "wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%-",
                    volume_up_command = "wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%+"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.Wlan(foreground = colors[4], format = "WiFi: {percent:2.0%}"),
                widget.Sep(padding = 10, linewidth = 2),
                # widget.Wallpaper(foreground = colors[4], directory = "/usr/share/backgrounds/", random_selection = True, label = "WLPR"),
                # widget.Chord(
                #    chords_colors={
                #        "launch": ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                # widget.Sep(padding = 10, linewidth = 2),
                widget.Clock(foreground = colors[6], format="%b %d (%a) %H:%M"),
                widget.Sep(padding = 10, linewidth = 2),
                widget.Systray(),
                widget.Spacer(length = 10),
                # widget.QuickExit(),
            ],
            30,
            background = colors[0],
            opacity = 0.9,
            # margin = [0, 0, 0, 0],
            # border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
