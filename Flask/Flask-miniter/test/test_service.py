import jwt
import bcrypt
import pytest
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from model import UserDao, TweetDao
from service import UserService, TweetService
from sqlalchemy import create_engine, text
from unittest import mock

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)

@pytest.fixture
def user_service():
    mock_s3_client = mock.Mock()
    return UserService(UserDao(database), config.test_config, mock_s3_client)

@pytest.fixture
def tweet_service():
    return TweetService(TweetDao(database))

# test ���� �� 
def setup_function():
    # create test user
    hashed_password = bcrypt.hashpw(
        b'1234',
        bcrypt.gensalt()
    )
    new_users = [
        {
            'id'              : 1,
            'name'            : 'first',
            'email'           : 'test@test.com',
            'profile'         : 'first profile',
            'hashed_password' : hashed_password
        }, {
            'id'              : 2,
            'name'            : 'user',
            'email'           : 'user@test.com',
            'profile'         : 'second profile',
            'hashed_password' : hashed_password
        }
    ]
    database.execute(text("""
        INSERT INTO users (
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """), new_users)

    # user2�� ���� tweet �̸� ����
    database.execute(text("""
                        INSERT INTO tweets (
                            user_id,
                            tweet
                        ) VALUES (
                            2,
                            "user2 test tweet"
                        )"""
                    ))

# test ���� �� 
def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))

# ����� ���� Ȯ��
def get_user(user_id):
    row = database.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id' : user_id 
    }).fetchone()

    return {
        'id' : row['id'],
        'name' : row['name'],
        'email' : row['email'],
        'profile' : row['profile']
    } if row else None

# �ȷο� ����Ʈ Ȯ��
def get_follow_list(user_id):
    rows = database.execute(text("""
        SELECT follow_user_id as id
        FROM users_follow_list
        WHERE user_id = :user_id
    """), {
        'user_id' : user_id
    }).fetchall()

    return [row['id'] for row in rows]

# ȸ������
def test_create_new_user(user_service):
    new_user = {
        'name' : 'new',
        'email' : 'new@test.com',
        'profile' : 'create new user test',
        'password' : '1234'
    }

    new_user_id = user_service.create_new_user(new_user)
    created_user = get_user(new_user_id)

    assert created_user == {
        'id' : new_user_id,
        'name' : new_user['name'],
        'profile' : new_user['profile'],
        'email' : new_user['email']
    }

# �α���
def test_login(user_service):
    # �̹� �ִ� ������ �׽�Ʈ
    assert user_service.login({
        'email' : 'test@test.com',
        'password' : '1234'
    })
    # �߸��� ��й�ȣ �׽�Ʈ
    assert not user_service.login({
        'email' : 'test@test.com',
        'password' : 'abcd'
    })

# ��ū ���� �� decode�� ������ ���� ���̵����� Ȯ��
def test_generate_access_token(user_service):
    token   = user_service.generate_access_token(1)
    payload = jwt.decode(token, config.JWT_SECRET_KEY, 'HS256')

    assert payload['user_id'] == 1

# follow
def test_follow(user_service):
    user_service.follow(1, 2)
    follow_list = get_follow_list(1)

    assert follow_list == [2]

# unfollow
def test_unfollow(user_service):
    user_service.follow(1, 2)
    user_service.unfollow(1, 2)
    follow_list = get_follow_list(1)

    assert follow_list == []

# tweet
def test_tweet(tweet_service):
    tweet_service.tweet(1, 'tweet test')
    timeline = tweet_service.get_timeline(1)

    assert timeline == [
        {
            'user_id' : 1,
            'tweet' : 'tweet test'
        }
    ]

# timeline
def test_timeline(user_service, tweet_service):
    tweet_service.tweet(1, 'first tweet test')
    tweet_service.tweet(2, 'second tweet test')
    user_service.follow(1, 2)

    timeline = tweet_service.get_timeline(1)

    assert timeline == [
        {
            'user_id' : 2,
            'tweet' : 'user2 test tweet'
        },
        {
            'user_id' : 1,
            'tweet'   : 'first tweet test'
        }, 
        {
            'user_id' : 2,
            'tweet'   : 'second tweet test'
        }        
    ]