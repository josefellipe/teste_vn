import pytest
from src.service.user import UserService
from src.schema.user import UserCreateSchema, FriendRequestSchema


@pytest.fixture
def service():
    return UserService()


@pytest.fixture
def create_user(service, db):
    def _create_user(name, username):
        return service.create_user(db, UserCreateSchema(name=name, username=username))
    return _create_user


def test_create_user(service, db):
    data = UserCreateSchema(name="John", username="john123")
    result = service.create_user(db, data)
    
    assert result.username == "john123"


def test_get_user(service, create_user, db):
    create_user("John", "john123")
    
    result = service.get_user(db, "john123")
    
    assert result.username == "john123"


def test_add_friend(service, create_user, db):
    user1 = create_user("John", "john123")
    user2 = create_user("Mary", "mary456")
    
    data = FriendRequestSchema(user_id=user1.id, friend_id=user2.id)
    result = service.add_friend(db, data)
    
    assert result == True


def test_get_friends(service, create_user, db):
    user1 = create_user("John", "john123")
    user2 = create_user("Mary", "mary456")
    user3 = create_user("Bob", "bob789")
    
    service.add_friend(db, FriendRequestSchema(user_id=user1.id, friend_id=user2.id))
    service.add_friend(db, FriendRequestSchema(user_id=user1.id, friend_id=user3.id))
    
    result = service.get_friends(db, user_id=user1.id, limit=10, offset=0)
    
    assert len(result) == 2


def test_render_feed_with_friendships(service, create_user, db):
    user1 = create_user("John", "john")
    user2 = create_user("Mary", "mary")
    
    service.add_friend(db, FriendRequestSchema(user_id=user1.id, friend_id=user2.id))
    
    result = service.render_feed(db, user1.id)
    
    assert len(result) == 1
    assert "John and Mary are now friends" in result[0]
