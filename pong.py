"""
AI-USE SUMMARY
--------------
Tool: Claude (Anthropic), via the Claude chat interface.
Date: 2026-10-28

  - Wrote this Pong sketch from a prompt asking for two paddles driven by
    two 0-255 values read over serial from an ESP32.
  - Reused the structure of the existing p5py sketch from Haptics (AppState class,
    setup(), read_esp(), draw(), run(renderer="vispy")) so the two scripts
    stay consistent.
  - Wrote the ball physics, paddle collision, scoring, and serial buffering.
"""

from p5 import *
import serial
import time
import random

COM_PORT = 'COM4'
BAUD_RATE = 9600


class AppState:
    esp = None
    rx_buffer = b""

    # Raw paddle values from the ESP32 (0-255)
    y_raw = [127, 127]

    # Paddle geometry
    paddle_w = 12
    paddle_h = 80
    paddle_margin = 20

    # Ball
    ball_x = 0
    ball_y = 0
    ball_vx = 0
    ball_vy = 0
    ball_d = 14
    ball_speed = 4

    # Score: [left, right]
    score = [0, 0]


APP_STATE = AppState()


def reset_ball(direction=None):
    """Center the ball and launch it in a random (or given) direction."""
    APP_STATE.ball_x = width / 2
    APP_STATE.ball_y = height / 2
    APP_STATE.ball_speed = 4

    if direction is None:
        direction = random.choice([-1, 1])

    APP_STATE.ball_vx = direction * APP_STATE.ball_speed
    APP_STATE.ball_vy = random.uniform(-2, 2)


def setup():
    size(640, 360)
    stroke(255)

    print("Opening serial connection...")

    try:
        APP_STATE.esp = serial.Serial(
            COM_PORT,
            BAUD_RATE,
            timeout=0
        )
        time.sleep(2)
        APP_STATE.esp.reset_input_buffer()
        print("Connected to ESP32 on", COM_PORT)

    except serial.SerialException as e:
        print("Serial connection error:", e)
        APP_STATE.esp = None

    reset_ball()


def read_esp():
    esp = APP_STATE.esp

    if esp is None or not esp.is_open:
        return

    # Pull everything waiting and accumulate it, so partial lines
    # are held until their newline arrives
    if esp.in_waiting:
        APP_STATE.rx_buffer += esp.read(esp.in_waiting)

    if b"\n" not in APP_STATE.rx_buffer:
        return

    # Keep any trailing partial line; use only the most recent complete line
    *lines, APP_STATE.rx_buffer = APP_STATE.rx_buffer.split(b"\n")

    for raw in reversed(lines):
        try:
            line = raw.decode('utf-8').strip()

            if not line:
                continue

            values = line.split(',')

            if len(values) != 2:
                continue

            y_a, y_b = map(int, values)

            # Clamp to expected range
            APP_STATE.y_raw = [max(0, min(255, y_a)), max(0, min(255, y_b))]
            return

        except (ValueError, UnicodeDecodeError):
            print("Invalid serial data:", repr(raw))


def paddle_y(index):
    """Map a 0-255 reading to the paddle's top edge in screen pixels."""
    travel = height - APP_STATE.paddle_h
    return (APP_STATE.y_raw[index] / 255) * travel


def paddle_x(index):
    if index == 0:
        return APP_STATE.paddle_margin
    return width - APP_STATE.paddle_margin - APP_STATE.paddle_w


def update_ball():
    s = APP_STATE
    r = s.ball_d / 2

    s.ball_x += s.ball_vx
    s.ball_y += s.ball_vy

    # Bounce off top and bottom walls
    if s.ball_y - r < 0:
        s.ball_y = r
        s.ball_vy *= -1
    elif s.ball_y + r > height:
        s.ball_y = height - r
        s.ball_vy *= -1

    # Paddle collisions
    for i in range(2):
        px = paddle_x(i)
        py = paddle_y(i)

        within_y = py - r <= s.ball_y <= py + s.paddle_h + r
        within_x = px - r <= s.ball_x <= px + s.paddle_w + r

        moving_toward = (i == 0 and s.ball_vx < 0) or (i == 1 and s.ball_vx > 0)

        if within_x and within_y and moving_toward:
            # Speed up slightly on each hit
            s.ball_speed = min(s.ball_speed + 0.4, 12)

            # Deflection angle depends on where the ball hit the paddle
            hit = (s.ball_y - (py + s.paddle_h / 2)) / (s.paddle_h / 2)
            hit = max(-1, min(1, hit))

            direction = 1 if i == 0 else -1
            s.ball_vx = direction * s.ball_speed
            s.ball_vy = hit * s.ball_speed * 0.75

            # Push the ball out of the paddle
            if i == 0:
                s.ball_x = px + s.paddle_w + r
            else:
                s.ball_x = px - r

    # Scoring
    if s.ball_x < 0:
        s.score[1] += 1
        reset_ball(direction=-1)
    elif s.ball_x > width:
        s.score[0] += 1
        reset_ball(direction=1)


def draw():
    background(30)

    read_esp()
    update_ball()

    # Center line
    stroke(80)
    for y in range(0, int(height), 20):
        line((width / 2, y), (width / 2, y + 10))

    # Paddles
    stroke(255)
    fill(255)
    for i in range(2):
        rect((paddle_x(i), paddle_y(i)), APP_STATE.paddle_w, APP_STATE.paddle_h)

    # Ball
    circle(APP_STATE.ball_x, APP_STATE.ball_y, APP_STATE.ball_d)

    # Score
    # text(str(APP_STATE.score[0]), (width / 2 - 40, 20))
    # text(str(APP_STATE.score[1]), (width / 2 + 30, 20))


if __name__ == '__main__':
    print("Starting application...")
    run(renderer="vispy")