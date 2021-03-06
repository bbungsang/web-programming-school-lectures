# 도커(Docker)
#### 리눅스 컨테이너 기반의 오픈소스 가상화 플랫폼

## 컨테이너
- 일반적으로 알고 있는 컨테이너와 같이 다양한 프로그램 및 실행 환경을 **컨테이너** 로 `추상화`하고, 각각 **동일한 인터페이스** 를 제공하여 프로그램의 배포 및 관리를 단순하게 해준다.
- **격리된 공간** 에서 프로세스가 동작하는 `가상화` 기술 

![docker container](./images/docker-works.png) 

#### [기존 가상화 기술]
- **OS** 를 가상화, VMware, VirtualBoxa 등
- *전가상화(Full Virtualization)* : 호스트 OS 위에 게스트 OS 전체를 가상화하여 사용하는 방식, 무겁고 느리다.

#### [클라우드 서비스 가상화 기술]
- **CPU** 를 가상화, KVM, Xen 등
- *반가상화(Paravirtualization)* : 게스트 OS가 필요하지만 전체 OS를 가상화하는 방식은 아니다.

> 하지만 전가상화, 반가상화 모두 추가적인 OS를 설치하여 가상화하는 방법이기 때문에 성능적인 문제가 발생한다. ➜ **프로세스 격리** 방식 등장!

#### [도커 가상화 기술]
- **프로세스 격리**, CPU나 메모리는 딱 프로세스가 필요한 만큼만 추가로 사용하고 성능적으로 거의 손실이 없다.
- 서버 하나에 여러 개의 컨테이너를 실행할 경우, 서로 영향을 미치지 않고 독립적으로 실행되어 굉장히 가벼운 가상머신을 사용하는 듯한 느낌을 준다.
- 새로운 컨테이너를 만드는 데 걸리는 시간은 거의 1~2초 가량, 실행 중인 컨테이너에 접속하여 'apt-get' 또는 'yum' 으로 패키지를 설치할 수 있으며, 사용자 추가 및 여러 개의 프로세스를 백그라운드로 실행 가능하다.

## 이미지
- 컨테이너 실행에 필요한 파일과 설정 값 등을 포함하고 있는 것으로 상태값을 가지지 않으며 변하지 않는다.
- `컨테이너 = 이미지를 실행한 상태`, 같은 이미지에서 여러 개의 컨테이너를 생성할 수 있고, 컨테이너의 상태가 바뀌거나 삭제되더라도 이미지는 변하지 않고 그대로 남아있다.
- 이미지는 컨테이너를 실행하기 위한 모든 정보를 가지고 있기 때문에 컴파일 및 여러 패키지 설치가 필요없다.
- 서버가 추가되더라도 만들어 놓은 이미지를 다운받고 컨테이너를 생성만하면 된다.
- 이미지는 'Docker hub'에 등록하거나 'Docker Registry 저장소'를 직접 만들어 관리할 수 있다.

> 물리적으로 서버를 줄이면 해당 서버의 데이터가 통째로 날아갈 수도 있기 때문에 서버 개수와 데이터를 저장하는 공간을 별도로 해야한다.  

### 레이어 저장 방식
- 이미지는 컨테이너 실행을 위한 모든 정보를 가지고 있어서 용량이 엄청나다. 
- 하지만 처음 이미지를 다운 받을 때에만 크게 부담이 작용할 뿐, **레이어(Layer)** 라는 개념을 사용함으로써 **파일 추가/수정** 시,  **새로운 레이어만 다운** 받고 이후의 레이어가 이전 레이어를 **참조** 하는 형태로 작용하기 때문에 굉장히 효율적으로 이미지 관리가 가능하다.
- 이미지는 **URL 방식**으로 관리되며 **태그**를 붙일 수 있다. 
- 태그 기능을 잘 이용하면 테스트나 롤백도 쉽게 할 수 있다.

> 배포용 컨테이너의 경우, 이미지는 로컬에서 다 만들어서 넘겨주기  때문에 zsh, git 등과 같은 패키지가 필요하지 않다.

### 이미지 생성
- 도커는 이미지를 만들기 위해 `Dockerfile`이라는 파일 자체 **DSL(Domain-Specific-Language)** 를 이용하여 이미지 생성 과정을 적는다.
- 서버에 어떤 프로그램을 설치하기 위해 메모장에 따로 적어두고 각각 실행할 필요가 없다. `Dockerfile`에 전부 기입하고 그 자체로 관리하면 된다. 
- 해당 파일은 소스와 함께 버전 관리가 가능하며 원하면 누구나 이미지 생성 과정을 보고 수정할 수 있다.

> 로컬에서 도커로 서비스가 작동되면, 서버에서도 동일하게 작동한다.

[도커 명령어]

```
>>> docker run ubuntu:16.04 # 이미지 생성
>>> docker run --rm -it ubuntu:16.04 /bin/bash # 생성한 이미지 실행
>>> docker ps
>>> docker cp . <image-name>:/srv/used-book-store
>>> docker stop <imgae-name>
>>> docker run --rm -it updated_ubuntu /bin/zsh 
>>> docker build -t updated ubuntu . # Dockerfile 명령어가 순차적으로 실행, 그 결과가 >>> updated_ubuntu 라는 이미지로 형성
>>> docker run --rm -it updated_ubuntu /bin/bash
```

![](./images/docker-logo.png) 

> 최근 도커 사용 경향 (≧ω≦)ゞ <br>
- 서버 1개가 받아들이는 용량은 한정되어있다. 따라서 호스트 안 쪽에서 여러 컨테이너가 작동될 수 있지만, 최근 컨테이너 하나만 작동시키는 경향을 따르고 있다. 즉, **서버 1개에 1개의 프로세서**가 작동시키는 방식이 대세이다. <br>
- 클라이언트로부터 장고가 받는 요청, 장고가 백엔드 처리하는 것, 백엔드를 데이터베이스에 요청 처리하는 것 등 각각의 부하가 다른다. 도커는 이에 따라서 자동으로 스케일링이 되도록한다. <br>
- 스케일링이란? 서버 1개가 받아들이는 용량은 한정, 클라이언트의 요청은 갑자기 늘기도 줄기도 한다. 요청이 늘어나면 물리적인 서버를 늘려야하고, 어느 순간 줄어들면 줄여야한다. 하지만 이 작업은 몹시 어려운 일이다. AWS, Azure 와 같은 클라우드가 늘리고 줄이는 일을 자동으로 처리해주기 때문에 일반 어플리케이션 개발자도 쉽게 서버 관리에 접근할 수 있다. 
