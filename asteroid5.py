import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 500, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Nave")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
AMARELO = (255, 255, 0)
CINZA = (169, 169, 169)
MARROM = (139, 69, 19)

# Carrega imagens com transparência
try:
    nave_img = pygame.image.load("nave2.png").convert_alpha()
    nave_img = pygame.transform.scale(nave_img, (50, 50))
    print("Imagem da nave carregada com sucesso!")
except pygame.error:
    print("Erro ao carregar a imagem da nave.")
    nave_img = None

try:
    powerup_img = pygame.image.load("powerup.png").convert_alpha()
    powerup_img = pygame.transform.scale(powerup_img, (30, 30))
except pygame.error:
    print("Erro ao carregar a imagem do power-up.")

# Carrega sons
som_explosao = pygame.mixer.Sound("explosao.wav")
som_powerup = pygame.mixer.Sound("powerup.wav")
som_tiro = pygame.mixer.Sound("tiro.wav")

# Configurações do jogador
nave = pygame.Rect(225, 450, 50, 50)  # Ajustada a posição para garantir visibilidade
velocidade_nave = 5
vidas = 3
escudo_ativo = False

# Configurações dos asteroides
asteroides = []
velocidade_asteroide = 3
tempo_ultimo_asteroide = 0

# Configurações dos power-ups
powerups = []
tempo_ultimo_powerup = 0

# Configurações dos tiros
tiros = []
velocidade_tiro = 7

# Fonte para pontuação e vidas
fonte = pygame.font.Font(None, 36)
pontuacao = 0

# Função para desenhar asteroides com formas aleatórias
def desenhar_asteroide(asteroide, cor):
    # Número de lados do polígono
    lados = random.choice([6, 7, 8])  # Hexágono, Heptágono, Octógono
    raio = asteroide.width // 2
    centro = (asteroide.x + raio, asteroide.y + raio)

    # Calculando os pontos para o polígono
    pontos = []
    for i in range(lados):
        angulo = math.radians((360 / lados) * i)
        x = centro[0] + raio * math.cos(angulo)
        y = centro[1] + raio * math.sin(angulo)
        pontos.append((x, y))

    pygame.draw.polygon(tela, cor, pontos)

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    tela.fill((0, 0, 0))  # Fundo preto
    tempo_atual = pygame.time.get_ticks()

    # Captura eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                tiro = pygame.Rect(nave.x + 22, nave.y, 6, 15)
                tiros.append(tiro)
                som_tiro.play()

    # Movimento da nave
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave.x > 0:
        nave.x -= velocidade_nave
    if teclas[pygame.K_RIGHT] and nave.x < LARGURA - 50:
        nave.x += velocidade_nave

    # Criar novos asteroides periodicamente
    if tempo_atual - tempo_ultimo_asteroide > 700:
        asteroide = pygame.Rect(random.randint(0, LARGURA - 40), 0, 40, 40)
        asteroides.append(asteroide)
        tempo_ultimo_asteroide = tempo_atual

    # Criar power-ups periodicamente
    if tempo_atual - tempo_ultimo_powerup > 5000:
        powerup = pygame.Rect(random.randint(0, LARGURA - 30), 0, 30, 30)
        powerups.append(powerup)
        tempo_ultimo_powerup = tempo_atual

    # Movendo tiros
    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro
        if tiro.y < 0:
            tiros.remove(tiro)

    # Movendo asteroides
    for asteroide in asteroides[:]:
        asteroide.y += velocidade_asteroide
        if asteroide.y > ALTURA:
            asteroides.remove(asteroide)
            pontuacao += 1

    # Movendo power-ups
    for powerup in powerups[:]:
        powerup.y += 2
        if powerup.y > ALTURA:
            powerups.remove(powerup)

    # Verifica colisão com power-ups
    for powerup in powerups[:]:
        if nave.colliderect(powerup):
            escudo_ativo = True
            som_powerup.play()
            powerups.remove(powerup)

    # Verifica colisão dos tiros com asteroides
    for tiro in tiros[:]:
        for asteroide in asteroides[:]:
            if tiro.colliderect(asteroide):
                tiros.remove(tiro)
                asteroides.remove(asteroide)
                pontuacao += 5
                som_explosao.play()
                break

    # Verifica colisão com asteroides
    for asteroide in asteroides[:]:
        if nave.colliderect(asteroide):
            if escudo_ativo:
                escudo_ativo = False
            else:
                vidas -= 1
                som_explosao.play()
            asteroides.remove(asteroide)
            if vidas == 0:
                rodando = False

    # Desenha nave
    if nave_img:
        tela.blit(nave_img, (nave.x, nave.y))
    else:
        pygame.draw.rect(tela, (0, 255, 0), nave)

    # Desenha tiros
    for tiro in tiros:
        pygame.draw.rect(tela, AMARELO, tiro)

    # Desenha asteroides
    for asteroide in asteroides:
        cor_asteroide = random.choice([MARROM, CINZA, BRANCO])  # Cores aleatórias
        desenhar_asteroide(asteroide, cor_asteroide)

    # Desenha power-ups
    for powerup in powerups:
        tela.blit(powerup_img, (powerup.x, powerup.y))

    # Mostra pontuação e vidas
    tela.blit(fonte.render(f"Pontos: {pontuacao}", True, BRANCO), (10, 10))
    tela.blit(fonte.render(f"Vidas: {vidas}", True, BRANCO), (400, 10))
    if escudo_ativo:
        tela.blit(fonte.render("Escudo Ativo!", True, AZUL), (180, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
