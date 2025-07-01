"""
Pythonクラス定義・オブジェクト指向学習
Ruby/Golangとの比較を含む実践的な例
継承、多重継承、プロパティ、クラスメソッド、静的メソッドなど
"""

from typing import Optional, List, ClassVar, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

# =============================================================================
# 1. 基本的なクラス定義
# =============================================================================

class Person:
    """
    基本的なクラス定義
    Ruby: class Person
    Go: type Person struct
    """
    
    # クラス変数（全インスタンスで共有）
    species: ClassVar[str] = "Homo sapiens"
    total_count: ClassVar[int] = 0
    
    def __init__(self, name: str, age: int, email: Optional[str] = None) -> None:
        """
        コンストラクタ
        Ruby: def initialize(name, age, email = nil)
        Go: func NewPerson(name string, age int, email *string) *Person
        """
        self.name = name        # パブリック属性
        self.age = age
        self.email = email
        self._id = self._generate_id()  # プライベート風属性（慣例）
        
        # クラス変数をインクリメント
        Person.total_count += 1
    
    def _generate_id(self) -> str:
        """
        プライベートメソッド（慣例：アンダースコア開始）
        Ruby: private def generate_id
        Go: 小文字開始でpackage private
        """
        import uuid
        return str(uuid.uuid4())[:8]
    
    def introduce(self) -> str:
        """
        インスタンスメソッド
        Ruby: def introduce
        Go: func (p *Person) Introduce() string
        """
        return f"Hello, I'm {self.name}, {self.age} years old."
    
    def update_email(self, email: str) -> None:
        """メールアドレス更新"""
        self.email = email
    
    def __str__(self) -> str:
        """文字列表現（ユーザー向け）"""
        return f"{self.name} ({self.age})"
    
    def __repr__(self) -> str:
        """文字列表現（開発者向け）"""
        return f"Person(name='{self.name}', age={self.age}, email='{self.email}')"
    
    @classmethod
    def get_total_count(cls) -> int:
        """
        クラスメソッド
        Ruby: def self.get_total_count
        Go: 関数として定義
        """
        return cls.total_count
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """
        静的メソッド
        Ruby: def self.validate_age
        Go: 通常の関数
        """
        return 0 <= age <= 150

# =============================================================================
# 2. プロパティ（ゲッター・セッター）
# =============================================================================

class BankAccount:
    """
    プロパティを使用したクラス
    Ruby: attr_accessor, attr_reader などと類似
    Go: ゲッター・セッターメソッドを手動実装
    """
    
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = initial_balance  # プライベート風
        self._transactions: List[str] = []
    
    @property
    def balance(self) -> float:
        """
        ゲッター
        Ruby: def balance; @balance; end
        Go: func (b *BankAccount) Balance() float64
        """
        return self._balance
    
    @balance.setter
    def balance(self, amount: float) -> None:
        """
        セッター
        Ruby: def balance=(amount); @balance = amount; end
        Go: func (b *BankAccount) SetBalance(amount float64)
        """
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount
    
    @property
    def transactions(self) -> List[str]:
        """読み取り専用プロパティ"""
        return self._transactions.copy()  # コピーを返してカプセル化を保つ
    
    def deposit(self, amount: float) -> None:
        """入金"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append(f"Deposit: +${amount}")
    
    def withdraw(self, amount: float) -> bool:
        """出金"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance >= amount:
            self._balance -= amount
            self._transactions.append(f"Withdrawal: -${amount}")
            return True
        return False

# =============================================================================
# 3. 継承（単一継承）
# =============================================================================

class Employee(Person):
    """
    Personクラスを継承
    Ruby: class Employee < Person
    Go: 埋め込み（embedding）を使用
    """
    
    def __init__(self, name: str, age: int, employee_id: str, 
                 department: str, salary: float, email: Optional[str] = None) -> None:
        """
        親クラスのコンストラクタを呼び出し
        Ruby: super(name, age, email)
        Go: 埋め込み構造体の初期化
        """
        super().__init__(name, age, email)  # 親クラスの初期化
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
    
    def introduce(self) -> str:
        """
        メソッドのオーバーライド
        Ruby: def introduce (自動的にオーバーライド)
        Go: 同名メソッドで隠蔽
        """
        base_intro = super().introduce()  # 親クラスのメソッド呼び出し
        return f"{base_intro} I work in {self.department} department."
    
    def give_raise(self, amount: float) -> None:
        """従業員固有のメソッド"""
        self.salary += amount
    
    def __repr__(self) -> str:
        return f"Employee(name='{self.name}', age={self.age}, id='{self.employee_id}', dept='{self.department}')"

class Manager(Employee):
    """
    Employeeクラスをさらに継承
    Ruby: class Manager < Employee
    """
    
    def __init__(self, name: str, age: int, employee_id: str, 
                 department: str, salary: float, team_size: int, 
                 email: Optional[str] = None) -> None:
        super().__init__(name, age, employee_id, department, salary, email)
        self.team_size = team_size
        self.reports: List[Employee] = []
    
    def add_report(self, employee: Employee) -> None:
        """部下を追加"""
        self.reports.append(employee)
    
    def introduce(self) -> str:
        base_intro = super().introduce()
        return f"{base_intro} I manage a team of {self.team_size} people."

# =============================================================================
# 4. 多重継承（Multiple Inheritance）
# =============================================================================

class Flyable(ABC):
    """
    抽象基底クラス（インターフェース風）
    Ruby: module Flyable
    Go: type Flyable interface
    """
    
    @abstractmethod
    def fly(self) -> str:
        """飛ぶ動作（抽象メソッド）"""
        pass
    
    @abstractmethod
    def land(self) -> str:
        """着陸動作（抽象メソッド）"""
        pass

class Swimmable(ABC):
    """
    泳げる能力の抽象クラス
    """
    
    @abstractmethod
    def swim(self) -> str:
        pass

class Animal:
    """動物の基底クラス"""
    
    def __init__(self, name: str, species: str) -> None:
        self.name = name
        self.species = species
    
    def eat(self) -> str:
        return f"{self.name} is eating."
    
    def sleep(self) -> str:
        return f"{self.name} is sleeping."

class Bird(Animal, Flyable):
    """
    鳥クラス（多重継承）
    Animal + Flyable を継承
    Ruby: class Bird < Animal; include Flyable; end
    Go: 埋め込みで実現
    """
    
    def __init__(self, name: str, wing_span: float) -> None:
        super().__init__(name, "Bird")
        self.wing_span = wing_span
    
    def fly(self) -> str:
        return f"{self.name} is flying with {self.wing_span}cm wings."
    
    def land(self) -> str:
        return f"{self.name} has landed safely."

class Duck(Animal, Flyable, Swimmable):
    """
    アヒルクラス（3つのクラス/インターフェースを継承）
    """
    
    def __init__(self, name: str) -> None:
        super().__init__(name, "Duck")
    
    def fly(self) -> str:
        return f"{self.name} the duck is flying (not very gracefully)."
    
    def land(self) -> str:
        return f"{self.name} the duck has landed on water."
    
    def swim(self) -> str:
        return f"{self.name} is swimming gracefully on the water."
    
    def quack(self) -> str:
        return f"{self.name} says: Quack!"

# =============================================================================
# 5. メソッドレゾリューション順序（MRO）
# =============================================================================

class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return "B"

class C(A):
    def method(self) -> str:
        return "C"

class D(B, C):
    """
    多重継承でのMRO（Method Resolution Order）
    Python: D -> B -> C -> A -> object
    """
    pass

# MROを確認: D.mro() または D.__mro__

# =============================================================================
# 6. プロトコル（Protocol）- 構造的サブタイピング
# =============================================================================

class Drawable(Protocol):
    """
    プロトコル（Go のインターフェースに近い）
    """
    def draw(self) -> str: ...

class Circle:
    """Drawableプロトコルを満たす（明示的継承なし）"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> str:
        return f"Drawing a circle with radius {self.radius}"

class Square:
    """Drawableプロトコルを満たす"""
    
    def __init__(self, side: float) -> None:
        self.side = side
    
    def draw(self) -> str:
        return f"Drawing a square with side {self.side}"

def render_shape(shape: Drawable) -> str:
    """
    Drawableプロトコルを満たすオブジェクトを受け取る
    Go のインターフェースのような使い方
    """
    return shape.draw()

# =============================================================================
# 7. dataclass と継承
# =============================================================================

@dataclass
class Point:
    x: float
    y: float

@dataclass
class ColoredPoint(Point):
    color: str = "black"

@dataclass
class Point3D(Point):
    z: float = 0.0

# =============================================================================
# 8. 実践例：ゲームキャラクター設計
# =============================================================================

class Character(ABC):
    """ゲームキャラクターの抽象基底クラス"""
    
    def __init__(self, name: str, health: int, attack_power: int) -> None:
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.level = 1
    
    @abstractmethod
    def special_attack(self) -> str:
        """特殊攻撃（各キャラクターで実装）"""
        pass
    
    def attack(self, target: 'Character') -> str:
        """通常攻撃"""
        target.health -= self.attack_power
        return f"{self.name} attacks {target.name} for {self.attack_power} damage!"
    
    def heal(self, amount: int) -> None:
        """回復"""
        self.health = min(self.health + amount, self.max_health)

class Warrior(Character):
    """戦士クラス"""
    
    def __init__(self, name: str) -> None:
        super().__init__(name, health=120, attack_power=15)
        self.armor = 10
    
    def special_attack(self) -> str:
        return f"{self.name} performs a mighty sword slash!"

class Mage(Character):
    """魔法使いクラス"""
    
    def __init__(self, name: str) -> None:
        super().__init__(name, health=80, attack_power=20)
        self.mana = 100
    
    def special_attack(self) -> str:
        if self.mana >= 20:
            self.mana -= 20
            return f"{self.name} casts a powerful fireball!"
        return f"{self.name} doesn't have enough mana!"

# =============================================================================
# 使用例・テスト
# =============================================================================

if __name__ == "__main__":
    print("=== 基本クラス ===")
    person1 = Person("Alice", 25, "alice@example.com")
    person2 = Person("Bob", 30)
    
    print(person1.introduce())
    print(f"Total people: {Person.get_total_count()}")
    print(f"Species: {Person.species}")
    print(f"Age validation: {Person.validate_age(25)}")
    
    print("\n=== プロパティ ===")
    account = BankAccount("John Doe", 1000.0)
    print(f"Initial balance: ${account.balance}")
    
    account.deposit(500.0)
    print(f"After deposit: ${account.balance}")
    
    account.withdraw(200.0)
    print(f"After withdrawal: ${account.balance}")
    print(f"Transactions: {account.transactions}")
    
    print("\n=== 継承 ===")
    employee = Employee("Carol", 28, "EMP001", "Engineering", 75000.0)
    manager = Manager("Dave", 35, "MGR001", "Engineering", 95000.0, 5)
    
    print(employee.introduce())
    print(manager.introduce())
    
    manager.add_report(employee)
    print(f"Manager reports: {len(manager.reports)}")
    
    print("\n=== 多重継承 ===")
    bird = Bird("Eagle", 200.0)
    duck = Duck("Donald")
    
    print(bird.fly())
    print(bird.land())
    print(bird.eat())
    
    print(duck.fly())
    print(duck.swim())
    print(duck.quack())
    
    print("\n=== MRO ===")
    d = D()
    print(f"D().method(): {d.method()}")  # "B"
    print(f"MRO: {[cls.__name__ for cls in D.mro()]}")
    
    print("\n=== プロトコル ===")
    circle = Circle(5.0)
    square = Square(4.0)
    
    shapes = [circle, square]
    for shape in shapes:
        print(render_shape(shape))
    
    print("\n=== dataclass 継承 ===")
    point = Point(1.0, 2.0)
    colored_point = ColoredPoint(3.0, 4.0, "red")
    point_3d = Point3D(5.0, 6.0, 7.0)
    
    print(f"Point: {point}")
    print(f"Colored Point: {colored_point}")
    print(f"3D Point: {point_3d}")
    
    print("\n=== ゲームキャラクター ===")
    warrior = Warrior("Conan")
    mage = Mage("Gandalf")
    
    print(f"Warrior: {warrior.name}, HP: {warrior.health}")
    print(f"Mage: {mage.name}, HP: {mage.health}, Mana: {mage.mana}")
    
    print(warrior.attack(mage))
    print(f"Mage HP after attack: {mage.health}")
    
    print(warrior.special_attack())
    print(mage.special_attack())
