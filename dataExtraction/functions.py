import os
import time
import random

def human_delay(mean_delay=2, sigma=1):
    """Delay exponencial con lambda de distribución normal centrada en 1/mean_delay."""
    while True:
        lam = random.gauss(1/mean_delay, sigma)
        if lam > 0:
            return random.expovariate(lam)

def human_typing(elem, text):
    """Simula tipeo humano caracter a caracter."""
    for ch in text:
        elem.send_keys(ch)
        time.sleep(random.uniform(0.05, 0.4))

def random_mouse_movements(action, range_px=300, steps=10, pause=(0.05, 0.2)):
    """Movimientos aleatorios del ratón."""
    for _ in range(steps):
        x = random.randint(-range_px, range_px)
        y = random.randint(-range_px, range_px)
        try:
            action.move_by_offset(x, y).perform()
            time.sleep(random.uniform(*pause))
        except:
            pass
        action.reset_actions()

def random_scrolls(driver, pause=(0.5, 1.5)):
    """Scrolls aleatorios: número de 2 a 15 basado en exponencial con media 4."""
    lam = abs(random.gauss(1/4, 0.05))
    count = int(random.expovariate(lam))
    count = max(2, min(count, 15))
    for _ in range(count):
        amt = random.randint(100, 500) * random.choice([1, -1])
        driver.execute_script(f"window.scrollBy(0, {amt});")
        time.sleep(random.uniform(*pause))

def random_pause_between_actions(prob=1):
    """Pausas largas ocasionales para simular pensamientos."""
    if random.random() < prob:
        time.sleep(human_delay())

def wait_for_download(download_dir, timeout=120):
    """Espera hasta que aparezca y complete una nueva descarga."""
    before = set(os.listdir(download_dir))
    end_time = time.time() + timeout
    while time.time() < end_time:
        after = set(os.listdir(download_dir))
        added = after - before
        if added:
            fname = added.pop()
            while fname.endswith('.crdownload') or os.path.exists(os.path.join(download_dir, fname + '.crdownload')):
                time.sleep(1)
                current = set(os.listdir(download_dir))
                new = current - before
                if new:
                    fname = next(iter(new))
            return os.path.join(download_dir, fname)
        time.sleep(1)
    return None
