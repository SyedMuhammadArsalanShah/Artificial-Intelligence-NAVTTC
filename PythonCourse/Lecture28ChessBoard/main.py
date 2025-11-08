import tkinter as tk
import chess
import random
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# ===================== TRAIN MODEL =====================
def generate_data(samples=300):
    X, y = [], []
    for _ in range(samples):
        b = chess.Board()
        for _ in range(random.randint(1, 10)):
            if b.is_game_over():
                break
            move = random.choice(list(b.legal_moves))
            b.push(move)
        white = len([p for p in b.piece_map().values() if p.color])
        black = len([p for p in b.piece_map().values() if not p.color])
        mobility = len(list(b.legal_moves))
        score = (white - black) * 0.8 + 0.2 * (mobility / 10)
        X.append([white, black, mobility])
        y.append(score)
    return np.array(X), np.array(y)

try:
    model = joblib.load("chess_ai_model.pkl")
except:
    X, y = generate_data()
    model = LinearRegression().fit(X, y)
    joblib.dump(model, "chess_ai_model.pkl")

# ===================== SETUP =====================
root = tk.Tk()
root.title("♛ Smart ML Chess – Syed M Arsalan Shah")
root.geometry("1100x760")
root.minsize(850, 640)
root.config(bg="#0f1112")

board = chess.Board()
buttons, selected = {}, None
flipped = False
player_score, ai_score = 0, 0

piece_icons = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
}

# ===================== EVALUATION =====================
def evaluate_board(b):
    white = len([p for p in b.piece_map().values() if p.color])
    black = len([p for p in b.piece_map().values() if not p.color])
    mobility = len(list(b.legal_moves))
    X = np.array([[white, black, mobility]])
    return model.predict(X)[0]

# ===================== UPDATE BOARD =====================
def update_board():
    for r in range(8):
        for c in range(8):
            color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
            buttons[(r, c)].config(bg=color, text="", fg="#000")
    for square, piece in board.piece_map().items():
        r = chess.square_rank(square)
        c = chess.square_file(square)
        display_r = 7 - r if not flipped else r
        display_c = c if not flipped else 7 - c
        buttons[(display_r, display_c)].config(text=piece_icons[piece.symbol()])
    score = evaluate_board(board)
    score_label.config(text=f"🧠 Board Eval: {score:.2f}\nTurn: {'White' if board.turn else 'Black'}")
    player_label.config(text=f"👑 You (White): {player_score}")
    ai_label.config(text=f"🤖 AI (Black): {ai_score}")

# ===================== PLAYER CLICK =====================
def on_click(r, c):
    global selected, player_score
    square = chess.square(c if not flipped else 7 - c,
                          7 - r if not flipped else r)
    piece = board.piece_at(square)
    if selected is None:
        if piece and piece.color == chess.WHITE:
            selected = square
            buttons[(r, c)].config(bg="#F7E96C")
    else:
        move = chess.Move(selected, square)
        if move in board.legal_moves:
            board.push(move)
            player_score += 1
            update_board()
            status_label.config(text=f"✅ You played: {move.uci()}")
            root.after(600, ai_move)
        else:
            status_label.config(text="❌ Illegal move!")
        selected = None
        update_board()

# ===================== AI MOVE =====================
def ai_move():
    global ai_score
    if board.is_game_over():
        status_label.config(text="🏁 Game Over!")
        return
    legal_moves = list(board.legal_moves)
    move_scores = []
    for mv in legal_moves:
        board.push(mv)
        score = evaluate_board(board)
        move_scores.append((score, mv))
        board.pop()
    best_move = max(move_scores, key=lambda x: x[0])[1]
    board.push(best_move)
    ai_score += 1
    update_board()
    status_label.config(text=f"🤖 AI played: {best_move.uci()}")

# ===================== UI =====================
title = tk.Label(root, text="♟️ Machine Learning Chess",
                 bg="#0f1112", fg="#FACC15", font=("Segoe UI", 26, "bold"))
title.pack(pady=10)

main_frame = tk.Frame(root, bg="#0f1112")
main_frame.pack(expand=True, fill="both", padx=25, pady=10)

# Chessboard
board_frame = tk.Frame(main_frame, bg="#0f1112")
board_frame.pack(side="left", padx=40, pady=20, expand=True)

btn_font = ('Segoe UI Symbol', 28, 'bold')
for r in range(8):
    for c in range(8):
        color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
        btn = tk.Button(board_frame, font=btn_font,
                        bg=color, fg="#000", relief="flat", bd=0,
                        activebackground="#F9F871",
                        command=lambda r=r, c=c: on_click(r, c))
        btn.grid(row=r, column=c, sticky="nsew")
        buttons[(r, c)] = btn

for i in range(8):
    board_frame.rowconfigure(i, weight=1)
    board_frame.columnconfigure(i, weight=1)

# Side Panel
side_frame = tk.Frame(main_frame, bg="#1e1e1e", relief="ridge", bd=2)
side_frame.pack(side="left", fill="both", padx=25, pady=20)

score_label = tk.Label(side_frame, text="", font=("Segoe UI", 16, "bold"),
                       bg="#1e1e1e", fg="#FACC15", justify="center")
score_label.pack(pady=20)

player_label = tk.Label(side_frame, text="👑 You (White): 0",
                        font=("Segoe UI", 15, "bold"),
                        bg="#1e1e1e", fg="#A3E635")
player_label.pack(pady=5)

ai_label = tk.Label(side_frame, text="🤖 AI (Black): 0",
                    font=("Segoe UI", 15, "bold"),
                    bg="#1e1e1e", fg="#60A5FA")
ai_label.pack(pady=5)

status_label = tk.Label(side_frame, text="Your Move! ♙",
                        font=("Segoe UI", 13, "italic"),
                        bg="#1e1e1e", fg="#66CCFF", wraplength=220, justify="center")
status_label.pack(pady=15)

# Buttons Section
def restart():
    global board, player_score, ai_score
    board = chess.Board()
    player_score = ai_score = 0
    update_board()
    status_label.config(text="♻️ New game started!")

def flip_board():
    global flipped
    flipped = not flipped
    update_board()
    status_label.config(text="🔄 Board flipped!")

def exit_game():
    root.destroy()

button_style = {"bg": "#333", "fg": "white", "font": ("Segoe UI", 12, "bold"),
                "relief": "flat", "width": 15, "height": 2, "bd": 0, "activebackground": "#555"}

tk.Button(side_frame, text="🔄 Restart Game", command=restart, **button_style).pack(pady=12)
tk.Button(side_frame, text="↕️ Flip Board", command=flip_board, **button_style).pack(pady=12)
tk.Button(side_frame, text="❌ Exit", command=exit_game, **button_style).pack(pady=12)

footer = tk.Label(root, text="Created by Syed M Arsalan Shah 🧠 | ML Chess UI ✨",
                  bg="#0f1112", fg="#777", font=("Segoe UI", 10, "italic"))
footer.pack(side="bottom", pady=6)

# ===================== Dynamic Font Resizing =====================
def resize_board(event):
    size = min(board_frame.winfo_width(), board_frame.winfo_height()) // 8
    font_size = max(18, size // 2)
    for btn in buttons.values():
        btn.config(font=("Segoe UI Symbol", font_size, "bold"))

root.bind("<Configure>", resize_board)

update_board()
root.mainloop()