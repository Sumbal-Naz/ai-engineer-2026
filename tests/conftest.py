# Import pytest so we can create pytest fixtures.
import pytest

# Import TestClient so our tests can send HTTP requests
# to the FastAPI application.
from fastapi.testclient import TestClient

# Import SQLAlchemy tools for creating our test database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the application's FastAPI app.
from src.app.api import app, get_current_user

# Import the SQLAlchemy Base class and database dependency.
from src.app.database import Base, get_db
from src.app.models import UserDB


# ---------------------------------------------------------
# TEST DATABASE
# ---------------------------------------------------------

# Use a completely separate SQLite database for testing.
#
# This prevents pytest from modifying our normal
# ai_engineer.db database.
TEST_DATABASE_URL = "sqlite:///./ai_engineer_test.db"


# Create a separate SQLAlchemy engine for the test database.
#
# check_same_thread=False is required because FastAPI's
# TestClient may interact with the database from different
# threads.
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# Create a session factory connected to the test database.
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# ---------------------------------------------------------
# DATABASE FIXTURE
# ---------------------------------------------------------

@pytest.fixture
def db_session():
    """
    Create a fresh database for each test.

    The tables are created before the test and removed
    after the test finishes.

    This gives each test database isolation.
    """

    # Create all tables defined by our SQLAlchemy models.
    Base.metadata.create_all(bind=test_engine)

    # Create a database session connected to the
    # test database.
    db = TestSessionLocal()

    try:
        # Give the database session to the test.
        yield db

    finally:
        # Close the database session after the test.
        db.close()

        # Remove all tables after the test.
        #
        # The next test will therefore start with
        # an empty database.
        Base.metadata.drop_all(bind=test_engine)


# ---------------------------------------------------------
# DATABASE DEPENDENCY OVERRIDE
# ---------------------------------------------------------

@pytest.fixture
def client(db_session):
    """
    Create a FastAPI TestClient that uses the test database.

    FastAPI normally uses get_db(), which connects to
    ai_engineer.db.

    We override get_db() so tests use our test database instead.
    """

    def override_get_db():
        """
        Return the test database session to FastAPI.
        """
        try:
            yield db_session
        finally:
            pass

    # Tell FastAPI:
    #
    # Whenever an endpoint asks for get_db(),
    # use override_get_db() instead.
    app.dependency_overrides[get_db] = override_get_db

    # Create a test client for making HTTP requests.
    test_client = TestClient(app)

    try:
        # Give the test client to the test.
        yield test_client

    finally:
        # Remove the dependency override after the test.
        #
        # This prevents one test's configuration from
        # affecting another test.
        app.dependency_overrides.clear()

@pytest.fixture
def auth_client(db_session):
    """
    Create a TestClient that is authenticated with a JWT token.

    This fixture:
    1. Creates a test user directly in the test database.
    2. Logs that user in through the real /login endpoint.
    3. Gets the JWT access token returned by the API.
    4. Adds the token to the TestClient.
    5. Returns the authenticated client to the test.
    """

    # Import the password hashing function used by our application.
    from src.app.auth import hash_password

    # Import the UserDB database model.
    from src.app.models import UserDB

    # Create a test user in the isolated test database.
    test_user = UserDB(
        username="testuser",
        password_hash=hash_password("TestPassword123"),
        is_active=True,
        role="user",
    )

    # Add the test user to the test database.
    db_session.add(test_user)

    # Save the test user.
    db_session.commit()

    # Refresh the object so SQLAlchemy loads its generated ID.
    db_session.refresh(test_user)

    # Create the FastAPI TestClient using our existing
    # database-isolated client fixture.
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)

    try:
        # Log in through the actual API.
        login_response = test_client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "TestPassword123",
            },
        )

        # Make sure the login itself worked.
        assert login_response.status_code == 200

        # Extract the JWT access token from the response.
        access_token = login_response.json()["access_token"]

        # Add the JWT to the client.
        test_client.headers.update(
            {
                "Authorization": f"Bearer {access_token}"
            }
        )

        # Return the authenticated client to the test.
        yield test_client

    finally:
        # Remove dependency overrides after the test.
        app.dependency_overrides.clear()

@pytest.fixture
def admin_client(client):
    """
    Provide a TestClient with authentication overridden
    as an admin user.
    """

    app.dependency_overrides[
        get_current_user
    ] = override_admin_user

    yield client

    app.dependency_overrides.clear()

def override_admin_user():
    """
    Return a fake authenticated admin user.
    """

    return UserDB(
        id=1,
        username="test_admin",
        password_hash="fake_hash",
        is_active=True,
        role="admin"
    )

def override_normal_user():
    """
    Return a fake authenticated normal user.
    """

    return UserDB(
        id=2,
        username="test_user",
        password_hash="fake_hash",
        is_active=True,
        role="user"
    )

@pytest.fixture
def normal_user_client(client):
    """
    Provide a TestClient with authentication overridden
    as a normal user.
    """

    app.dependency_overrides[
        get_current_user
    ] = override_normal_user

    yield client

    app.dependency_overrides.clear()