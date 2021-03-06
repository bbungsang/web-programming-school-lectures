## Relationships
- 관계형 데이터베이스의 강점은 서로 관련이 있는 테이블에 있다. 장고는 데이터베이스 관계를 정의할 수 있는 3가지 방법을 제공한다.

### Many-to-one relationships
- 이 방법을 설명하기 위해 **django.db.models.ForeignKey** 사용한다.
- 외래키는 클래스형 인자를 요구한다.
- 예를 들어, `Car` 모델이 `Manufacturer`(컬럼, 속성)를 포함한다면, Manufacturer은 다양한 브랜드와 여러 대의 자동차를 만들지만 하나의 Car객체는 하나의 Manufacturer를 가지게된다.

```python
from django.db import models

class Manufacturer(models.Model):
  pass

class Car(models.Model):
  manufacturer = models.ForeignKey(
    Manufacturer,
    on_delete=models.CASCADE
  )
```

<br>
### Many-to-many relationships
- 이 방법을 설명하기 위해 **ManyToManyField** 를 사용한다.
- **ManyToManyField** 는 클래스 인자를 요구한다.
- 예를 들어, Pizza(모델)가 여러 개의 Topping object 를 가지고 있다면, 한 가지의 Topping 이 여러 개의 피자에 쓰였을 수도 있고, 각각의 Pizza 가 여러 개의 Topping 을 가지고 있을 수 있다.

```python
from django.db import models

class Topping(models.Model):
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
```
- ManyToManyField는 오직 모델 하나에 대입시킬 수 있다.
- 일반적으로 ManyToManyField 인스턴스는 폼에서 수정될 예정인 대상으로 해야한다.
- 예를 들어 토핑이 여러 개의 피자에 있는 것보다 하나의 피자가 토핑들을 가지고 있는 것이 더욱 자연스럽기 때문에 토핑은 피자에 있는 것이다. 따라서 ManyToManyField를 Pizza 모델에 걸어서 사용자들이 토핑들을 선택하도록 한다.

<br>
### Extra fields on many-to-many relationships
- `musicians`에 속해있는 `musical groups`을 추적하는 어플리케이션의 경우, 그룹에 속해있는 멤버와 뮤지션들은 many-to-many 관계에 있을 것이다. 따라서 이 관계를 표현하기 위해 ManyToManyField를 사용해야하지만, 그룹에 속해있는 사람의 가입 날짜와 같은 수집하고자하는 그룹에 자세한 많은 사항이 있을 것이다.
- 이럴 때, 장고는 many-to-many를 다루는 것에 익숙해지도록 모델을 명세화할 것을 허용한다. 모델의 중간자 부분에 extra fields를 넣을 수 있는데, 이때 중간자 모델은 ManyToManyField를 건 필드에 through 인자를 사용함으로써 연관지어진다.

```python
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
      Person,
      through='Membership',
    )

    def __str__(self):
        return self.name

# intermediary model
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```
- 중간자 모델을 설정하려고 할 때, many-to-many relationship을 포함하고 있는 모델의 외래키를 분명하게 명기해야한다. 이 선언은 어떻게 두 모델이 관련되어 있는 지를 설명해준다.

```python
# Person 객체 생성
>>> heejin = Person.objects.create(name='김희진')

# Group 객체 생성
>>> ca = Group.objects.create(name='크아팸')

# Membership(중간자모델) 객체 생성
>>> m1 = Mebership(
...     person=heejin,
...     group=ca,
...     date_joined=date(2016, 01, 01),
...     invite_reason="새해 첫 날을 맞이하여 기념으로",
...   )
>>> m1.save()
>>> ca.members.all()
<QuerySet [<Person: 김희진>]>
>>> heejin.group_set.all()
<QuerySet [<Group: 크아팸>]>
```
- 위와 같이 추가로 Person의 sooyin, hwanga 객체를 더 생성했다고 가정해보자.

```python
>>> ca.members.add(sooyin)
>>> ca.members.create(name='김황아')
>>> ca.members.set([heejin, sooyin, hwanga])
```
- 하지만 Person과 Group 사이에 관계를 생성할 수 없다. 중간자 모델이 존재할 경우, Membership(중간자모델)을 통해 관계를 구체적으로 명세할 필요가 있다.

- <QuerySet [<Person: 김희진>, <Person: 모수인>, <Person: 김황아>]>일 경우,

```python
# remove()
>>> ca.members.remove(heejin)
>>> ca.members.all()
<QuerySet [<Person: 모수인>, <Person: 김황아>]>

# clear()
>>> ca.members.clear()
>>> ca.members.all()
<QuerySet []>
```
- 다시 <QuerySet [<Person: 김희진>, <Person: 모수인>, <Person: 김황아>]>일 경우,

```python
>>> Group.objects.filter(members__name__startswith='김희진')
<QuerySet [<Group: 크아팸>]>

>>> Person.objects.filter(
...   group__name='크아팸',
...   membership__date_joined__gt=date(2016,1,1))
<QuerySet [<Person: 김희진>]>
```
