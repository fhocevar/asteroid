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

# Carrega imagens
nave_img = pygame.image.load("nave.png")  # Substitua por uma imagem de nave
nave_img = pygame.transform.scale(nave_img, (50, 50))

# Configurações do jogador
nave = pygame.Rect(225, 500, 50, 50)
velocidade_nave = 5

# Configurações dos asteroides
asteroides = []
velocidade_asteroide = 3
tempo_ultimo_asteroide = 0

# Fonte para pontuação
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

    # Movendo asteroides
    for asteroide in asteroides[:]:
        asteroide.y += velocidade_asteroide
        if asteroide.y > ALTURA:
            asteroides.remove(asteroide)
            pontuacao += 1  # Ganha pontos ao sobreviver

    # Verifica colisão
    for asteroide in asteroides:
        if nave.colliderect(asteroide):
            rodando = False  # Fim de jogo

    # Desenha nave
    tela.blit(nave_img, (nave.x, nave.y))

    # Desenha asteroides
    for asteroide in asteroides:
        pygame.draw.rect(tela, VERMELHO, asteroide)

    # Mostra pontuação
    texto = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
