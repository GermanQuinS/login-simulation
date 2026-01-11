#!/usr/bin/env python3
"""
macOS Premium Login Screen
Usuario: GermanQS
Contraseña: Germancito10
"""

import tkinter as tk
import math
from datetime import datetime, timedelta
import sys
import random

USUARIO_VALIDO = "GermanQS"
PASS_VALIDA = "Germancito10"
MAX_INTENTOS = 5

# === ESTILO macOS ===
BG_TOP = '#0B0F14'
BG_BOTTOM = '#1A1F26'
TEXT_MAIN = '#FFFFFF'
TEXT_SUB = '#A1A1A6'
ORANGE = '#FF9F0A'
ORANGE_DARK = '#CC7A00'
GREEN = '#32D74B'
RED = '#FF453A'
FIELD_BG = '#1C1C1E'
FIELD_BORDER = '#3A3A3C'
FONT = 'SF Pro Display'

class MacOSLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.attributes('-fullscreen', True)

        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind('<Escape>', lambda e: "break")
        self.root.bind('<F11>', lambda e: "break")
        self.root.bind('<Control-c>', lambda e: "break")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.intentos = 0
        self.bloqueado = False
        self.tiempo_desbloqueo = None
        self.password_focused = False

        self.setup_ui()

    # ================= UI =================

    def setup_ui(self):
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=BG_TOP,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)

        self.crear_fondo()
        self.crear_reloj()
        self.crear_login_box()
        self.crear_footer()

        self.actualizar_reloj()
        self.animar_estrellas()
        self.animar_avatar_border()
        self.password_entry.focus_set()

    def crear_fondo(self):
        for y in range(self.height):
            ratio = y / self.height
            r = int(11 + (26 - 11) * ratio)
            g = int(15 + (31 - 15) * ratio)
            b = int(20 + (38 - 20) * ratio)
            self.canvas.create_line(0, y, self.width, y,
                                    fill=f'#{r:02x}{g:02x}{b:02x}')

        self.estrellas = []
        random.seed(42)
        for _ in range(20):
            x = random.randint(80, self.width - 80)
            y = random.randint(80, self.height - 80)
            s = random.choice([1, 1.5])
            e = self.canvas.create_oval(x, y, x + s, y + s,
                                        fill='#FFFFFF', outline='')
            self.estrellas.append((e, random.random()))

    def crear_reloj(self):
        cx = self.width // 2
        self.clock_text = self.canvas.create_text(
            cx, 110,
            font=(FONT, 92, 'bold'),
            fill=TEXT_MAIN
        )
        self.date_text = self.canvas.create_text(
            cx, 175,
            font=(FONT, 24),
            fill=TEXT_SUB
        )

    def crear_login_box(self):
        cx = self.width // 2
        cy = self.height // 2 + 60
        avatar_y = cy - 165

        for i in range(55):
            r = 78 - i * 1.4
            shade = int(40 + i * 3)
            self.canvas.create_oval(
                cx - r, avatar_y - r,
                cx + r, avatar_y + r,
                fill=f'#{shade:02x}{shade:02x}{shade:02x}',
                outline=''
            )

        self.avatar_border = self.canvas.create_oval(
            cx - 78, avatar_y - 78,
            cx + 78, avatar_y + 78,
            outline=ORANGE,
            width=3
        )

        self.canvas.create_text(
            cx, avatar_y + 2,
            text='G',
            font=(FONT, 68, 'bold'),
            fill=TEXT_MAIN
        )

        self.canvas.create_text(
            cx, avatar_y + 115,
            text=USUARIO_VALIDO,
            font=(FONT, 28, 'bold'),
            fill=TEXT_MAIN
        )

        # === PASSWORD ===
        password_y = avatar_y + 185
        w, h = 380, 56

        self.password_bg = self.canvas.create_rectangle(
            cx - w//2, password_y - h//2,
            cx + w//2, password_y + h//2,
            fill=FIELD_BG,
            outline=FIELD_BORDER,
            width=2
        )

        self.password_focus = self.canvas.create_rectangle(
            cx - w//2 - 3, password_y - h//2 - 3,
            cx + w//2 + 3, password_y + h//2 + 3,
            outline=ORANGE,
            width=3,
            state='hidden'
        )

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.canvas,
            textvariable=self.password_var,
            font=(FONT, 22),
            bg=FIELD_BG,
            fg=TEXT_MAIN,
            insertbackground=ORANGE,
            show='●',
            bd=0,
            justify='center'
        )

        self.password_window = self.canvas.create_window(
            cx, password_y,
            window=self.password_entry,
            width=360,
            height=46
        )

        self.password_entry.bind('<FocusIn>', self.on_focus)
        self.password_entry.bind('<FocusOut>', self.on_blur)
        self.password_entry.bind('<Return>', lambda e: self.verificar_login())

        # === BOTÓN ===
        btn_y = password_y + 85
        for i in range(22):
            r = 36 - i * 1.4
            self.canvas.create_oval(
                cx - r, btn_y - r,
                cx + r, btn_y + r,
                fill=f'#{255 - i*6:02x}{159 - i*4:02x}0A',
                outline=''
            )

        self.btn_border = self.canvas.create_oval(
            cx - 36, btn_y - 36,
            cx + 36, btn_y + 36,
            outline=ORANGE_DARK,
            width=3
        )

        self.btn_arrow = self.canvas.create_text(
            cx, btn_y,
            text='→',
            font=(FONT, 40, 'bold'),
            fill=TEXT_MAIN
        )

        for i in [self.btn_border, self.btn_arrow]:
            self.canvas.tag_bind(i, '<Button-1>', lambda e: self.verificar_login())
            self.canvas.tag_bind(i, '<Enter>', self.on_btn_hover)
            self.canvas.tag_bind(i, '<Leave>', self.on_btn_leave)

        # === MENSAJES ===
        msg_y = btn_y + 75
        self.error_text = self.canvas.create_text(
            cx, msg_y, fill=RED, font=(FONT, 17)
        )
        self.intentos_text = self.canvas.create_text(
            cx, msg_y + 28, fill=TEXT_SUB, font=(FONT, 15)
        )
        self.timer_text = self.canvas.create_text(
            cx, msg_y + 90, fill=ORANGE,
            font=(FONT, 54, 'bold'), state='hidden'
        )
        self.success_text = self.canvas.create_text(
            cx, msg_y, fill=GREEN,
            font=(FONT, 19), state='hidden'
        )

    def crear_footer(self):
        self.canvas.create_text(
            self.width // 2, self.height - 32,
            text='Presiona Alt+F4 para salir',
            font=(FONT, 13),
            fill='#6E6E73'
        )

    # ================= ANIMACIONES =================

    def animar_estrellas(self, step=0):
        for s, o in self.estrellas:
            a = 0.5 + 0.5 * abs(math.sin((step + o * 80) * 0.02))
            v = int(255 * a)
            self.canvas.itemconfig(s, fill=f'#{v:02x}{v:02x}{v:02x}')
        self.root.after(60, lambda: self.animar_estrellas(step + 1))

    def animar_avatar_border(self, step=0):
        b = int(180 + 60 * abs(math.sin(step * 0.025)))
        g = int(159 * b / 255)
        self.canvas.itemconfig(
            self.avatar_border,
            outline=f'#{b:02x}{g:02x}0A'
        )
        self.root.after(50, lambda: self.animar_avatar_border(step + 1))

    def on_focus(self, e):
        self.password_focused = True
        self.canvas.itemconfig(self.password_focus, state='normal')
        self.animar_focus()

    def on_blur(self, e):
        self.password_focused = False
        self.canvas.itemconfig(self.password_focus, state='hidden')

    def animar_focus(self, step=0):
        if not self.password_focused:
            return
        b = int(200 + 40 * abs(math.sin(step * 0.08)))
        g = int(159 * b / 255)
        self.canvas.itemconfig(
            self.password_focus,
            outline=f'#{b:02x}{g:02x}0A'
        )
        self.root.after(40, lambda: self.animar_focus(step + 1))

    def on_btn_hover(self, e):
        self.canvas.itemconfig(self.btn_border, width=4, outline=ORANGE)
        self.root.config(cursor='hand2')

    def on_btn_leave(self, e):
        self.canvas.itemconfig(self.btn_border, width=3, outline=ORANGE_DARK)
        self.root.config(cursor='')

    # ================= LÓGICA (ORIGINAL) =================

    def actualizar_reloj(self):
        now = datetime.now()
        self.canvas.itemconfig(self.clock_text, text=now.strftime('%H:%M'))

        dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        meses = ['enero','febrero','marzo','abril','mayo','junio',
                 'julio','agosto','septiembre','octubre','noviembre','diciembre']
        self.canvas.itemconfig(
            self.date_text,
            text=f"{dias[now.weekday()]}, {now.day} de {meses[now.month-1]}"
        )
        self.root.after(1000, self.actualizar_reloj)

    def verificar_login(self):
        if self.bloqueado:
            self.shake()
            return

        if self.password_var.get() == PASS_VALIDA:
            self.login_exitoso()
        else:
            self.login_fallido()

    def login_exitoso(self):
        self.canvas.itemconfig(self.error_text, text='')
        self.canvas.itemconfig(self.intentos_text, text='')
        self.canvas.itemconfig(self.success_text,
                               text='✓ Acceso concedido',
                               state='normal')
        self.password_entry.config(state='disabled')
        self.root.after(1200, lambda: self.root.destroy() or sys.exit(0))

    def login_fallido(self):
        self.intentos += 1
        restantes = MAX_INTENTOS - self.intentos
        self.password_var.set('')
        self.shake()
        self.canvas.itemconfig(self.error_text, text='Contraseña incorrecta')

        if restantes > 0:
            self.canvas.itemconfig(
                self.intentos_text,
                text=f'Intentos restantes: {restantes}'
            )
        else:
            self.iniciar_bloqueo()

    def iniciar_bloqueo(self):
        self.bloqueado = True
        self.tiempo_desbloqueo = datetime.now() + timedelta(minutes=5)
        self.password_entry.config(state='disabled')
        self.canvas.itemconfig(self.timer_text, state='normal')
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if not self.bloqueado:
            return

        diff = self.tiempo_desbloqueo - datetime.now()
        if diff.total_seconds() <= 0:
            self.desbloquear()
            return

        m = int(diff.total_seconds() // 60)
        s = int(diff.total_seconds() % 60)
        self.canvas.itemconfig(self.timer_text, text=f'{m:02d}:{s:02d}')
        self.root.after(100, self.actualizar_temporizador)

    def desbloquear(self):
        self.bloqueado = False
        self.intentos = 0
        self.canvas.itemconfig(self.timer_text, state='hidden')
        self.canvas.itemconfig(self.error_text, text='')
        self.canvas.itemconfig(self.intentos_text, text='')
        self.password_entry.config(state='normal')
        self.password_entry.focus_set()

    def shake(self, c=0):
        if c >= 10:
            return
        offset = int(16 * math.sin(c * math.pi / 5))
        if c == 0:
            self.bg_pos = self.canvas.coords(self.password_bg)
            self.focus_pos = self.canvas.coords(self.password_focus)
            self.win_x = self.canvas.coords(self.password_window)[0]

        self.canvas.coords(self.password_bg,
                           self.bg_pos[0] + offset, self.bg_pos[1],
                           self.bg_pos[2] + offset, self.bg_pos[3])
        self.canvas.coords(self.password_focus,
                           self.focus_pos[0] + offset, self.focus_pos[1],
                           self.focus_pos[2] + offset, self.focus_pos[3])
        self.canvas.coords(self.password_window,
                           self.win_x + offset,
                           self.canvas.coords(self.password_window)[1])
        self.root.after(30, lambda: self.shake(c + 1))


def main():
    root = tk.Tk()
    MacOSLogin(root)
    root.mainloop()

if __name__ == "__main__":
    main()
