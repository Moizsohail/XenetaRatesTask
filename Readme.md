# README

## Running the Project

To run the project, execute the following command:

```
docker-compose up --build
```

## Testing the Project

To test the project, execute the following command:

```
docker-compose --project-name xeneta-test -f docker-compose-test.yml up --build
```

## DB Optimization

The following indexes have been added to optimize the database:

| Table Name | Column Name |
| ---------- | ----------- |
| regions    | parent_slug |
| ports      | parent_slug |
| prices     | day         |
| prices     | orig_code   |
| prices     | dest_code   |

## Project Structure

```
📦backend
┣ 📂src
┃ ┣ 📂accessors
┃ ┃ ┣ 📜__init__.py
┃ ┃ ┗ 📜accessors.py
┃ ┣ 📂shared
┃ ┃ ┣ 📜constants.py
┃ ┃ ┣ 📜specs.py
┃ ┃ ┗ 📜utils.py
┃ ┣ 📂tests
┃ ┃ ┣ 📜__init__.py
┃ ┃ ┣ 📜conftest.py
┃ ┃ ┗ 📜handler_test.py
┃ ┣ 📜application.py
┃ ┣ 📜logs.log
┃ ┣ 📜services.py
┃ ┗ 📜validators.py
┣ 📜Dockerfile
┣ 📜pytest.Dockerfile
┗ 📜requirements.txt
```

## Statistics

[WakaTime statistics](https://wakatime.com/@5217844b-3256-4044-a472-a1b780730800/projects/bfzcavsbrx?start=2023-02-05&end=2023-02-11) of the project.
