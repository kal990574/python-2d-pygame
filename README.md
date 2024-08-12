```python
 🔨Game project with pygame library
    project 1: avoid obstacle game
    project 2: divide ball game
    project 3: bubble pop game
```
## 알고리즘 및 게임 개발 기능 구현

### 1. 인접 객체 추적을 위한 깊이 우선 탐색 (DFS) 알고리즘 구현
깊이 우선 탐색(DFS) 알고리즘을 구현하여 그래프 또는 트리 구조에서 인접 객체를 효율적으로 추적합니다. 이 알고리즘은 재귀적 방식으로 구현될 수 있으며, 연결된 요소들을 탐색하는 데 유용합니다.

```python
def dfs(node, visited, adj):
    visited.add(node)
    print(f"Visited node {node}")

    for neighbor in adj[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, adj)

# 그래프 예시: 각 노드가 연결된 노드를 리스트로 표현
adjacency_list = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0],
    3: [1],
    4: [1]
}

visited = set()
dfs(0, visited, adjacency_list)
```

### 2. 이미지 스프라이트 관리를 위해 Pygame 내 `sprite` 클래스를 활용
`Pygame`의 `sprite` 클래스를 활용하여 게임 내 이미지 스프라이트를 효율적으로 관리합니다. 이를 통해 게임 객체의 애니메이션, 충돌 처리 등을 손쉽게 구현할 수 있습니다.

```python
import pygame

# Pygame 초기화
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self):
        # 스프라이트 업데이트 로직 (예: 움직임)
        self.rect.x += 5

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()

# 플레이어 스프라이트 생성 및 그룹에 추가
player = Player("player.png", (100, 100))
all_sprites.add(player)

# 게임 루프 예시
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # 화면 그리기
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
```
