import pygame
import random

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

# Carrega imagens
nave_img = pygame.image.load("nave.png")  # Substitua por uma imagem de nave
nave_img = pygame.transform.scale(nave_img, (50, 50))

powerup_img = pygame.image.load("powerup.png")  # Ícone do escudo
powerup_img = pygame.transform.scale(powerup_img, (30, 30))

# Carrega sons
som_explosao = pygame.mixer.Sound("explosao.wav")
som_powerup = pygame.mixer.Sound("powerup.wav")

# Configurações do jogador
nave = pygame.Rect(225, 500, 50, 50)
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

# Fonte para pontuação e vidas
fonte = pygame.font.Font(None, 36)
pontuacao = 0

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
    if tempo_atual - tempo_ultimo_powerup > 5000:  # A cada 5 segundos
        powerup = pygame.Rect(random.randint(0, LARGURA - 30), 0, 30, 30)
        powerups.append(powerup)
        tempo_ultimo_powerup = tempo_atual

    # Movendo asteroides
    for asteroide in asteroides[:]:
        asteroide.y += velocidade_asteroide
        if asteroide.y > ALTURA:
            asteroides.remove(asteroide)
            pontuacao += 1  # Ganha pontos ao sobreviver

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

    # Verifica colisão com asteroides
    for asteroide in asteroides[:]:
        if nave.colliderect(asteroide):
            if escudo_ativo:
                escudo_ativo = False  # Perde o escudo, mas não uma vida
            else:
                vidas -= 1
                som_explosao.play()
            asteroides.remove(asteroide)
            if vidas == 0:
                rodando = False  # Fim de jogo

    # Desenha nave
    tela.blit(nave_img, (nave.x, nave.y))

    # Desenha asteroides
    for asteroide in asteroides:
        pygame.draw.rect(tela, VERMELHO, asteroide)

    # Desenha power-ups
    for powerup in powerups:
        tela.blit(powerup_img, (powerup.x, powerup.y))

    # Mostra pontuação
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    # Mostra vidas
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, BRANCO)
    tela.blit(texto_vidas, (400, 10))

    # Mostra se o escudo está ativo
    if escudo_ativo:
        texto_escudo = fonte.render("Escudo Ativo!", True, AZUL)
        tela.blit(texto_escudo, (180, 10))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
