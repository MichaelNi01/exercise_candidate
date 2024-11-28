# API Testing - Dog API

This project aims to test the functionality of an API that manages dog operations. Automated tests are designed to ensure that the creation, viewing, and deletion of dogs work correctly. The framework used for the tests is `pytest`.

## Fixtures

### `start_container` Fixture

This fixture is used to start a container of the API before executing the tests and to stop it after all tests have finished. The container is started using an image called `exercise:1.0`, which runs on port 5000. 

At the end of the test execution, the fixture ensures that the container is stopped and removed automatically, ensuring that the test environment is cleaned up properly. 

Note: It is important to note that this fixture is configured to work with **Podman** by default, but if **Docker** is preferred, the word "podman" can simply be replaced with "docker" in the fixture code. 

### `create_dog` Fixture

This fixture is responsible for creating a dog in the API. It makes a `POST` request with a payload containing the dog’s breed, age, and name. The API response includes a unique `id` that identifies the newly created dog. This `id` is then used by other test cases to interact with the dog, such as retrieving its information or deleting it.

At the end of the test execution, the `create_dog` fixture also ensures that the created dog is deleted by making a `DELETE` request with the dog’s `ID`

## Test Cases

The test cases are designed to cover the main operations of the API:

- **`create_dog`**: This test case creates a dog with valid data and checks that the API returns a successful response and that the response includes an `dog_id`, indicating that the dog has been created correctly. After the test, the created dog is automatically deleted using the fixture.

- **`create_invalid_dog`**: This test case attempts to create a dog with an invalid payload (e.g., missing or incorrect data) and verifies that the API returns a status code of 400 or 422, indicating that the request is invalid.

- **`view_valid_dog`**: In this case, it is verified that a dog created previously can be viewed correctly. The `dog_id` of the dog that was obtained when the dog was created is used, and a `GET` request is made to retrieve its information. A successful response with a status code of 200 is expected.

- **`delete_valid_dog`**: This test case deletes a dog using its `dog_id`. After making the `DELETE` request, it verifies that the response is successful with a status code of 204, indicating that the dog has been deleted correctly.

- **`delete_invalid_dog`**: Here, an attempt is made to delete a dog with a non-existent `dog_id`, which should result in a status code of 404. This ensures that the API correctly handles errors when trying to delete a non-existent resource.

## How to Run the Tests

To run the automated tests, users need to follow some basic steps. First, they must install the required dependencies, such as `pytest` and `requests`. Then, the API container must be running, which is ensured by the `start_container` fixture. If Docker is being used, it is important to verify that Docker is properly installed and running on the system. Finally, the tests can be executed using the `pytest` command: pytest test_dogs_api.py

## Requirements

- **Docker or Podman**: One of these tools is required to start the API container.
- **Python 3.x**: The tests run in a Python environment.
- **pytest**: The framework used for automated testing.