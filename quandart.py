import pygame
import random
import sys
import math

# --- AYARLAR ---
RENK_ARKA_PLAN = (5, 5, 12)
RENK_CYAN = (0, 255, 255)
RENK_MAGENTA = (255, 0, 255)
RENK_YESIL = (0, 255, 100)
RENK_KIRMIZI = (255, 30, 30)
RENK_MAVI = (30, 100, 255)
RENK_ALTIN = (255, 215, 0)
RENK_BEYAZ = (255, 255, 255)
RENK_GRI = (100, 100, 100)

ATIS_HAKKI = 3

# --- PYGAME BAŞLATMA ---
pygame.init()

info = pygame.display.Info()
GENISLIK = info.current_w
YUKSEKLIK = info.current_h
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK), pygame.FULLSCREEN)
pygame.display.set_caption("ULTRA KUANTUM DART - SETUP")
saat = pygame.time.Clock()


# --- FONT AYARLARI ---
def get_font(size, bold=True):
    try:
        return pygame.font.SysFont("arial", size, bold=bold)
    except:
        return pygame.font.Font(None, size)


font_kucuk = get_font(int(min(YUKSEKLIK * 0.022, GENISLIK * 0.012)))
font_orta = get_font(int(min(YUKSEKLIK * 0.035, GENISLIK * 0.02)))
font_buyuk = get_font(int(min(YUKSEKLIK * 0.07, GENISLIK * 0.04)))
font_dev = get_font(int(min(YUKSEKLIK * 0.15, GENISLIK * 0.08)))


# --- YARDIMCI FONKSİYON: GLOW TEXT ---
def ciz_glow_text(surface, text, font, renk, x, y, align="center"):
    text_surf = font.render(text, True, renk)
    text_rect = text_surf.get_rect()

    if align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
    else:
        text_rect.topleft = (x, y)

    # Basit gölge
    golge = font.render(text, True, (renk[0] // 3, renk[1] // 3, renk[2] // 3))
    surface.blit(golge, (text_rect.x + 2, text_rect.y + 2))
    surface.blit(text_surf, text_rect)


# --- SINIFLAR (OYUN İÇİ) ---
class Partikül:
    def __init__(self, x, y, renk):
        self.x = x
        self.y = y
        self.renk = renk
        self.boyut = random.randint(3, 7)
        angle = random.uniform(0, 6.28)
        speed = random.uniform(3, 12)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.omur = 255

    def guncelle(self):
        self.x += self.vx
        self.y += self.vy
        self.omur -= 4
        self.boyut *= 0.96

    def ciz(self, surface):
        if self.omur > 0:
            s = pygame.Surface((int(self.boyut * 2), int(self.boyut * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.renk, int(self.omur)), (int(self.boyut), int(self.boyut)), int(self.boyut))
            surface.blit(s, (self.x - self.boyut, self.y - self.boyut))


class SokDalgasi:
    def __init__(self, x, y, renk):
        self.x = x
        self.y = y
        self.renk = renk
        self.yaricap = 50
        self.kalinlik = 15
        self.alpha = 200

    def guncelle(self):
        self.yaricap += 20
        self.kalinlik = max(1, self.kalinlik * 0.92)
        self.alpha -= 6

    def ciz(self, surface):
        if self.alpha > 0:
            temp_surface = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.renk, int(self.alpha)), (self.x, self.y), int(self.yaricap),
                               int(self.kalinlik))
            surface.blit(temp_surface, (0, 0))


# --- KURULUM YÖNETİCİSİ (SETUP) ---
class KurulumYoneticisi:
    def __init__(self):
        self.adim = "SAYI_GIRIS"  # SAYI_GIRIS, ISIM_GIRIS
        self.girilen_metin = ""
        self.oyuncu_sayisi = 0
        self.isimler = []
        self.suanki_isim_sirasi = 1
        self.tamamlandi = False
        self.cursor_blink = 0

    def veri_isle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter tuşu
                if self.adim == "SAYI_GIRIS":
                    try:
                        sayi = int(self.girilen_metin)
                        if sayi > 0:
                            self.oyuncu_sayisi = sayi
                            self.adim = "ISIM_GIRIS"
                            self.girilen_metin = ""
                    except:
                        self.girilen_metin = ""  # Hatalı giriş silinir

                elif self.adim == "ISIM_GIRIS":
                    isim = self.girilen_metin.strip()
                    if not isim:
                        isim = f"Yarışmacı {self.suanki_isim_sirasi}"

                    self.isimler.append(isim)
                    self.suanki_isim_sirasi += 1
                    self.girilen_metin = ""

                    if len(self.isimler) >= self.oyuncu_sayisi:
                        self.tamamlandi = True

            elif event.key == pygame.K_BACKSPACE:
                self.girilen_metin = self.girilen_metin[:-1]
            else:
                # Sadece mantıklı karakterleri al, çok uzatmasın
                if len(self.girilen_metin) < 12:
                    self.girilen_metin += event.unicode

    def ciz(self, ekran):
        ekran.fill(RENK_ARKA_PLAN)

        # Basit arka plan ızgarası
        for i in range(0, GENISLIK, 100): pygame.draw.line(ekran, (20, 20, 30), (i, 0), (i, YUKSEKLIK))
        for i in range(0, YUKSEKLIK, 100): pygame.draw.line(ekran, (20, 20, 30), (0, i), (GENISLIK, i))

        cx, cy = GENISLIK // 2, YUKSEKLIK // 2

        if self.adim == "SAYI_GIRIS":
            baslik = "KAÇ YARIŞMACI OLACAK?"
            renk = RENK_MAGENTA
            alt_bilgi = "(Sayı girin ve ENTER'a basın)"
        else:
            baslik = f"{self.suanki_isim_sirasi}. YARIŞMACI İSMİ?"
            renk = RENK_CYAN
            alt_bilgi = "(İsim yazın ve ENTER'a basın)"

        # Başlık
        ciz_glow_text(ekran, baslik, font_buyuk, renk, cx, cy - 100)

        # Giriş Kutusu
        kutu_genislik = 400
        kutu_yukseklik = 80
        pygame.draw.rect(ekran, (20, 30, 40),
                         (cx - kutu_genislik // 2, cy - kutu_yukseklik // 2, kutu_genislik, kutu_yukseklik),
                         border_radius=10)
        pygame.draw.rect(ekran, renk,
                         (cx - kutu_genislik // 2, cy - kutu_yukseklik // 2, kutu_genislik, kutu_yukseklik), 3,
                         border_radius=10)

        # Girilen Metin
        text_surf = font_buyuk.render(self.girilen_metin, True, RENK_BEYAZ)
        text_rect = text_surf.get_rect(center=(cx, cy))
        ekran.blit(text_surf, text_rect)

        # İmleç (Cursor) yanıp sönme
        self.cursor_blink += 1
        if self.cursor_blink % 60 < 30:
            cursor_x = text_rect.right + 5
            pygame.draw.line(ekran, RENK_BEYAZ, (cursor_x, text_rect.top + 10), (cursor_x, text_rect.bottom - 10), 2)

        # Alt bilgi
        ciz_glow_text(ekran, alt_bilgi, font_kucuk, (150, 150, 150), cx, cy + 80)


# --- OYUN YÖNETİCİSİ ---
class OyunYoneticisi:
    def __init__(self, oyuncu_listesi):
        self.oyuncular = oyuncu_listesi
        self.sifirla()
        self.partikuller = []
        self.sok_dalgalari = []
        self.arka_plan_yildizlari = [[random.randint(0, GENISLIK), random.randint(0, YUKSEKLIK), random.randint(1, 2)]
                                     for _ in range(100)]
        self.zaman = 0

    def sifirla(self):
        self.skorlar = {y: [None] * ATIS_HAKKI for y in self.oyuncular}
        self.toplamlar = {y: 0 for y in self.oyuncular}
        self.gosterilen_toplamlar = {y: 0.0 for y in self.oyuncular}
        self.suanki_oyuncu_idx = 0
        self.suanki_atis_idx = 0
        self.oyun_bitti = False
        self.merkez_mesaj = "SİSTEM HAZIR"
        self.merkez_alt_mesaj = f"İLK ATICI: {self.oyuncular[0].upper()}"
        self.merkez_renk = RENK_CYAN
        self.flash_alpha = 0

    def atis_yap(self, kapi_tipi):
        if self.oyun_bitti: return

        oyuncu = self.oyuncular[self.suanki_oyuncu_idx]
        sistem_puani = random.randint(10, 90)
        sonuc_puani = 0

        # Karavana kontrolü
        if kapi_tipi == 'KARAVANA':
            sonuc_puani = 0
            self.merkez_renk = RENK_GRI
            msg = "KARAVANA"
            sistem_puani = 0
        elif kapi_tipi == 'X':
            sonuc_puani = 100 - sistem_puani
            self.merkez_renk = RENK_YESIL
            msg = "X - FLIP"
        elif kapi_tipi == 'Z':
            sonuc_puani = -1 * sistem_puani
            self.merkez_renk = RENK_KIRMIZI
            msg = "Z - PHASE"
        else:  # I
            sonuc_puani = sistem_puani
            self.merkez_renk = RENK_MAVI
            msg = "I - IDENTITY"

        self.skorlar[oyuncu][self.suanki_atis_idx] = sonuc_puani
        self.toplamlar[oyuncu] += sonuc_puani

        self.merkez_mesaj = str(sonuc_puani)
        if kapi_tipi == 'KARAVANA':
            self.merkez_alt_mesaj = "HEDEF ISKALANDI"
        else:
            self.merkez_alt_mesaj = f"{msg} | GİRDİ: {sistem_puani}"

        # HUD Animasyon
        panel_genislik = int(GENISLIK * 0.35)
        hud_x = panel_genislik + (GENISLIK - panel_genislik) // 2
        hud_y = YUKSEKLIK // 2
        self.efekt_olustur(hud_x, hud_y, self.merkez_renk, miktar=50)
        self.flash_alpha = 100

        # Sıradaki oyuncu
        self.suanki_oyuncu_idx += 1
        if self.suanki_oyuncu_idx >= len(self.oyuncular):
            self.suanki_oyuncu_idx = 0
            self.suanki_atis_idx += 1

        if self.suanki_atis_idx >= ATIS_HAKKI:
            self.oyunu_bitir()
        else:
            if not self.oyun_bitti:
                # Bir sonraki atıcının ismini küçük bilgi olarak geçebiliriz (opsiyonel)
                pass

    def oyunu_bitir(self):
        self.oyun_bitti = True
        kazanan = max(self.toplamlar, key=self.toplamlar.get)
        self.merkez_mesaj = str(self.toplamlar[kazanan])
        self.merkez_alt_mesaj = f"KAZANAN: {kazanan.upper()}"
        self.merkez_renk = RENK_ALTIN
        panel_genislik = int(GENISLIK * 0.35)
        hud_x = panel_genislik + (GENISLIK - panel_genislik) // 2
        hud_y = YUKSEKLIK // 2
        self.efekt_olustur(hud_x, hud_y, RENK_ALTIN, miktar=100)

    def efekt_olustur(self, x, y, renk, miktar=30):
        for _ in range(miktar):
            self.partikuller.append(Partikül(x, y, renk))
        self.sok_dalgalari.append(SokDalgasi(x, y, renk))

    def guncelle_ve_ciz(self):
        self.zaman += 1
        ekran.fill(RENK_ARKA_PLAN)

        # Yıldızlar
        for yildiz in self.arka_plan_yildizlari:
            yildiz[0] -= yildiz[2] * 0.5
            if yildiz[0] < 0:
                yildiz[0] = GENISLIK
                yildiz[1] = random.randint(0, YUKSEKLIK)
            pygame.draw.circle(ekran, (80, 80, 100), (int(yildiz[0]), int(yildiz[1])), yildiz[2])

        # Grid
        grid_renk = (30, 40, 60)
        for i in range(0, GENISLIK, 100):
            pygame.draw.line(ekran, grid_renk, (i, 0), (i, YUKSEKLIK), 1)
        for i in range(0, YUKSEKLIK, 100):
            pygame.draw.line(ekran, grid_renk, (0, i), (GENISLIK, i), 1)

        self.ciz_skor_tablosu()
        self.ciz_hud()

        # Efektler
        for p in self.partikuller[:]:
            p.guncelle()
            p.ciz(ekran)
            if p.omur <= 0: self.partikuller.remove(p)

        for s in self.sok_dalgalari[:]:
            s.guncelle()
            s.ciz(ekran)
            if s.alpha <= 0: self.sok_dalgalari.remove(s)

        if self.flash_alpha > 0:
            s_flash = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
            s_flash.fill((255, 255, 255, int(self.flash_alpha)))
            ekran.blit(s_flash, (0, 0))
            self.flash_alpha -= 5

    def ciz_skor_tablosu(self):
        panel_w = int(GENISLIK * 0.35)
        x_baslangic = 40
        y_baslangic = 60

        ciz_glow_text(ekran, "KUANTUM SKOR", font_orta, RENK_MAGENTA, x_baslangic + 100, 40)
        pygame.draw.line(ekran, RENK_MAGENTA, (x_baslangic, y_baslangic + 10), (panel_w, y_baslangic + 10), 2)

        kalan_yukseklik = YUKSEKLIK - 150
        row_h = min(80, kalan_yukseklik / max(1, len(self.oyuncular)))

        for idx, oyuncu in enumerate(self.oyuncular):
            y_pos = y_baslangic + 50 + (idx * row_h)
            aktif = (idx == self.suanki_oyuncu_idx and not self.oyun_bitti)
            rect_area = (x_baslangic, y_pos, panel_w - 40, row_h - 10)

            renk_kutu = (20, 30, 45) if not aktif else (10, 50, 70)
            pygame.draw.rect(ekran, renk_kutu, rect_area, border_radius=8)

            if aktif:
                pygame.draw.rect(ekran, RENK_CYAN, rect_area, 2, border_radius=8)
                # O anki oyuncunun yanına ok
                pygame.draw.polygon(ekran, RENK_CYAN, [
                    (x_baslangic - 20, y_pos + row_h / 2 - 15),
                    (x_baslangic - 20, y_pos + row_h / 2 + 5),
                    (x_baslangic - 5, y_pos + row_h / 2 - 5)
                ])

            ciz_glow_text(ekran, oyuncu, font_kucuk, RENK_BEYAZ, x_baslangic + 15, y_pos + (row_h / 2 - 10),
                          align="left")

            col_width = (panel_w - 120) / 4
            for i in range(ATIS_HAKKI):
                puan = self.skorlar[oyuncu][i]
                txt = "." if puan is None else str(puan)
                c = (100, 100, 100)
                if puan is not None:
                    c = RENK_YESIL if puan > 0 else RENK_KIRMIZI
                    if puan == 0: c = RENK_GRI

                px = x_baslangic + (panel_w * 0.45) + (i * col_width * 0.8)
                ciz_glow_text(ekran, txt, font_kucuk, c, px, y_pos + (row_h / 2 - 10))

            hedef = self.toplamlar[oyuncu]
            mevcut = self.gosterilen_toplamlar[oyuncu]
            if mevcut < hedef:
                self.gosterilen_toplamlar[oyuncu] += 0.5 if (hedef - mevcut) < 5 else 1
            elif mevcut > hedef:
                self.gosterilen_toplamlar[oyuncu] -= 0.5 if (mevcut - hedef) < 5 else 1

            gosterilecek = int(self.gosterilen_toplamlar[oyuncu])
            renk_toplam = RENK_ALTIN if gosterilecek >= 0 else RENK_KIRMIZI
            ciz_glow_text(ekran, str(gosterilecek), font_orta, renk_toplam, x_baslangic + panel_w - 60,
                          y_pos + (row_h / 2 - 15), align="right")

    def ciz_hud(self):
        panel_genislik = int(GENISLIK * 0.35)
        cx = panel_genislik + (GENISLIK - panel_genislik) // 2
        cy = YUKSEKLIK // 2
        base_radius = min(GENISLIK, YUKSEKLIK) * 0.22

        pygame.draw.circle(ekran, (30, 40, 50), (cx, cy), base_radius, 2)
        pygame.draw.circle(ekran, self.merkez_renk, (cx, cy), base_radius + 5, 1)

        for i in range(3):
            angle_offset = (self.zaman * (1 + i * 0.5)) % 360
            rect_r = base_radius - (20 + i * 30)
            rect = (cx - rect_r, cy - rect_r, rect_r * 2, rect_r * 2)
            pygame.draw.arc(ekran, self.merkez_renk, rect, math.radians(angle_offset), math.radians(angle_offset + 120),
                            4)

        ciz_glow_text(ekran, self.merkez_mesaj, font_dev, self.merkez_renk, cx, cy - 20, align="center")

        kutu_w = min(600, GENISLIK * 0.4)
        kutu_h = 50
        kutu_x = cx - kutu_w // 2
        kutu_y = cy + base_radius + 40
        pygame.draw.rect(ekran, (10, 15, 20), (kutu_x, kutu_y, kutu_w, kutu_h), border_radius=5)
        pygame.draw.rect(ekran, self.merkez_renk, (kutu_x, kutu_y, kutu_w, kutu_h), 1, border_radius=5)
        ciz_glow_text(ekran, self.merkez_alt_mesaj, font_kucuk, RENK_BEYAZ, cx, kutu_y + 15, align="center")

        if self.oyun_bitti:
            anim_text = "[R] YENİDEN BAŞLAT"
            alpha = abs(math.sin(self.zaman * 0.05)) * 255
            s = font_orta.render(anim_text, True, RENK_ALTIN)
            s.set_alpha(alpha)
            r = s.get_rect(center=(cx, YUKSEKLIK - 80))
            ekran.blit(s, r)
        else:
            bilgi = "[X] BIT | [Z] PHASE | [I] IDENTITY | [SPACE] KARAVANA"
            ciz_glow_text(ekran, bilgi, font_kucuk, (150, 150, 170), cx, YUKSEKLIK - 50, align="center")


# --- MAIN LOOP ---

# Aşama 1: Kurulum (Setup)
setup = KurulumYoneticisi()
setup_running = True

while setup_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            setup.veri_isle(event)

    setup.ciz(ekran)
    pygame.display.flip()
    saat.tick(60)

    if setup.tamamlandi:
        setup_running = False

# Aşama 2: Ana Oyun
oyun = OyunYoneticisi(setup.isimler)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if oyun.oyun_bitti:
                if event.key == pygame.K_r:
                    # Resetleme mantığı: İsimleri koruyarak resetle
                    oyun.sifirla()
            else:
                if event.key == pygame.K_x:
                    oyun.atis_yap('X')
                elif event.key == pygame.K_z:
                    oyun.atis_yap('Z')
                elif event.key == pygame.K_i or event.key == pygame.K_1:
                    oyun.atis_yap('I')
                elif event.key == pygame.K_SPACE or event.key == pygame.K_0:
                    oyun.atis_yap('KARAVANA')

    oyun.guncelle_ve_ciz()
    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()