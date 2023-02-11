# README

## Notes on Codebase

As you delve into the code, you'll notice that I have not included many comments. This is because I am a firm believer in writing self-explanatory code. I have named variables appropriately, refactored the code for better readability, and added type hints for functions with complex inputs and outputs. This will make it easier for you to understand the code.

## Challenges I Faced

As this is my first time writing a medium-scale Flask application, I faced some challenges. One of the biggest challenges I faced was with regards to circular dependencies. Unlike Django, where the dependency between apps and other utilities is abstracted, Flask has a more flexible structure that requires a deeper understanding of dependencies. However, I was able to overcome this challenge and I hope that the codebase reflects my efforts.

## Assumptions I Made

One assumption I made was with regards to region codes. I assumed that if a user provides a region_slug, its child region_slug will also be included. For example, if a user provides the region_slug for Norway, it will also include the region_slug for Oslo.

## Running the Project

To run the project, execute the following command:

```bash
docker-compose up --build
```

### Test API

```
http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-20&origin=CNCWN&destination=scandinavia
```

**Expected Output**

```json
[
    {
    "average_price": 1739,
    "day": "2016-01-01"
    },
    {
    "average_price": 1738,
    "day": "2016-01-02"
    },
    {
    "average_price": 1729,
    "day": "2016-01-05"
    },
    {
    "average_price": 1728,
    "day": "2016-01-06"
    },
    {
    "average_price": 1696,
    "day": "2016-01-07"
    },
    {
    "average_price": 1630,
    "day": "2016-01-08"
    },
...
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
 ┃ ┃ ┣ 📜accessor_test.py
 ┃ ┃ ┣ 📜conftest.py
 ┃ ┃ ┗ 📜handler_test.py
 ┃ ┣ 📜application.py
 ┃ ┣ 📜logs.log
 ┃ ┣ 📜services.py
 ┃ ┗ 📜validators.py
 ┣ 📜Dockerfile
 ┣ 📜logs.log
 ┣ 📜pytest.Dockerfile
 ┗ 📜requirements.txt
```

## Statistics

[WakaTime statistics](https://wakatime.com/@5217844b-3256-4044-a472-a1b780730800/projects/bfzcavsbrx?start=2023-02-05&end=2023-02-11) of the project.

## Conclusion

I hope that the codebase meets your expectations and I would love to hear any feedback you have. If you have any questions or need clarification on any part of the code, please do not hesitate to reach out to me. I'm here to help.
