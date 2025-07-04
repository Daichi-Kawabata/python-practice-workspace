# ORM比較メモ: SQLAlchemy vs ActiveRecord (Ruby) vs GORM (Go)

## 概要

このメモでは、Python の SQLAlchemy、Ruby の ActiveRecord、Go の GORM の主要な違いと特徴を比較します。

## 基本的なモデル定義

### SQLAlchemy (Python)
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    author: Mapped["User"] = relationship("User", back_populates="posts")
```

### ActiveRecord (Ruby)
```ruby
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
  
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true
end

class Post < ApplicationRecord
  belongs_to :author, class_name: 'User'
  
  validates :title, presence: true
  validates :content, presence: true
end
```

### GORM (Go)
```go
type User struct {
    ID    uint   `gorm:"primaryKey"`
    Name  string `gorm:"size:100;not null"`
    Email string `gorm:"size:100;uniqueIndex;not null"`
    Posts []Post `gorm:"foreignKey:AuthorID"`
}

type Post struct {
    ID       uint   `gorm:"primaryKey"`
    Title    string `gorm:"size:200;not null"`
    Content  string `gorm:"type:text;not null"`
    AuthorID uint
    Author   User `gorm:"foreignKey:AuthorID"`
}
```

## CRUD操作の比較

### Create（作成）

#### SQLAlchemy
```python
# セッション管理が必要
with get_db_session() as session:
    user = User(name="John", email="john@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
```

#### ActiveRecord
```ruby
# シンプルで直感的
user = User.create(name: "John", email: "john@example.com")
# または
user = User.new(name: "John", email: "john@example.com")
user.save
```

#### GORM
```go
// 構造体ベース
user := User{Name: "John", Email: "john@example.com"}
result := db.Create(&user)
```

### Read（読み取り）

#### SQLAlchemy
```python
# IDで検索
user = session.get(User, 1)

# 条件検索
users = session.query(User).filter(User.name == "John").all()

# 関連データを含む検索（eager loading）
users = session.query(User).options(joinedload(User.posts)).all()
```

#### ActiveRecord
```ruby
# IDで検索
user = User.find(1)

# 条件検索
users = User.where(name: "John")

# 関連データを含む検索
users = User.includes(:posts)
```

#### GORM
```go
// IDで検索
var user User
db.First(&user, 1)

// 条件検索
var users []User
db.Where("name = ?", "John").Find(&users)

// 関連データを含む検索
db.Preload("Posts").Find(&users)
```

### Update（更新）

#### SQLAlchemy
```python
user = session.get(User, 1)
user.name = "Jane"
session.commit()
```

#### ActiveRecord
```ruby
user = User.find(1)
user.update(name: "Jane")
# または
user.name = "Jane"
user.save
```

#### GORM
```go
var user User
db.First(&user, 1)
db.Model(&user).Update("name", "Jane")
```

### Delete（削除）

#### SQLAlchemy
```python
user = session.get(User, 1)
session.delete(user)
session.commit()
```

#### ActiveRecord
```ruby
user = User.find(1)
user.destroy
# または
User.destroy(1)
```

#### GORM
```go
var user User
db.Delete(&user, 1)
```

## 主要な特徴比較

| 特徴 | SQLAlchemy | ActiveRecord | GORM |
|------|------------|--------------|------|
| **言語** | Python | Ruby | Go |
| **設計思想** | Data Mapper | Active Record | Code First |
| **学習コストの低さ** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **柔軟性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **型安全性** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **パフォーマンス** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **セッション管理** | 明示的 | 自動 | 明示的 |
| **マイグレーション** | Alembic | Built-in | Auto Migrate |

## マイグレーション

### SQLAlchemy + Alembic
```bash
# マイグレーション作成
alembic revision --autogenerate -m "Add users table"

# マイグレーション実行
alembic upgrade head
```

### ActiveRecord
```bash
# マイグレーション作成
rails generate migration CreateUsers name:string email:string

# マイグレーション実行
rails db:migrate
```

### GORM
```go
// 自動マイグレーション
db.AutoMigrate(&User{}, &Post{})
```

## リレーション定義

### 1対多 (One-to-Many)

#### SQLAlchemy
```python
class User(Base):
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

class Post(Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
```

#### ActiveRecord
```ruby
class User < ApplicationRecord
  has_many :posts
end

class Post < ApplicationRecord
  belongs_to :user
end
```

#### GORM
```go
type User struct {
    Posts []Post `gorm:"foreignKey:UserID"`
}

type Post struct {
    UserID uint
    User   User
}
```

### 多対多 (Many-to-Many)

#### SQLAlchemy
```python
# 中間テーブル定義
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Post(Base):
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=post_tags)
```

#### ActiveRecord
```ruby
class Post < ApplicationRecord
  has_and_belongs_to_many :tags
end

class Tag < ApplicationRecord
  has_and_belongs_to_many :posts
end
```

#### GORM
```go
type Post struct {
    Tags []Tag `gorm:"many2many:post_tags;"`
}

type Tag struct {
    Posts []Post `gorm:"many2many:post_tags;"`
}
```

## 複雑なクエリ

### SQLAlchemy
```python
# サブクエリ
subquery = session.query(Post.author_id).filter(Post.is_published == True).subquery()
authors = session.query(User).filter(User.id.in_(subquery)).all()

# JOIN
results = session.query(User, Post).join(Post).filter(Post.is_published == True).all()

# 生SQL
results = session.execute("SELECT * FROM users WHERE created_at > :date", {"date": date})
```

### ActiveRecord
```ruby
# サブクエリ
authors = User.where(id: Post.where(published: true).select(:author_id))

# JOIN
results = User.joins(:posts).where(posts: { published: true })

# 生SQL
results = User.find_by_sql("SELECT * FROM users WHERE created_at > ?", [date])
```

### GORM
```go
// サブクエリ
var authors []User
db.Where("id IN (?)", db.Model(&Post{}).Select("author_id").Where("published = ?", true)).Find(&authors)

// JOIN
var results []User
db.Joins("JOIN posts ON posts.author_id = users.id").Where("posts.published = ?", true).Find(&results)

// 生SQL
var results []User
db.Raw("SELECT * FROM users WHERE created_at > ?", date).Scan(&results)
```

## 長所と短所

### SQLAlchemy
**長所:**
- 非常に柔軟で強力
- データベース操作を細かく制御可能
- 複雑なクエリに対応
- Pythonの型ヒントとの相性が良い

**短所:**
- 学習コストが高い
- セッション管理が複雑
- ボイラープレートコードが多い

### ActiveRecord
**長所:**
- 非常にシンプルで直感的
- 規約による設定（Convention over Configuration）
- 豊富なヘルパーメソッド
- 学習コストが低い

**短所:**
- 複雑なクエリが書きにくい
- パフォーマンスの最適化が困難
- マジックメソッドによる暗黙的な動作

### GORM
**長所:**
- 型安全性が高い
- パフォーマンスが良い
- シンプルなAPI
- 自動マイグレーション

**短所:**
- 機能がやや限定的
- 複雑なリレーションが扱いにくい
- ドキュメントがやや不足

## 選択指針

### SQLAlchemy を選ぶべき場合
- 複雑なデータベース操作が必要
- パフォーマンスの最適化が重要
- 既存のPythonアプリケーションとの統合
- 型安全性を重視

### ActiveRecord を選ぶべき場合
- 開発速度を重視
- シンプルなCRUD操作が中心
- Railsエコシステムを活用
- 学習コストを抑えたい

### GORM を選ぶべき場合
- 高いパフォーマンスが必要
- 型安全性を最重視
- マイクロサービス構成
- Goの並行処理との連携

## 学習リソース

### SQLAlchemy
- [公式ドキュメント](https://docs.sqlalchemy.org/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

### ActiveRecord
- [Rails Guides - Active Record](https://guides.rubyonrails.org/active_record_basics.html)
- [ActiveRecord API Documentation](https://api.rubyonrails.org/classes/ActiveRecord/Base.html)

### GORM
- [GORM公式サイト](https://gorm.io/)
- [GORM Guide](https://gorm.io/docs/)

## まとめ

それぞれのORMには特徴があり、プロジェクトの要件に応じて適切に選択することが重要です：

- **SQLAlchemy**: 最も柔軟で強力だが、学習コストが高い
- **ActiveRecord**: 最もシンプルで直感的だが、複雑な操作には限界がある
- **GORM**: 型安全性とパフォーマンスのバランスが良い

Pythonでの開発では、SQLAlchemyの強力さを活かしつつ、適切な抽象化レイヤーを設けることで、開発効率とメンテナンス性の両立を図ることができます。
