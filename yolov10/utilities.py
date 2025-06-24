import mysql.connector

def center_window(window):
    window.update_idletasks()  # Cập nhật kích thước thực của window
    w = window.winfo_width()
    h = window.winfo_height()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{x}+{y}")
    
def fetch_data(query):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    
def draw_horizontal_gradient(canvas, color1, color2, width, height):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / width
    g_ratio = (g2 - g1) / width
    b_ratio = (b2 - b1) / width

    for i in range(width):
        nr = int(r1 + (r_ratio * i)) >> 8
        ng = int(g1 + (g_ratio * i)) >> 8
        nb = int(b1 + (b_ratio * i)) >> 8
        color = f'#{nr:02x}{ng:02x}{nb:02x}'
        canvas.create_line(i, 0, i, height, fill=color)