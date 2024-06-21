# Geometoid - 추가기능 구현 버전

# 구현 목표

* 본 프로젝트는 간단한 탑다운 2D 슈팅 게임을 구현하는 것을 목표로 합니다. 플레이어는 3가지 종류의 적에 맞서 스테이지를 생존해야 하며 체력이 0이 되면 종료됩니다.

# 구현 기능
* pygame 기반 게임 환경 구현
* 키보드 입력으로 플레이어 이동
* 마우스 조작으로 플레이어 조준 및 공격
* 3가지 종류의 적 및 기초 인공지능
* 객체간의 충돌 처리
* 스테이지 흐름 제어 기능  

# 추가 구현 기능
* 플레이어 객체의 데미지 효과
* 게임 시작 메뉴와 재도전 기능
* 마우스 우클릭 시 무적 모드 발동

[![Watch Demo](https://raw.githubusercontent.com/ysan9500/geometoid/main/demo/phase2_demo_thumbnail.png)](https://raw.githubusercontent.com/ysan9500/geometoid/main/demo/phase2_demo.mp4)

# Reference
[1] https://github.com/pygame/pygame "pygame"

# 지원 Operating Systems 및 실행 방법

## 지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :x: (확인 필요) |
| Linux  | :o:  |
|MacOS   | :x: (확인 필요) |

본 프로젝트는 Ubuntu 22.04 LTS 환경에서 개발 및 테스트 되었으며 다른 환경에서의 동작은 테스트되지 않았습니다. 그러나 pygame을 통해 개발되었기 때문에 다른 환경에서도 동작이 가능할 것으로 예상됩니다.

## 실행 방법
### Windows
https://github.com/pygame/pygame 참조하여 설치 후 확인 필요

### Linux

1. python3 설치
```bash
sudo apt-get install python3
```
2. pygame 설치
```bash
pip3 install pygame
```
3. 프로젝트 폴더 내부에서 main.py 실행
```bash
python3 main.py
```

### MacOS
https://github.com/pygame/pygame 참조하여 설치 후 확인 필요


# 실행 예시
![example](https://github.com/illuminoplanet/geometoid/assets/61686504/36e60197-bd3f-4edd-a273-8f19a9ad4025)

# 코드 설명
## main.py
### 메인 루프
- 상태 업데이트
  1. player.update(mouse, keys): 플레이어 상태를 업데이트.
  2. stage.update(player): 스테이지 상태를 업데이트.

- 화면 렌더링
  1. stage.draw(screen, font): 스테이지 관련 렌더링.
  2. player.draw(screen, font): 플레이어 관련 렌더링.


## player.py
### 클래스 Player
설명: 게임 내에서 플레이어 캐릭터를 정의하고 조작하는 클래스.

- draw(screen, font): 플레이어와 발사체를 화면에 그리는 메서드.

  1. 플레이어의 체력이 0 이하일 경우 "Game Over" 메시지를 표시.
  2. 발사체를 순회하며 각 발사체를 렌더링.
  3. 플레이어 이미지를 마우스에 맞게 회전시켜 화면에 렌더링.
  4. 화면 좌측 상단에 플레이어의 체력을 표시.

- update(mouse, keys): 플레이어와 발사체 상태를 업데이트하는 메서드.
  1. 가속도와 마찰력을 반영하여 속도 업데이트.
  2. 플레이어의 위치를 화면 안에 유지.
  3. 발사 조작시 쿨다운 시간 마다 발사체를 생성.

- take_damage(damage): 플레이어가 피해를 입었을 때 체력을 감소시키는 메서드.

## projectile.py
### 클래스 Projectile
설명: 플레이어가 발사하는 발사체를 정의하는 클래스.

- update(): 발사체의 상태를 업데이트하는 메서드.
  1. 발사체의 위치를 속도에 따라 이동.
  2. 발사체가 화면 경계 밖으로 나가면 삭제.

- draw(screen): 발사체를 화면에 그리는 메서드.
  1. 발사체를 방향에 맞게 회전시켜 렌더링.


## stage.py
### 클래스 Stage
설명: 게임 스테이지를 관리하고, 적을 생성하며, 각 라운드를 진행하는 클래스.
- update(player): 스테이지와 적 상태를 업데이트하는 메서드.
  1. 적 상태 업데이트
  2. 객체간의 충돌 처리
  3. 현재 적이 모두 제거된 경우 다음 웨이브 시작
  3. 모든 적이 제거된 경우 준비 상태로 전환하고 다음 라운드 준비.

- plan_round(): 다음 라운드를 계획하는 메서드.
  1. 라운드에 따라 웨이브 수를 계산하고, 각 웨이브에 포함될 적을 생성하여 대기 리스트에 추가.
  2. 준비 상태 해제.

- spawn_enemies(): 대기 중인 적을 스테이지에 소환하는 메서드.
  1. 대기 리스트에서 적을 꺼내 스테이지에 소환.
  2. 적이 순차적으로 등장하도록 설정.

- invincible(): 플레이어를 일정시간 무적으로 만드는 메서드. *추가구현
  무적 시간이 남았을 경우: 
    1. 플레이어가 받는 데미지를 무효화.
    2. 플레이어와 충돌하는 적을 즉시 파괴.
    3. 플레이어 sprite의 색깔을 무지개빛으로 바꿈.

- damage_effect(): 플래이어가 데미지를 입을 때마다 붉은 화면으로 알림.
  플레이어가 데미지를 입었을 시 일정 시간동안 화면을 붉게 채움.


## enemy.py
### 클래스 Enemy
설명: 게임 내 적 캐릭터의 기본 클래스로, 공통적인 속성과 메서드를 정의.
- update(): 적의 상태를 업데이트하는 메서드.
- draw(screen): 적을 화면에 그리는 메서드.
- take_damage(damage): 적이 피해를 입었을 때 체력을 감소시키는 메서드.
- destroy(): 적을 파괴하는 메서드.
- check_collision(other): 다른 객체와의 충돌을 확인하는 메서드.

### 클래스 Chaser, Shooter, Spreader
설명: Enemy 클래스를 상속받아 특정한 행동을 하는 적 클래스.
- update(): 적의 종류에 맞게 적의 상태를 업데이트하는 메서드.
- draw(screen): 적의 종류에 맞게 적을 화면에 그리는 메서드.

## menu.py *추가구현
### 클래스 Menu
설명: 게임 메뉴 클래스로, 게임 시작과 종료 시 재도전, 게임 종료의 옵션을 수행.
- draw(): 메뉴 화면을 출력하는 메서드. start, quit의 두 가지 옵션을 제공.
- handle_event(): 키보드 입력을 통해 start, quit의 옵션을 받아 수행.
